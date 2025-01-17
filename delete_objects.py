import bpy

class NODE_OT_DeleteObjectsWithoutTexture(bpy.types.Operator):
    """
    Operator to delete objects without materials or textures.
    """
    bl_idname = "object.delete_without_texture"
    bl_label = "Delete Objects Without Texture"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Get a list of all objects in the current scene
        all_objects = bpy.context.scene.objects

        # Track the number of deleted objects
        deleted_count = 0

        # Loop through each object in the scene
        for obj in list(all_objects):
            # Check if the object has any material slots
            if len(obj.material_slots) == 0:
                # If the object doesn't have any materials, delete it
                bpy.data.objects.remove(obj, do_unlink=True)
                deleted_count += 1

        # Report how many objects were deleted
        if deleted_count > 0:
            self.report({'INFO'}, f"Deleted {deleted_count} objects without materials or textures.")
        else:
            self.report({'INFO'}, "No objects without materials or textures were found.")

        return {'FINISHED'}

def register():
    bpy.utils.register_class(NODE_OT_DeleteObjectsWithoutTexture)

def unregister():
    bpy.utils.unregister_class(NODE_OT_DeleteObjectsWithoutTexture)
