import bpy
import os
import sys
import pip

from bpy.props import (StringProperty,
                       PointerProperty,
                       )
                       
from bpy.types import (Panel,
                       PropertyGroup,
                       )
                       
addon_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(addon_path)
                       
def install_dependences():
    l = os.getlogin()
    pip.main(['install', 'translators', '--user'])
    packages_path = "C:/Users/" + l + "/AppData/Roaming/Python/Python310/site-packages"
    sys.path.insert(0, packages_path)
    
def check_for_dependences():
    try:
        import translators as ts
        import lxml
        import six
        bpy.ops.mesh.primitive_cube_add()
    except ModuleNotFoundError:
        install_dependences()
                
class MyProperties(PropertyGroup):
    bar: StringProperty(
        name="Текст",
        description=":",
        default="",
        maxlen=1024,
        )
        
class button(bpy.types.Operator):
    bl_label = "button"
    bl_idname = "object.button_translate"
        
    def execute(self, context):
        check_for_dependences()
        text_Rus = bpy.context.scene.my_tool.bar
        bpy.context.scene.my_tool.bar = translators.translate_text(text_Rus, translator="google", from_language="ru", to_language="en")
        return {"FINISHED"}

class OBJECT_PT_CustomPanel(Panel):
    bl_label = "Переводчик"
    bl_idname = "OBJECT_PT_custom_panel"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "Tools"
    bl_context = "objectmode"   

    @classmethod
    def poll(self,context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        layout.prop(mytool, "bar")
        layout.separator()
        
        row = layout.row()
        row.operator("object.button_translate", text = "Перевести")
        

classes = (
    MyProperties,
    OBJECT_PT_CustomPanel,
    button
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
    bpy.types.Scene.my_tool = PointerProperty(type=MyProperties)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()