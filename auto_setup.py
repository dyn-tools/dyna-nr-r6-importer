import bpy

class NODE_OT_AutoSetup(bpy.types.Operator):
    """
    Operator to automatically set up a node group for selected objects.
    """
    bl_idname = "node.auto_setup_node_group"
    bl_label = "Auto Setup Node Group"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        def instantiate_group(nodes, data_block_name):
            group = nodes.new(type='ShaderNodeGroup')
            group.node_tree = bpy.data.node_groups[data_block_name]
            return group

        def dyn_genlink(input, output, img_node, use_premul=None):
            first_word = input.split(" ")[0]
            if first_word == "PBR" or first_word == "Normal":
                img_node.image.colorspace_settings.name = "Non-Color"
            if input == "Mix Factor":
                img_node.image.alpha_mode = 'STRAIGHT'

            if use_premul is not None and hasattr(img_node.image, 'alpha_mode'):
                img_node.image.alpha_mode = 'PREMUL' if use_premul else 'NONE'

            tree.links.new(node_group.inputs[input], img_node.outputs[output])

        for obj in context.selected_objects:
            if obj.type == 'MESH':
                mat = obj.active_material
                if mat is not None:
                    tree = mat.node_tree
                    already_existingg = False

                    for node in tree.nodes:
                        if node.type == "GROUP" and node.node_tree and node.node_tree.name == 'Siege Object BSDF':
                            already_existingg = True

                    if not already_existingg:
                        instantiate_group(mat.node_tree.nodes, 'Siege Object BSDF')

                    node_group = None
                    for node in tree.nodes:
                        if "Image Texture" in node.name and node.image is not None:
                            node.image.alpha_mode = 'NONE'
                        if node.type == "GROUP" and node.node_tree and node.node_tree.name == 'Siege Object BSDF':
                            node_group = node
                            break

                    if node_group is not None:
                        img_nodes = [node for node in tree.nodes if node.type == "TEX_IMAGE"]
                        output_node = node_group.outputs["BSDF"]
                        input_node = tree.nodes["Material Output"].inputs["Surface"]

                        count = len(img_nodes)
                        config_switch = {
                            2: {"USE-Premul": True,"Override Color": None, "Override Strength": None, "Diffuse": 0, "Alpha Input": 0, "PBR Multi": None,
                             "Normal Base": 1, "Mix Factor": None, "Diffuse 2": None, "Alpha Input 2": None, "PBR Multi 2": None, "Normal Base 2": None},
                            3: {"USE-Premul": True, "Override Color": None, "Override Strength": None, "Diffuse": 0, "Alpha Input": 0, "PBR Multi": 2,
                             "Normal Base": 1, "Mix Factor": None, "Diffuse 2": None, "Alpha Input 2": None, "PBR Multi 2": None, "Normal Base 2": None},
                            4: {"USE-Premul": True, "Override Color": 3, "Override Strength": 3, "Diffuse": 0, "Alpha Input": 0, "PBR Multi": 2,
                             "Normal Base": 1, "Mix Factor": None, "Diffuse 2": None, "Alpha Input 2": None, "PBR Multi 2": None, "Normal Base 2": None},
                            5: {"USE-Premul": True, "Override Color": 3, "Override Strength": 3, "Diffuse": 0, "Alpha Input": 0, "PBR Multi": 2,
                             "Normal Base": 1, "Mix Factor": None, "Diffuse 2": None, "Alpha Input 2": None, "PBR Multi 2": None, "Normal Base 2": None},
                            6: {"Override Color": None, "Override Strength": None, "Diffuse": 3, "Alpha Input": None, "PBR Multi": 5,
                             "Normal Base": 4, "Mix Factor": 0, "Diffuse 2": 0, "Alpha Input 2": None, "PBR Multi 2": 2, "Normal Base 2": 1},
                            7: {"Override Color": None, "Override Strength": None, "Diffuse": 3, "Alpha Input": None, "PBR Multi": 5,
                             "Normal Base": 4, "Mix Factor": 0, "Diffuse 2": 0, "Alpha Input 2": None, "PBR Multi 2": 2, "Normal Base 2": 1}
                            }
                        default_config = {}
                        config = config_switch.get(count, default_config)
                        for input_name, img_index in config.items():
                            if img_index is not None and img_index < count:
                                img_node = img_nodes[img_index]
                                use_premul = config.get("USE-Premul", False)
                                first_word = input_name.split(" ")[0]
                                if input_name == "Override Strength" or input_name == "PBR" or input_name == "Mix Factor" or first_word == "Alpha":
                                    dyn_genlink(input_name, "Alpha", img_node, use_premul=use_premul)
                                elif input_name != "USE-Premul":
                                    dyn_genlink(input_name, "Color", img_node)

                        tree.links.new(input_node, output_node)

        return {'FINISHED'}

def register():
    bpy.utils.register_class(NODE_OT_AutoSetup)

def unregister():
    bpy.utils.unregister_class(NODE_OT_AutoSetup)