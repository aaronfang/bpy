import bpy
from mathutils import Vector
obj = bpy.context.object
me = obj.data

# get min and max z from bounding box and their differential
bbox = [Vector(point) for point in obj.bound_box]
max_z = max(v.z for v in bbox)
min_z = min(v.z for v in bbox)
diff = max_z - min_z

mesh_loops = me.loops
color_loops = me.vertex_colors.active.data

# vcol data is stored in a loop layer. to find the corresponding vertex,
# we'll use the regular mesh loops to find the vertex index and then access
# obj.data.vertices to get the z location.
for m_loop, c_loop in zip(mesh_loops, color_loops):

    idx = m_loop.vertex_index  # each loop has one vert index
    z = me.vertices[idx].co.z # store the z location from the index
    color = (z - min_z) / diff # calculate a normalized range (0.0 to 1.0)

    c_loop.color = [color] * 4  # apply to the color loop as [color, color, color, 1]