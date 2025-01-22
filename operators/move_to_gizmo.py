import bpy # type: ignore
import bmesh # type: ignore
from mathutils import Vector # type: ignore


class MoveToGizmoOperator(bpy.types.Operator):
    bl_idname = "object.move_to_gizmo"
    bl_label = "Move to Gizmo"
    bl_description = "Move object so selected vertices' midpoint aligns with 3D gizmo"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.object
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "No valid mesh object selected")
            return {'CANCELLED'}

        # Switch to Edit mode to access vertex selection
        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(obj.data)

        # Retrieve the coordinates of the selected vertices
        selected_verts = [v.co for v in bm.verts if v.select]
        if not selected_verts:
            self.report({'ERROR'}, "No vertices selected")
            bpy.ops.object.mode_set(mode='OBJECT')
            return {'CANCELLED'}

        # Calculate the midpoint of the selected vertices
        midpoint = sum(selected_verts, Vector()) / len(selected_verts)

        # Return to Object mode
        bpy.ops.object.mode_set(mode='OBJECT')

        # Calculate the offset to move the object
        gizmo_position = context.scene.cursor.location
        offset = gizmo_position - obj.matrix_world @ midpoint

        # Move the object
        for obj in context.selected_objects:
            obj.location += offset

        return {'FINISHED'}



def register():
    bpy.utils.register_class(MoveToGizmoOperator)

def unregister():
    bpy.utils.unregister_class(MoveToGizmoOperator)

if __name__ == "__main__":
    register()
