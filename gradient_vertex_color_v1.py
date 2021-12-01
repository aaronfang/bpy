import bpy
from mathutils import Vector

objs = bpy.context.selected_objects
selected_verts = []
for obj in objs:
    mesh = obj.data
    for v in mesh.vertices:
        if v.select:
            selected_verts.append(v)

bbox = [objs[0].matrix_world @ v.co for v in selected_verts]
max_z = max(v.z for v in bbox)
min_z = min(v.z for v in bbox)
diff = max_z - min_z

for obj in objs:
    mesh = obj.data
    mesh_loops = mesh.loops
    color_loops = mesh.vertex_colors.active.data
    for m_loop, c_loop in zip(mesh_loops, color_loops):
        idx = m_loop.vertex_index
        z = mesh.vertices[idx].co.z
        color = (z - min_z) / diff
        for v in selected_verts:
            if v.index == idx:
                c_loop.color = [c_loop.color[0],c_loop.color[1],c_loop.color[2],color]