import bpy
from math import *

obj = bpy.context.active_object  # active object
mesh = obj.data
uvLayerNm = 'map3'
vtxColNm = 'outline_Col'
#vtxCol_width = 'Width_Col'
#vtxCol_pdo = 'Pdo_Col'

## create vertex color layer 'Width_Col' if not exist
#if mesh.vertex_colors.get(vtxCol_width) is None:
#    mesh.vertex_colors.new(name=vtxCol_width)

## create vertex color layer 'Width_Col' if not exist
#if mesh.vertex_colors.get(vtxCol_pdo) is None:
#    mesh.vertex_colors.new(name=vtxCol_pdo)

# create vertex color layer 'Width_Col' if not exist
if mesh.vertex_colors.get(vtxColNm) is None:
    mesh.vertex_colors.new(name=vtxColNm)

# create uv map layer if not exist
if mesh.uv_layers.get(uvLayerNm) is None:
    mesh.uv_layers.new(name=uvLayerNm)

src_uv = mesh.uv_layers[uvLayerNm]
dst_vcol = mesh.vertex_colors[vtxColNm]

def uvs_to_color(mesh, src_uv, dst_vcol, dst_u_idx=0, dst_v_idx=1):
    for loop_index, loop in enumerate(mesh.loops):
        c = dst_vcol.data[loop_index].color
        uv = src_uv.data[loop_index].uv
        c[dst_u_idx] = uv[0]
        c[dst_v_idx] = uv[1]
#        u = fmod(uv[0], 1.0)
#        v = fmod(uv[1], 1.0)
#        c[dst_u_idx] = u + 1.0 if u < 0 else u
#        c[dst_v_idx] = v + 1.0 if v < 0 else v

        dst_vcol.data[loop_index].color = c

    mesh.update()

uvs_to_color(mesh,src_uv,dst_vcol,dst_u_idx=0, dst_v_idx=1)