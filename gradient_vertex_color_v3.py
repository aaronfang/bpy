import bpy, bmesh

objs = bpy.context.selected_objects
selected_verts = []
for obj in objs:
    mesh = obj.data
    # create bmesh from mesh
    bm = bmesh.new()
    bm.from_mesh(mesh)

    for v in bm.verts:
        if v.select:
            selected_verts.append(v)

    # write to the active vertex color layer or create a new layer, if there's none
    if len(bm.loops.layers.color) > 0:
        color_layer = bm.loops.layers.color[mesh.vertex_colors.active_index]
    else:
        color_layer = bm.loops.layers.color.new("Color")

    # colorize verts based on world location
    for vert in bm.verts:
        for loop in vert.link_loops:
            if vert.select:
                loop[color_layer] = [loop[color_layer][0],loop[color_layer][1],loop[color_layer][2],vert.co.z]

    # write bmesh data to mesh
    bm.to_mesh(mesh)