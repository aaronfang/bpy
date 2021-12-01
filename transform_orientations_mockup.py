	
	
	
bl_info = {
    "name": "Transform Orientations Mockup",
    "author": "CoDEmanX",
    "version": (0, 3),
    "blender": (2, 68, 0),
    "location": "View3D > Header",
    "description": "Replace View 3D header by one with a Transform Orientations prototype",
    "warning": "Dirty hack",
    "wiki_url": "",
    "tracker_url": "",
    "category": "3D View"}

import bpy
from bpy.props import *
from bpy.types import Header, Menu, Panel
from bl_ui.properties_paint_common import UnifiedPaintPanel
from bpy.app.translations import contexts as i18n_contexts

def actions(self, context):
    create = ('CREATE', "Create", "", "ZOOMIN", 1)
    overwrite = ('OVERWRITE', "Overwrite", "", "FILE_REFRESH", 2)
    rename = ('RENAME', "Rename", "", "GREASEPENCIL", 3)
    delete = ('DELETE', "Delete", "", "X", 4)
    delete_all = ('DELETE_ALL', "Delete All", "", "X", 5)
    l = []
    o = context.space_data.current_orientation
    l.append(create)
    if o is not None:
        l.append(overwrite)
        l.append(rename)
        l.append(delete)
    if len(context.scene.orientations):
        l.append(delete_all)
    return l
    

class TRANSFORM_OT_orientation_specials(bpy.types.Operator):
    bl_label = "Transform Orientation Specials"
    bl_idname = "transform.orientation_specials"
    bl_description = ("Create new transform orientation "
                      "(hold Shift to overwrite, "
                      "Ctrl to rename, "
                      "Alt to delete)")
    
    action = EnumProperty(items=actions)
    
    def invoke(self, context, event):
        
        obj = context.object
        name = getattr(obj, "name", None)
        props = {}
        current_orientation = context.space_data.current_orientation
        action = self.action
        
        print("ctrl?", event.ctrl)
        if event.shift:
            action = 'OVERWRITE'
        elif event.ctrl:
            action = 'RENAME'
        elif event.alt:
            action = 'DELETE'

        
        if action == 'OVERWRITE':
            
            #row.enabled = current_orientation is not None
            props["use"] = True #?
            props["overwrite"] = True
                
            #props.use_view = True # ???
            if current_orientation is not None:
                props['name'] = current_orientation.name
            
            #props.name = getattr(context.space_data.current_orientation, "name", "")
            bpy.ops.transform.create_orientation(**props)
        
        elif action == 'RENAME':
            
            if not bpy.ops.transform.rename_orientation.poll():
                self.report({'WARNING'}, "Need CUSTOM transform orientation")
                return {'CANCELLED'}
        
            # NOTE: use index to fetch the right one
            for i, to in enumerate(context.scene.orientations):
                if to == current_orientation:
                    props["index"] = i
                    break
    
            props["name"] = getattr(context.space_data.current_orientation, "name", "")
            bpy.ops.transform.rename_orientation('INVOKE_DEFAULT', **props)
            
        elif action == 'DELETE':
            if not bpy.ops.transform.delete_orientation.poll():
                self.report({'WARNING'}, "Need CUSTOM transform orientation")
                return {'CANCELLED'}
            bpy.ops.transform.delete_orientation()

        elif action == 'DELETE_ALL':
            bpy.ops.transform.delete_all_orientations()
        
        else: #action == 'CREATE':
            props["use"] = True
            props["overwrite"] = False
            
            if name is None:
                props["use_view"] = True # make this another menu entry?
            else:
                props["name"] = name
                
            bpy.ops.transform.create_orientation(**props)

        
        return {'FINISHED'}
    
     


