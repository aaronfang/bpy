	
	
# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# ##### END GPL LICENSE BLOCK #####
	
	
	
"""



by  Rickyblender 
on blendernaton forum

feedback from Padone

Thread  in pythpn forum

http://blenderartists.org/forum/showthread.php?360140-help-please-is-there-a-fast-way-to-convert-srgb-values-to-linear&p=2802920#post2802920

"""
	
	
	
import bpy,bmesh
from bpy.props import *
from mathutils import *
from math import *
	
from time import time

last_menu1 = 'None'
	
	
# Ckeck Box Properties
	
	
# Float Numbers Properties
	

#####
	
	
	
	
class Panelsimple1(bpy.types.Panel):						# This is the panel
	
	'''Panel'''
	
	bl_label = "Remove Doubles / Merge"							# Header Panel's  name
	bl_space_type = "VIEW_3D"							# in 3D view
#   bl_region_type = "TOOLS"							# in tool shelf
	bl_region_type = "TOOL_PROPS"  
	bl_show_header=True  
	
	
	#   http://www.blender.org/documentation/250PythonDoc/bpy.types.Panel.html#bpy.types.Panel
	
	def draw(self, context):
	
		global last_menu1							  # Access global Var to find the last operation
	
		layout = self.layout
		scene = context.scene
	
		col = layout.column()
#		col.label(' menu color shade:', 'LAMP_DATA')
	
	
	
	# First  Operator
#		col.operator_menu_enum('view_3d.my_color1', 'colormenu1', 'Menu Selection')
	
																		# Here the operator menu is displayed
																		# 'view_3d.my_color1' is the bl_idname of the operator called
	
		col.label(' Selection : ' + last_menu1, 'QUESTION')
#		print ('in draw   ies panel  colormenu1 =',last_menu1,' Val =',eval(last_menu1))
	
		colorselect=""
	
		if eval(last_menu1)==1:
	
			colorselect="sRGB"
#			col.label('First point', 'FCURVE')
	
			print ('selected sRGB')
	
		elif eval(last_menu1)==2:
	
			colorselect="Linear"
#			col.label('Middle Point', 'PARTICLE_DATA')
	
	
	
	
####
	
	
	
#		print (' Color selection =',colorselect)
	
		col.separator()
		Txcolor=colorselect+ ' Color selected'
	
		col.label(Txcolor, 'WIRE')
	
		subtype ='PERCENTAGE'

		col.separator()
	
	
	
	
	
		layout.operator("custom.button1")
	
	
		layout.operator("custom.button2")
	
	
	
	
	
#####
	
	
class FIRSTOperator(bpy.types.Operator):					# When an option in the operator menu is clicked, this is called
	
	'''Operator'''
	bl_idname = 'view_3d.my_color1'
	bl_label = 'Operator'
	
	# Define possible operations
	
	colormenu1 = EnumProperty(items=(
		('1', 'sRGB-Linear', 'The first item'),
		('2', 'Linear-sRGB', 'The second item')
											))
	
	
	
	@classmethod
	def poll(cls, context):
		return context.object is not None
	
	
	def execute(self, context):
	
		global last_menu1										# Access global Var so we can later draw it in the panel
	
		last_menu1 = self.properties.colormenu1					# Store the choosen operation / Selection
		print ('selection   shade=',self.properties.colormenu1[0])
	
	
	
	
	
	
	
		if last_menu1=="1":
	
			print ()
			print (' operator  BL  Diffuse  SRGB  to Linear  1')
	

	
	
		elif last_menu1=="2":
	
	
	
			print (' operator  BL  Diffuse  Linear to   SRGB 2')
	

	
		return {'FINISHED'}
	
#####
	
	
	
	
###
	
	
#	http://entropymine.com/imageworsener/srgbformula/
	
def s2lin1(x):
	
	a = 0.055
	if x <= 0.04045 :
		y = x * (1.0 / 12.92)  
	elif  0.04045 < x <= 1 : 
		y =  ((x+0.055)/1.055)**2.4
	
	return y
	
###

#x = 0.1
	
#z = s2lin1(x)
	
	
#print ('Linear RGB  to   S RGB')
#print ()
	
###
	
	
def lin2s1(x):
	
	a = 0.055
	if x <=0.0031308:
		y = x * 12.92
	elif 0.0031308 < x <= 1 :
		y = 1.055*x**(1/2.4) - 0.055
	
	return y
	
###
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
#####
	
