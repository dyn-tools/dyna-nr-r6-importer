import bpy
from bpy.types import Panel

class NODE_PT_AutoSetupPanel(Panel):
    """
    UI Panel for DynaTools-R6
    """
    bl_label = "DynaTools-R6"
    bl_idname = "VIEW3D_PT_dyna_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'DynaTools-R6'

    def draw(self, context):
        layout = self.layout

        # Create a box for mesh cleanup
        box = layout.box()
        box.label(text="Mesh Cleanup")

        # Button for Delete Objects Without Texture
        row = box.row()
        row.operator("object.delete_without_texture", text="Delete Objects Without Texture")
        
        # Button for Delete Flat Artifacts
        row = box.row()
        row.operator("object.delete_flat_artifacts", text="Delete Flat Artifacts")


        #Create a box for Material and Lighting Setup
        box = layout.box()
        box.label(text="Material and Lighting Setup")

        # Larger button for Auto Setup Node Group
        row = box.row()
        row.scale_y = 2.0  # Set the scale to make the button larger
        row.operator("node.auto_setup_node_group", text="Auto Setup Node Group")

        # Larger button for Create Lights From Material
        row = box.row()
        row.scale_y = 2.0  # Set the scale to make the button larger
        row.operator("object.create_lights_from_material", text="Create Lights From Material")

def register():
    bpy.utils.register_class(NODE_PT_AutoSetupPanel)

def unregister():
    bpy.utils.unregister_class(NODE_PT_AutoSetupPanel)
