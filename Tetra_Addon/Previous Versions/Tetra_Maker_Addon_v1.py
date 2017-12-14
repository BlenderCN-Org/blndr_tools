######################################################
# Originally from https://en.wikibooks.org/wiki/Blender_3D:_Noob_to_Pro/Advanced_Tutorials/Python_Scripting/Addon_User_Interface
# To Do:
# - document
# - 
######################################################

bl_info = {
	"name": "Add_Mesh_Tetrahedron",
	"author": "DS",
	"version": (0,0,1),
	"description": "Adds tetrahedron",
	"location": "View3D > Tool Shelf > Create",
	"warning": "",
	"category": "Object"}

import bpy
from bpy.types import Scene
from bpy.props import IntProperty

import math
from math import sqrt

class TetrahedronMakerPanel(bpy.types.Panel):
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"
	bl_context = "objectmode"
	bl_category = "Create"
	bl_label = "Add Tetrahedron"
	
	def draw(self, context):
		layout = self.layout
		scene = context.scene
		box = layout.box()
		row = box.row()
		row.prop(scene, "sideLen", text="Length of Edge")
		row = box.row(False)
		row.operator("mesh.make_tetrahedron", text="Add Tetrahedron")
	#end draw
#end TetrahedronMakerPanel

class MakeTetrahedron(bpy.types.Operator):
	bl_idname = "mesh.make_tetrahedron"
	bl_label = "Add Tetrahedron"
	bl_options = {"UNDO"}
	
	def execute(self, context):
		vars = context.scene
		rad1Val = vars.sideLen / sqrt(3)
		depthVal = vars.sideLen * sqrt(2/3)
		bpy.ops.mesh.primitive_cone_add(vertices=3, radius1=rad1Val, radius2=0, depth=depthVal)
		bpy.context.active_object.name = "tetra_"+str(vars.sideLen)
		return {"FINISHED"}
	#end invoke
#end MakeTetrahedron

def register():
	bpy.utils.register_class(MakeTetrahedron)
	bpy.utils.register_class(TetrahedronMakerPanel)
	Scene.sideLen = IntProperty(name='Length of Edge', min=1, max=300, description="Length of Edge.")

def unregister():
	bpy.utils.register_class(MakeTetrahedron)
	bpy.utils.register_class(TetrahedronMakerPanel)
	del bpy.types.Object.sideLen

if __name__ == "__main__":
	register()