#Custom Button	
	
	
class custombutton1(bpy.types.Operator):
	
	bl_idname = "custom.button1"
	bl_label = "convert sRGB colors"
	__doc__ = "Simple convert sRGB colors"
	
	def invoke(self, context, event):
	
													# when the button is press it prints this to the log / Console
		print("  ####################  ")
		print("convert sRGB colors1")
		print (' $$$$$$$$$$$$$ convert sRGB colors    **************************')
		print("  ####################  ")
	
		global  last_menu1
	
		context = bpy.context
	
		mesh_objs = [ob for ob in context.selected_objects if ob.type == 'MESH']
	
	
		begin = time()
#		print('Start Time in seconds =', begin)
	
	
		print ()
		print (' operator  BL  Diffuse  SRGB  to Linear  1')
	
	
		for mesh in mesh_objs:
	
			print('repr =',repr(mesh))
	
			print("active_slot:", mesh.active_material_index)
			print ()
	
			if mesh.active_material is not None:
				print("active_material:", mesh.active_material.name)
	
			for i, mat in enumerate(mesh.material_slots):
#				print (' dir mat =', dir(mat ))
				if not i:
					print("material_slots")
				if mat is not None:
					print("\t[%d] = %s" % (i, mat.name))
#					print ('material = ', mat.material)
					
#					print (' dir mat =', dir(mat ))
#					print("\t[%d] = %s Diff color = %f" % (i, mat.name,mat.))
	
	
					for item in bpy.data.materials:
						if item.name == mat.name:
							nred1 = s2lin1(item.diffuse_color[0])
							ngreen1 = s2lin1(item.diffuse_color[1])
							nblue1 = s2lin1(item.diffuse_color[2])
							newcol = (( nred1 ,ngreen1 , nblue1 ))
							newcol = (( nred1 ,ngreen1 , nblue1 ))
							print ('old Red =',item.diffuse_color[0],' New Red =', nred1 ,'name =',item.name)
							item.diffuse_color = newcol
	
	
				else:
	
					print("\t[%d] is None" % i)
	
	
	
	
			print()
	
	
	
	
	# P 41  53 65
	
		end = time()
	
		print ()
		print('Execution took : ', time()-begin, 'seconds')
		print ()
	
	
	
		return{'FINISHED'}    
	
###
	
	
	
	
####
	
#Custom Button2
	
	
class custombutton2(bpy.types.Operator):
	
	bl_idname = "custom.button2"
	bl_label = "convert Lin colors"
	__doc__ = "Simple convert Lin colors"
	
	def invoke(self, context, event):
	
													# when the button is press it prints this to the log / Console
		print("  ####################  ")
		print("convert lin colors 2")
		print (' $$$$$$$$$$$$$ convert sRGB colors    **************************')
		print("  ####################  ")
	
		global  last_menu1
	
		context = bpy.context
	
		mesh_objs = [ob for ob in context.selected_objects if ob.type == 'MESH']
	
	
	
	# P 41  53 65
	
	
	
	
		begin = time()
#			print('Start Time in seconds =', begin)
	
		for mesh in mesh_objs:
	
			print('repr =',repr(mesh))
	
			print("active_slot:", mesh.active_material_index)
			print ()
	
			if mesh.active_material is not None:
				print("active_material:", mesh.active_material.name)
	
			for i, mat in enumerate(mesh.material_slots):
#				print (' dir mat =', dir(mat ))
				if not i:
					print("material_slots")
				if mat is not None:
					print("\t[%d] = %s" % (i, mat.name))
	
					for item in bpy.data.materials:
					
						if item.name == mat.name:
	
							print (item.name,' RGB =',item.diffuse_color)
							nred1 = lin2s1(item.diffuse_color[0])
							ngreen1 = lin2s1(item.diffuse_color[1])
							nblue1 = lin2s1(item.diffuse_color[2])
							newcol = (( nred1 ,ngreen1 , nblue1 ))
		#					print ('old Red =',item.diffuse_color[0],' New Red =', nred1 )
							print ('New SRGB =',newcol )
	
							item.diffuse_color = newcol
	
	
	
	
	
		end = time()
	
		print ()
		print('Execution took : ', time()-begin, 'seconds')
		print ()
	
	
	
	
	
		return{'FINISHED'}    
	
###
	
	
	
	
	
	
	
	
	
	
	
	
	
	
###
	
def register():
	bpy.utils.register_module(__name__)
	
	
def unregister():
	bpy.utils.unregister_module(__name__)
	
	
	
if __name__ == "__main__":
	register()
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	