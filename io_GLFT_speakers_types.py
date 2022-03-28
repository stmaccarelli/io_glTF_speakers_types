import bpy

bl_info = {
    "name": "glTF Extras: Speakers and types",
    "category": "Import-Export",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    'location': 'File > Export > glTF 2.0',
    'description': 'Exports speaker properties and Blender object types as glTF extras.',
    'tracker_url': "https://github.com/KhronosGroup/glTF-Blender-IO/issues/",  # Replace with your issue tracker
    'isDraft': False,
    'developer': "stmaccarelli", # Replace this
    'url': 'https://stefano-maccarelli.com',  # Replace this
}


class MoreExtrasProperties(bpy.types.PropertyGroup):
    enabled: bpy.props.BoolProperty(
        name=bl_info["name"],
        description='Master Enable.',
        default=True
        )
    objects_type: bpy.props.BoolProperty(
        name='Blender Types',
        description='export Blender object types.',
        default=True
        )
    speakers_extras: bpy.props.BoolProperty(
        name='Speakers Data',
        description='export speaker extra data like filename and more.',
        default=True
        )

def register():
    bpy.utils.register_class(MoreExtrasProperties)
    bpy.types.Scene.MoreExtrasProperties = bpy.props.PointerProperty(type=MoreExtrasProperties)

def register_panel():
    # Register the panel on demand, we need to be sure to only register it once
    # This is necessary because the panel is a child of the extensions panel,
    # which may not be registered when we try to register this extension
    try:
        bpy.utils.register_class(GLTF_PT_MoreExtrasPropertiesPanel)
    except Exception:
        pass

    # If the glTF exporter is disabled, we need to unregister the extension panel
    # Just return a function to the exporter so it can unregister the panel
    return unregister_panel


def unregister_panel():
    # Since panel is registered on demand, it is possible it is not registered
    try:
        bpy.utils.unregister_class(GLTF_PT_MoreExtrasPropertiesPanel)
    except Exception:
        pass


def unregister():
    unregister_panel()
    bpy.utils.unregister_class(MoreExtrasProperties)
    del bpy.types.Scene.MoreExtrasProperties

class GLTF_PT_MoreExtrasPropertiesPanel(bpy.types.Panel):

    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "More Extras"
    bl_parent_id = "FILE_PT_operator"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator

        return operator.bl_idname == "EXPORT_SCENE_OT_gltf"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        props = bpy.context.scene.MoreExtrasProperties

        col = layout.column(heading = "Enable", align = True)
        col.prop(props, 'enabled')

        col = layout.column(heading = "Data", align = True)
        col.active = props.enabled
        col.prop(props, 'objects_type')
        col.prop(props, 'speakers_extras')


class glTF2ExportUserExtension:

    def __init__(self):
        # We need to wait until we create the gltf2UserExtension to import the gltf2 modules
        # Otherwise, it may fail because the gltf2 may not be loaded yet
        from io_scene_gltf2.io.com.gltf2_io import Node
        self.Node = Node
        self.properties = bpy.context.scene.MoreExtrasProperties

    def gather_node_hook(self, gltf2_node, blender_object, export_settings):

        if not gltf2_node.extras and self.properties.enabled:
            gltf2_node.extras = {}
        
        if self.properties.objects_type:
            gltf2_node.extras["bl_type"] = blender_object.type

        if blender_object.type == 'SPEAKER' and self.properties.speakers_extras:
            # gltf2_node.name = "SPEAKER "+gltf2_node.name #here we could modify node name
            # gltf2_node.extras["bl_type"] = blender_object.type
            gltf2_node.extras["filename"] = blender_object.data.sound.name_full
            gltf2_node.extras["volume"] = blender_object.data.volume
            gltf2_node.extras["pitch"] = blender_object.data.pitch
            gltf2_node.extras["volume_max"] = blender_object.data.volume_max
            gltf2_node.extras["volume_min"] = blender_object.data.volume_min
            gltf2_node.extras["attenuation"] = blender_object.data.attenuation
            gltf2_node.extras["distance_max"] = blender_object.data.distance_max
            gltf2_node.extras["distance_reference"] = blender_object.data.distance_reference
            gltf2_node.extras["cone_angle_inner"] = blender_object.data.cone_angle_inner
            gltf2_node.extras["cone_angle_outer"] = blender_object.data.cone_angle_outer
            gltf2_node.extras["cone_volume_outer"] = blender_object.data.cone_volume_outer