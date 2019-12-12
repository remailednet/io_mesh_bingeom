bl_info = {
    "name": "Import bingeom format",
    "author": "Unknown",
    "version": (0, 1),
    "blender": (2, 80, 0),
    "location": "File > Import > bingeom",
    "description": "Import from bingeom",
    "category": "Import-Export",
}

# imports
import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, FloatProperty
from bpy.types import Operator

from . import Bingeom


class BingeomImporter(bpy.types.Operator, ImportHelper):
    bl_idname       = "import_scene.bingeom"
    bl_description  = "Import scene from bingeom"
    bl_label        = "Import bingeom"
    bl_options      = {'UNDO'}

    filename_ext = ""
    filter_glob = StringProperty(
        default="*",
        options={'HIDDEN'},
        )

    def execute(self, context):
        Bingeom.openFile(self.filepath)
        return {'FINISHED'}

def menu_import(self, context):
    self.layout.operator(BingeomImporter.bl_idname, text="Bingeom")


def make_annotations(cls):
    """Converts class fields to annotations if running with Blender 2.8"""
    if bpy.app.version < (2, 80):
        return cls
    bl_props = {k: v for k, v in cls.__dict__.items() if isinstance(v, tuple)}
    if bl_props:
        if '__annotations__' not in cls.__dict__:
            setattr(cls, '__annotations__', {})
        annotations = cls.__dict__['__annotations__']
        for k, v in bl_props.items():
            annotations[k] = v
            delattr(cls, k)
    return cls

classes = (
    BingeomImporter,
)

def register():
    for cls in classes:
        make_annotations(cls)
        bpy.utils.register_class(cls)

    if bpy.app.version < (2, 80, 0):
        bpy.types.INFO_MT_file_import.append(menu_import)
    else:
        bpy.types.TOPBAR_MT_file_import.append(menu_import)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    if bpy.app.version < (2, 80, 0):
        bpy.types.INFO_MT_file_import.remove(menu_import)
    else:
        bpy.types.TOPBAR_MT_file_import.remove(menu_import)


if __name__ == "__main__":
    register()
