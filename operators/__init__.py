import bpy # type: ignore

from .auto_setup import NODE_OT_AutoSetup
from .create_lights import NODE_OT_CreateLightsFromMaterial
from .delete_objects import NODE_OT_DeleteObjectsWithoutTexture, NODE_OT_DeleteFlatArtifactObjects
from .find_missing_textures import NODE_OT_FindMissingTextures
from .mesh_alignment import NODE_PT_MoveToGizmo, NODE_PT_AlignToPlane

classes = [NODE_OT_AutoSetup
           , NODE_OT_CreateLightsFromMaterial
           , NODE_OT_DeleteObjectsWithoutTexture, NODE_OT_DeleteFlatArtifactObjects
           , NODE_OT_FindMissingTextures
           , NODE_PT_MoveToGizmo, NODE_PT_AlignToPlane
           ]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)