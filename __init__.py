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



def register():
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