def draw_template_header_3D(self, context):
    layout = self.layout

    view = context.space_data
    mode_string = context.mode
    edit_object = context.edit_object
    obj = context.active_object
    toolsettings = context.tool_settings

    row = layout.row(align=True)
    row.template_header()

    # Menus
    if context.area.show_menus:
        sub = row.row(align=True)

        sub.menu("VIEW3D_MT_view")

        # Select Menu
        if mode_string in {'PAINT_WEIGHT', 'PAINT_VERTEX', 'PAINT_TEXTURE'}:
            mesh = obj.data
            if mesh.use_paint_mask:
                sub.menu("VIEW3D_MT_select_paint_mask")
            elif mesh.use_paint_mask_vertex and mode_string == 'PAINT_WEIGHT':
                sub.menu("VIEW3D_MT_select_paint_mask_vertex")
        elif mode_string not in {'EDIT_TEXT', 'SCULPT'}:
            sub.menu("VIEW3D_MT_select_%s" % mode_string.lower())

        if edit_object:
            sub.menu("VIEW3D_MT_edit_%s" % edit_object.type.lower())
        elif obj:
            if mode_string not in {'PAINT_TEXTURE'}:
                sub.menu("VIEW3D_MT_%s" % mode_string.lower())
            if mode_string in {'SCULPT', 'PAINT_VERTEX', 'PAINT_WEIGHT', 'PAINT_TEXTURE'}:
                sub.menu("VIEW3D_MT_brush")
            if mode_string == 'SCULPT':
                sub.menu("VIEW3D_MT_hide_mask")
        else:
            sub.menu("VIEW3D_MT_object")

    # Contains buttons like Mode, Pivot, Manipulator, Layer, Mesh Select Mode...
    #layout.template_header_3D()

    modes = bpy.types.Object.bl_rna.properties['mode'].enum_items
    
    if obj:
        mode = modes[obj.mode]
    else:
        mode = modes['OBJECT']
    #layout.menu(OBJECT_MT_mode_set.bl_idname, text=mode.name, icon=mode.icon)
    layout.operator_menu_enum("object.mode_set", "mode", text=mode.name, icon=mode.icon)
    
    
    layout.prop(context.space_data, "viewport_shade", text="", icon_only=True)
    
    #if not obj or obj.mode in {'OBJECT', 'EDIT'}:
    # much more fancy stuff here...
    
    row = layout.row(True)
    row.prop(context.space_data, "pivot_point", text="", icon_only=True)
    row.prop(context.space_data, "use_pivot_point_align", text="", icon_only=True)
    

    wm = context.window_manager
    row = layout.row(True)
    row.prop(context.space_data, "show_manipulator", text="")
    
    if context.space_data.show_manipulator:
        sub = row.row(True)
        sub.prop(context.space_data, "transform_manipulators", icon_only=True)
        sub = row.row(True)
        #sub.scale_x = 0.4
        sub.prop(context.space_data, "transform_orientation", text="")
        sub = row.row(True)
        sub.scale_x = 0.5
        #sub.menu(SimpleCustomMenu.bl_idname, text="", icon="DOWNARROW_HLT")
        #sub.operator("wm.call_menu", text="", icon="DOWNARROW_HLT").name = SimpleCustomMenu.bl_idname
        sub.operator_menu_enum("transform.orientation_specials", "action", text="", icon="DOWNARROW_HLT")

        props = row.operator("transform.orientation_specials", icon='ZOOMIN', text="")
        props.action = 'CREATE'

