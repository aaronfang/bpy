import bpy
from mathutils import Vector
obj = bpy.context.object
me = obj.data
selected_verts = [v for v in mesh.vertices if v.select]

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




if bpy.context.active_object.mode == 'edit':
    bpy.ops.object.editmode_toggle()

for poly in mesh.polygons:
    for loop_index in poly.loop_indices:
        loop_vert_index = mesh.loops[loop_index].vertex_index
        print(loop_index)
        for v in selected_verts:
            if v == loop_vert_index:
            vcol_layer.data[loop_index].color = colo



for v in selected_verts:
    if v.index == loop_vert_index:
        print(v.index)


import bpy
from mathutils import Vector

obj = bpy.context.object
mesh = obj.data
selected_verts = [v for v in mesh.vertices if v.select]
vcol_layer = mesh.vertex_colors.active
print(vcol_layer)

for poly in mesh.polygons:
    for loop_index in poly.loop_indices:
        loop_vert_index = mesh.loops[loop_index].vertex_index
        for v in selected_verts:
            if v.index == loop_vert_index:
                print("yes")#print(vcol_layer.data[v.index].color)


import bpy
from mathutils import Vector

obj = bpy.context.object
mesh = obj.data
selected_verts = [v for v in mesh.vertices if v.select]
color_loops = mesh.vertex_colors.active.data

# get min and max z from bounding box and their differential
bbox = [Vector(point) for point in obj.bound_box]
max_z = max(v.z for v in bbox)
min_z = min(v.z for v in bbox)
diff = max_z - min_z

for m_loop, c_loop in zip(mesh.loops, color_loops):
    idx = m_loop.vertex_index
    z = mesh.vertices[idx].co.z
    color = (z - min_z) / diff
    for v in selected_verts:
        if v.index == idx:
            print(v)
            #color_loops.data[v.index].color = color


import bpy
from mathutils import Vector

obj = bpy.context.object
mesh = obj.data
color_loops = mesh.vertex_colors.active.data
selected_verts = [v for v in mesh.vertices if v.select]

# get min and max z from bounding box and their differential
bbox = [Vector(point) for point in obj.bound_box]
max_z = max(v.z for v in bbox)
min_z = min(v.z for v in bbox)
diff = max_z - min_z

for m_loop, c_loop in zip(mesh.loops, color_loops):
    idx = m_loop.vertex_index
    z = mesh.vertices[idx].co.z
    color = (z - min_z) / diff
    for v in selected_verts:
        if v.index == idx:
            c_loop.color = [c_loop.color[0],c_loop.color[1],c_loop.color[2],color]



import bpy
from mathutils import Vector

obj = bpy.context.object
mesh = obj.data
selected_verts = [v for v in mesh.vertices if v.select]

bbox = [obj.matrix_world @ v.co for v in selected_verts]
max_z = max(v.z for v in bbox)
min_z = min(v.z for v in bbox)
diff = max_z - min_z


import bpy
from mathutils import Vector

obj = bpy.context.object
mesh = obj.data
color_loops = mesh.vertex_colors.active.data
selected_verts = [v for v in mesh.vertices if v.select]

bbox = [obj.matrix_world @ v.co for v in selected_verts]
max_z = max(v.z for v in bbox)
min_z = min(v.z for v in bbox)
diff = max_z - min_z

for m_loop, c_loop in zip(mesh.loops, color_loops):
    idx = m_loop.vertex_index
    z = mesh.vertices[idx].co.z
    color = (z - min_z) / diff
    for v in selected_verts:
        if v.index == idx:
            c_loop.color = [c_loop.color[0],c_loop.color[1],c_loop.color[2],color]



import bpy
import bmesh

objs = bpy.context.objects_in_mode
dic_v = {}
for obj in objs:
    dic_v.update( {obj : []} )
    bm = bmesh.from_edit_mesh(obj.data)
    print(bm)
    for v in bm.verts:
        if v.select:
            dic_v[obj].append(v.index)

#print(dic_v)



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

dic_color = {}
for obj in objs:
    mesh = obj.data
    mesh_loops = mesh.loops
    color_loops = mesh.vertex_colors.active.data
    for m_loop, c_loop in zip(mesh_loops, color_loops):
        idx = m_loop.vertex_index
        dic_color.update({idx:[]})
        z = mesh.vertices[idx].co.z
        zColor = (z - min_z) / diff
        dic_color[idx].extend([c_loop.color[0],c_loop.color[1],c_loop.color[2],zColor])

for v in selected_verts:
    if v.index in dic_color:
        print('index: ' + str(v.index) + ' - '+ 'color: ' + str(dic_color[v.index]))
#        c_loop.color = [c_loop.color[0],c_loop.color[1],c_loop.color[2],dic_color[v.index][0]]

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

dic_color = {}
for obj in objs:
    mesh = obj.data
    mesh_loops = mesh.loops
    color_loops = mesh.vertex_colors.active.data
    for m_loop, c_loop in zip(mesh_loops, color_loops):
        idx = m_loop.vertex_index
        dic_color.update({idx:[]})
        z = mesh.vertices[idx].co.z
        zColor = (z - min_z) / diff
        dic_color[idx].extend([c_loop,c_loop.color[0],c_loop.color[1],c_loop.color[2],zColor])

#print(dic_color.get(next(iter(dic_color)))[0])# get index
for v in selected_verts:
    if v.index in list(dic_color.keys()):
        vtxCol = dic_color[v.index][0].color
        color = [dic_color[v.index][1],dic_color[v.index][2],dic_color[v.index][3]]
        print(vtxCol)
        vtxCol = color







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
    color_loops = mesh.vertex_colors.active.data
    for polygon in mesh.polygons:
        for v in selected_verts:
            for i, index in enumerate(polygon.vertices):
                if v.index == index:
                    print(v.index)




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
    color_loops = mesh.vertex_colors.active.data
    for polygon in mesh.polygons:
        for v in selected_verts:
            for i, index in enumerate(polygon.vertices):
                z = mesh.vertices[index].co.z
                color = (z - min_z) / diff
                if v.index == index:
                    loop_index = polygon.loop_indices[i]
                    print(mesh.vertex_colors.active.data[loop_index].color)
#                    mesh.vertex_colors.active.data[loop_index].color = color

