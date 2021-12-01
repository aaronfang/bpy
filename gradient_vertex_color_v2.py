### simple script to generate top-down gradient based on selected vertices(only affect vertex-color alpha channel)
### support multi-objects
### use:
###   1, select objects
###   2, go to element mode(vertex mode)
###   3, select vertices that need to generate top-down gradient
###   4, go back to object mode
###   5, run script, and done!
### author: aaronfang
### version 0.3 @ 2021.11.29

import bpy

# Function for Message box
def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):

    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

# Main Function
def gradient_selected_vertices():

    # get selected objects
    objs = bpy.context.selected_objects

    # get current mode
    curMode = bpy.context.active_object.mode
    if curMode == 'EDIT':
        ShowMessageBox("Switch to Object Mode", "Error Massage", 'ERROR')

    # check if no object(s) selected
    if len(objs) > 0:
        # get selected vertices list
        selected_verts = []
        for obj in objs:
            mesh = obj.data
            for v in mesh.vertices:
                if v.select:
                    selected_verts.append(v)

        # check if no vertices selected
        if len(selected_verts) > 0:
            # switch to object mode if currently in edit mode
            #if curMode == 'EDIT':
                #bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
            
            # calc vert.co.z difference
            bbox = [objs[0].matrix_world @ v.co for v in selected_verts]
            max_z = max(v.z for v in bbox)
            min_z = min(v.z for v in bbox)
            diff = max_z - min_z

            # for all selected objects
            # check if selected evert vertices on object, do object based gradient.
            # else if not selected every vertices on object, do gradient based on selected vertices. 
            for obj in objs:
                mesh = obj.data

                # check if current obj has some element selected
                if len([v for v in mesh.vertices if v.select]) > 0:
                    # create vertex color Layer 'Col' if not exists
                    if not mesh.vertex_colors:
                        mesh.vertex_colors.new(name='Col')
                    
                    mesh_loops = mesh.loops
                    color_loops = mesh.vertex_colors.active.data
                    sel_verts = [v for v in mesh.vertices if v.select]

                    # check if selected vertices contains all elements in current obj
                    # if true, loop all vertices and apply vertex colors
                    # if not, loop only selected vertices to apply
                    check = all(i in sel_verts for i in mesh.vertices)

                    if check:
                            for m_loop, c_loop in zip(mesh_loops, color_loops):
                                idx = m_loop.vertex_index
                                z = mesh.vertices[idx].co.z
                                color = (z - min_z) / diff
                                c_loop.color = [c_loop.color[0],c_loop.color[1],c_loop.color[2],color]
                    else:
                        for m_loop, c_loop in zip(mesh_loops, color_loops):
                            idx = m_loop.vertex_index
                            z = mesh.vertices[idx].co.z
                            color = (z - min_z) / diff
                            for v in sel_verts:
                                if v.index == idx:
                                    c_loop.color = [c_loop.color[0],c_loop.color[1],c_loop.color[2],color]
                else:
                    ShowMessageBox("Some Object has No Vertex Selected", "Error Massage", 'ERROR')
        else:
            ShowMessageBox("Please Select Some Vertices", "Error Massage", 'ERROR')
    else:
        ShowMessageBox("Please Select One or More Objects", "Error Massage", 'ERROR')

    # switch back to previous mode
    #bpy.ops.object.mode_set(mode=curMode, toggle=False)

gradient_selected_vertices()