#        sub = row.row(True)
#        if wm.ctrl:
#            props = sub.operator("transform.rename_orientation", text="", icon="ZOOMIN")
#            props.name = getattr(context.space_data.current_orientation, "name", "")
#        elif wm.alt:
#            sub.operator("transform.delete_orientation", text="", icon="ZOOMIN")
#        elif wm.shift:
#            current_orientation = context.space_data.current_orientation
#            props = sub.operator("transform.create_orientation", text="", icon="ZOOMIN")
#            props.use = True
#            props.overwrite = True
#            if current_orientation is not None:
#                props.name = current_orientation.name
#            
#        else:
#            name = getattr(context.object, "name", None)
#            props = sub.operator("transform.create_orientation", text="", icon="ZOOMIN")
#            props.use = True
#            props.overwrite = False
#            if name is None:
#                props.use_view = True # make this another menu entry?
#            else:
#                props.name = name
    
    row = layout.row()
    row.scale_x = 0.7
    row.scale_y = 0.7
    row.prop(context.scene, "layers", text="")
    
    if obj:
        if obj.mode == 'EDIT':
            row = layout.row(True)
            row.prop(context.tool_settings, "mesh_select_mode", index=0, icon="VERTEXSEL", text="")
            row.prop(context.tool_settings, "mesh_select_mode", index=1, icon="EDGESEL", text="")
            row.prop(context.tool_settings, "mesh_select_mode", index=2, icon="FACESEL", text="")
        else:
            layout.prop(context.space_data, "lock_camera_and_layers", text="")
    
    row = layout.row()
    
    if obj:
        mode = obj.mode
        # Particle edit
        if mode == 'PARTICLE_EDIT':
            row.prop(toolsettings.particle_edit, "select_mode", text="", expand=True)

        # Occlude geometry
        if ((view.viewport_shade not in {'BOUNDBOX', 'WIREFRAME'} and (mode == 'PARTICLE_EDIT' or (mode == 'EDIT' and obj.type == 'MESH'))) or
                (mode == 'WEIGHT_PAINT')):
            row.prop(view, "use_occlude_geometry", text="")

        # Proportional editing
        if mode in {'EDIT', 'PARTICLE_EDIT'}:
            row = layout.row(align=True)
            row.prop(toolsettings, "proportional_edit", text="", icon_only=True)
            if toolsettings.proportional_edit != 'DISABLED':
                row.prop(toolsettings, "proportional_edit_falloff", text="", icon_only=True)
        elif mode == 'OBJECT':
            row = layout.row(align=True)
            row.prop(toolsettings, "use_proportional_edit_objects", text="", icon_only=True)
            if toolsettings.use_proportional_edit_objects:
                row.prop(toolsettings, "proportional_edit_falloff", text="", icon_only=True)

    # Snap
    if not obj or mode not in {'SCULPT', 'VERTEX_PAINT', 'WEIGHT_PAINT', 'TEXTURE_PAINT'}:
        snap_element = toolsettings.snap_element
        row = layout.row(align=True)
        row.prop(toolsettings, "use_snap", text="")
        row.prop(toolsettings, "snap_element", text="", icon_only=True)
        if snap_element != 'INCREMENT':
            row.prop(toolsettings, "snap_target", text="")
            if obj:
                if mode in {'OBJECT', 'POSE'} and snap_element != 'VOLUME':
                    row.prop(toolsettings, "use_snap_align_rotation", text="")
                elif mode == 'EDIT':
                    row.prop(toolsettings, "use_snap_self", text="")

        if snap_element == 'VOLUME':
            row.prop(toolsettings, "use_snap_peel_object", text="")
        elif snap_element == 'FACE':
            row.prop(toolsettings, "use_snap_project", text="")

    # AutoMerge editing
    if obj:
        if (mode == 'EDIT' and obj.type == 'MESH'):
            layout.prop(toolsettings, "use_mesh_automerge", text="", icon='AUTOMERGE_ON')

    # OpenGL render
    row = layout.row(align=True)
    row.operator("render.opengl", text="", icon='RENDER_STILL')
    row.operator("render.opengl", text="", icon='RENDER_ANIMATION').animation = True

    # Pose
    if obj and mode == 'POSE':
        row = layout.row(align=True)
        row.operator("pose.copy", text="", icon='COPYDOWN')
        row.operator("pose.paste", text="", icon='PASTEDOWN')
        row.operator("pose.paste", text="", icon='PASTEFLIPDOWN').flipped = 1


class DeleteAllOrientations(bpy.types.Operator):
    """Move an object with the mouse, example"""
    bl_idname = "transform.delete_all_orientations"
    bl_label = "Delete all Transform Orientations"

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D' and len(context.scene.orientations)
        
    def execute(self, context):
        for to in context.scene.orientations:
            context.space_data.transform_orientation = to.name
            if context.space_data.current_orientation is not None:
                bpy.ops.transform.delete_orientation()
        return {'FINISHED'}
        
        
class RenameOrientation(bpy.types.Operator):
    """Move an object with the mouse, example"""
    bl_idname = "transform.rename_orientation"
    bl_label = "Rename Transform Orientation"
    
    name = bpy.props.StringProperty()
    index = bpy.props.IntProperty(default=-1, options={'HIDDEN'})
    
    @classmethod
    def poll(cls, context):
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                return area.spaces[0].current_orientation is not None
        return False
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    def execute(self, context):
        if not self.name:
            return {'CANCELLED'}
        
        if self.index >= 0:
            try:
                context.scene.orientations[self.index].name = self.name
            except IndexError:
                return {'CANCELLED'}
        else:
            for area in context.screen.areas:
                if area.type == 'VIEW_3D':
                    o = area.spaces[0].current_orientation
                    o.name = self.name
                    break
        return {'FINISHED'}


class OBJECT_MT_mode_set(bpy.types.Menu):
    bl_idname = "OBJECT_MT_mode_set"
    bl_label = "mode"
    
    def draw(self, context):
        self.layout.operator_enum("object.mode_set", "mode")

class G:
    draw = bpy.types.VIEW3D_HT_header.draw

def register():
    bpy.types.WindowManager.ctrl = bpy.props.BoolProperty()
    bpy.types.WindowManager.alt = bpy.props.BoolProperty()
    bpy.types.WindowManager.shift = bpy.props.BoolProperty()
    bpy.utils.register_module(__name__)
    bpy.types.VIEW3D_HT_header.draw = draw_template_header_3D


def unregister():
    del bpy.types.WindowManager.ctrl
    del bpy.types.WindowManager.alt
    del bpy.types.WindowManager.shift
    bpy.utils.unregister_module(__name__)
    bpy.types.VIEW3D_HT_header.draw = G.draw
    
if __name__ == "__main__":
    register()

	
	
	
	