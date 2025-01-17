bl_info = {
    "name": "Dyna R6 NR Importer",
    "description": "Tool for importing and managing NR assets in R6.",
    "author": "dyn4micfx",
    "version": (2, 0),
    "blender": (4, 1, 0),
    "location": "View3D > Sidebar > Dyna R6",
    "warning": "",
    "wiki_url": "http://my.wiki.url",
    "tracker_url": "http://my.bugtracker.url",
    "support": "COMMUNITY",
    "category": "Import-Export",
}

import bpy
import os
from . import auto_setup, delete_objects, create_lights, ui_panel

def append_shader_group(group_name):
    """
    Append a shader group from the `shader_groups.blend` file.
    """
    # Defer accessing bpy.data.node_groups to avoid restrictions
    if group_name in [ng.name for ng in bpy.data.node_groups]:
        return bpy.data.node_groups[group_name]

    addon_path = os.path.dirname(os.path.abspath(__file__))
    shader_file = os.path.join(addon_path, "shader_groups.blend")

    # Append the shader group from the `.blend` file
    with bpy.data.libraries.load(shader_file, link=False) as (data_from, data_to):
        if group_name in data_from.node_groups:
            data_to.node_groups.append(group_name)
        else:
            print(f"Shader group '{group_name}' not found in {shader_file}.")

    return bpy.data.node_groups.get(group_name)

def load_shader_groups(dummy=None):
    """
    Load the 'Siege Object BSDF' shader group after Blender context is fully initialized.
    """
    shader_groups = ["Siege Object BSDF"]  # Replace/add additional group names if needed
    for group_name in shader_groups:
        shader_group = append_shader_group(group_name)
        if shader_group:
            print(f"Shader group '{group_name}' loaded successfully.")
        else:
            print(f"Shader group '{group_name}' could not be loaded.")

def register():
    bpy.app.timers.register(load_shader_groups)  # Use a timer to defer execution
    auto_setup.register()
    delete_objects.register()
    create_lights.register()
    ui_panel.register()

def unregister():
    ui_panel.unregister()
    create_lights.unregister()
    delete_objects.unregister()
    auto_setup.unregister()

if __name__ == "__main__":
    register()
