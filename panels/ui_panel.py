import bpy # type: ignore
from bpy.types import Panel # type: ignore

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

        # Button for Delete Flat Artifacts
        row = box.row()
        row.operator("object.delete_flat_artifacts", text="Delete Flat Artifacts")

        # Button for Delete Objects Without Texture
        row = box.row()
        row.operator("object.delete_without_texture", text="Delete Objects Without Texture")
        

    #Create a box for Material and Lighting Setup
        box = layout.box()
        box.label(text="Material and Lighting Setup")

        # Button for Auto Setup Node Group
        row = box.row()
        row.scale_y = 2.0  # Set the scale to make the button larger
        row.operator("node.auto_setup_node_group", text="Auto Setup Node Group")

        # Button for Create Lights From Material
        row = box.row()
        row.scale_y = 2.0  # Set the scale to make the button larger
        row.operator("object.create_lights_from_material", text="Create Lights From Material")


    #Create a box for Material and Lighting Setup
        box = layout.box()
        box.label(text="Find Missing Textures For Selected:")

        # Settings for Find Missing Textures
        row = box.row()
        settings = context.scene.texture_import_settings

        # Property for log file path
        row = box.row()
        row.prop(settings, "log_file_path")

        # Property for log file path
        row = box.row()
        row.prop(settings, "texture_folder")

        # Button for Find Missing Textures
        row = box.row()
        row.operator("texture.find_missing_textures_for_mat")

def register():
    bpy.utils.register_class(NODE_PT_AutoSetupPanel)

def unregister():
    bpy.utils.unregister_class(NODE_PT_AutoSetupPanel)
