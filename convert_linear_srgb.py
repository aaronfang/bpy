import bpy

def s2lin1(x):
    
    a = 0.055
    if x <= 0.04045 :
        y = x * (1.0 / 12.92)  
    elif  0.04045 < x <= 1 : 
        y =  ((x+0.055)/1.055)**2.4
    
    return y

def lin2s1(x):
    
    a = 0.055
    if x <=0.0031308:
        y = x * 12.92
    elif 0.0031308 < x <= 1 :
        y = 1.055*x**(1/2.4) - 0.055
    
    return y

def convert_Linear_sRGB():
    
    objs = bpy.context.selected_objects

    for obj in objs:
        mesh = obj.data
        color_loops = mesh.vertex_colors.active.data
        for c_loop in color_loops:
            fixed_colorR = lin2s1(c_loop.color[0])
            fixed_colorG = lin2s1(c_loop.color[1])
            fixed_colorB = lin2s1(c_loop.color[2])
            #print('source_col = ' + str(c_loop.color[0],c_loop.color[1],c_loop.color[2]) + ' ; target_col = ' + str(fixed_colorR,fixed_colorG,fixed_colorB))
            c_loop.color = [fixed_colorR, fixed_colorG, fixed_colorB, c_loop.color[3]]

def convert_sRGB_Linear():
    
    objs = bpy.context.selected_objects

    for obj in objs:
        mesh = obj.data
        color_loops = mesh.vertex_colors.active.data
        for c_loop in color_loops:
            fixed_colorR = s2lin1(c_loop.color[0])
            fixed_colorG = s2lin1(c_loop.color[1])
            fixed_colorB = s2lin1(c_loop.color[2])
            #print('source_col = ' + str(c_loop.color[0],c_loop.color[1],c_loop.color[2]) + ' ; target_col = ' + str(fixed_colorR,fixed_colorG,fixed_colorB))
            c_loop.color = [fixed_colorR, fixed_colorG, fixed_colorB, c_loop.color[3]]

convert_Linear_sRGB()