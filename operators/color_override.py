import bpy
import platform
import subprocess



class OBJECT_OT_SetVertexColor(bpy.types.Operator):
    """Apply override color to vertex colors"""
    bl_idname = "object.set_override_color"
    bl_label = "Apply Override Color"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        color = context.scene.override_color
        r, g, b = color
        attr_name = "override_color"
        mat_node_name = "Siege Object BSDF"

        for obj in context.selected_objects:
            if obj.type == 'MESH':
                # Create a new color attribute if it doesn't exist
                if attr_name not in obj.data.attributes:
                    color_attr = obj.data.color_attributes.new(name=attr_name, type='BYTE_COLOR', domain='POINT')
                else:
                    color_attr = obj.data.color_attributes[attr_name]

                # Assign color to all vertices
                for i in range(len(obj.data.vertices)):
                    color_attr.data[i].color = (r, g, b, 1.0)

                obj.data.update()

                # Ensure material node tree updates
                if obj.active_material:
                    obj.active_material.use_nodes = True
                    bsdf = obj.active_material.node_tree.nodes.get(mat_node_name)
                    
                    if bsdf and "Override Color" in bsdf.inputs:
                        vcol_node = obj.active_material.node_tree.nodes.get("Vertex Color")
                        if not vcol_node:
                            vcol_node = obj.active_material.node_tree.nodes.new("ShaderNodeVertexColor")
                        vcol_node.layer_name = attr_name
                        obj.active_material.node_tree.links.new(vcol_node.outputs["Color"], bsdf.inputs["Override Color"])

        return {'FINISHED'}


class OBJECT_OT_CopyColor(bpy.types.Operator):
    """Copy primary selected object's color to others or to clipboard"""
    bl_idname = "object.copy_color"
    bl_label = "Copy Color"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_objects = context.selected_objects
        active_object = context.view_layer.objects.active
        attr_name = "override_color"


        if not active_object or active_object.type != 'MESH':
            self.report({'WARNING'}, "Active object is not a mesh.")
            return {'CANCELLED'}

        if attr_name not in active_object.data.attributes:
            self.report({'WARNING'}, "Active object does not have an override color.")
            return {'CANCELLED'}

        color_attr = active_object.data.attributes[attr_name]
        active_color = color_attr.data[0].color[:3]  # Get first stored color

        if len(selected_objects) > 1:
            for obj in selected_objects:
                if obj != active_object and obj.type == 'MESH':

                    # Ensure override color exists
                    if attr_name not in obj.data.attributes:
                        color_attr = obj.data.color_attributes.new(name=attr_name, type='BYTE_COLOR', domain='POINT')
                    else:
                        color_attr = obj.data.attributes[attr_name]

                    # Assign color to all vertices
                    for i in range(len(obj.data.vertices)):
                        color_attr.data[i].color = (*active_color, 1.0)

                    obj.data.update()

                    # Update viewport shading
                    if obj.active_material:
                        obj.active_material.use_nodes = True
                        bsdf = obj.active_material.node_tree.nodes.get("Principled BSDF")
                        
                        if bsdf and "Base Color" in bsdf.inputs:
                            vcol_node = obj.active_material.node_tree.nodes.get("Vertex Color")
                            if not vcol_node:
                                vcol_node = obj.active_material.node_tree.nodes.new("ShaderNodeVertexColor")
                            vcol_node.layer_name = attr_name
                            obj.active_material.node_tree.links.new(vcol_node.outputs["Color"], bsdf.inputs["Base Color"])

            self.report({'INFO'}, "Color copied to selected objects.")
        else:
            # Copy to clipboard
            hex_color = '#{:02X}{:02X}{:02X}'.format(
                int(active_color[0] * 255),
                int(active_color[1] * 255),
                int(active_color[2] * 255)
            )
            self.copy_to_clipboard(hex_color)
            self.report({'INFO'}, f"Color {hex_color} copied to clipboard.")

        return {'FINISHED'}


    def copy_to_clipboard(self, text):
        platform_name = platform.system()
        try:
            if platform_name == 'Windows':
                subprocess.run(['clip'], input=text.strip().encode('utf-8'), check=True)
            elif platform_name == 'Darwin':  # macOS
                subprocess.run(['pbcopy'], input=text.strip().encode('utf-8'), check=True)
            else:  # Linux
                subprocess.run(['xclip', '-selection', 'clipboard'], input=text.strip().encode('utf-8'), check=True)
        except Exception as e:
            self.report({'WARNING'}, f"Failed to copy to clipboard: {e}")


def register():
    bpy.utils.register_class(OBJECT_OT_SetVertexColor)
    bpy.utils.register_class(OBJECT_OT_CopyColor)

    bpy.types.Scene.override_color = bpy.props.FloatVectorProperty(
        name="Override Color",
        subtype='COLOR',
        default=(1.0, 1.0, 1.0),
        min=0.0, max=1.0,
        size=3
    )

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_SetVertexColor)
    bpy.utils.unregister_class(OBJECT_OT_CopyColor)

    del bpy.types.Scene.override_color

if __name__ == "__main__":
    register()
