######################################################
# Still to do:
# - internal documentation
# - video and samples
# - Add Reset
######################################################

bl_info = {
	"name": "Multi_Machine_v3",
	"author": "DS",
	"version": (0,0,1),
	"description": "Does boolean differences or unions on an target using an object (tool) in a parameter driven pattern (rotate or slide).",
	"location": "View3D > Tool Shelf > MultiMachine",
	"warning": "",
	"category": "Object"}
	
import bpy
import math
from bpy.types import Scene
from bpy.props import EnumProperty, IntProperty, FloatProperty, BoolProperty
from math import radians
from mathutils import Vector, Euler
import os

class ToolsPanel(bpy.types.Panel):
	bl_label = "Multi Machine"
	bl_idname = "VIEW_3D_TOOLS_Multi_Machine_v3"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"
	bl_category = "MM3"
	bl_context = "objectmode"

	def draw(self, context):
		layout = self.layout
		scene = context.scene

		box = layout.box()
		row = box.row()
		row.prop_search(scene, "Target", bpy.data, "objects",icon="TRIA_DOWN")
		row = box.row()
		row.prop_search(scene, "Tool", bpy.data, "objects",icon="TRIA_DOWN")
		row = box.row()
		row.prop(scene, "MMAction", text="Action")
		row = box.row()
		row.prop(scene, "MMMove", text="Move")
		row = box.row()
		row.prop(scene, "MMToolXVal", text="X")
		row = box.row()
		row.prop(scene, "MMToolYVal", text="Y")
		row = box.row()
		row.prop(scene, "MMToolZVal", text="Z")
		row = box.row()
		row.prop(scene, "NumSteps", text="Num. Steps")
		row = box.row()
		row.prop(scene, "StartSteps", text="Start at Step")

		box = layout.box()
		row = box.row()
		row.prop(scene, "MMPreStep", text="Pre-Move")
		row = box.row()
		row.prop(scene, "MMPreStepXVal", text="X")
		row = box.row()
		row.prop(scene, "MMPreStepYVal", text="Y")
		row = box.row()
		row.prop(scene, "MMPreStepZVal", text="Z")
		row = box.row()

		box = layout.box() 
		row = box.row()
		row.prop(scene, "RepeaterCnt", text="Repeat")
		row = box.row()
		row.prop(scene, "ReturnToLoc", text="ReturnToLoc")
		row = box.row()
		row.operator("tool.exec", text="Execute")
# End class ToolsPanel
	
class mmtoolButton(bpy.types.Operator):
	bl_idname = "tool.exec"
	bl_label = "Make Diff or Union"
	country = bpy.props.StringProperty()
	
	def execute(self, context):
		os.system("cls")
		vars = context.scene
		target = bpy.data.objects[vars.Target]
		tool = bpy.data.objects[vars.Tool]
		orig_Euler = target.rotation_euler
		orig_Location = target.location
		print('RTL: ', vars.ReturnToLoc)
		print(orig_Euler)
		print(orig_Location)
		return2_eul = rot_eul = [orig_Euler[0],orig_Euler[1],orig_Euler[2]]
		return2_loc = slide_loc = [orig_Location[0],orig_Location[1],orig_Location[2]]
		toolRotRads = [radians(vars.MMToolXVal),radians(vars.MMToolYVal),radians(vars.MMToolZVal)]
		toolSlideUnits = [vars.MMToolXVal,vars.MMToolYVal,vars.MMToolZVal]
		prestepRotRads = [radians(vars.MMPreStepXVal),radians(vars.MMPreStepYVal),radians(vars.MMPreStepZVal)]
		prestepSlideUnits = [vars.MMPreStepXVal,vars.MMPreStepYVal,vars.MMPreStepZVal]

		# print('orig: ',orig_Euler,orig_Location)
		# print('rot and slide: ',rot_eul,slide_loc)
		# print('tool: ',toolRotRads,toolSlideUnits)
		# print('pre: ',prestepRotRads,prestepSlideUnits)
		
		for r in range(vars.RepeaterCnt):
			# print ('rep_cnt: ',r)
			if (vars.MMPreStep =='Rotate'):
				rot_eul = Euler([sum(e) for e in zip(rot_eul, prestepRotRads)], "XYZ")
				target.rotation_euler = rot_eul
			elif (vars.MMPreStep =='Slide'):
				slide_loc = Vector([sum(v) for v in zip(slide_loc, prestepSlideUnits)])
				target.location = slide_loc
			
			# print('rot slide: ',rot_eul,slide_loc)
			
			for i in range(vars.NumSteps+1):
				# print('step: ',i)
				if (i > 0 ):
					if (vars.MMMove == 'Rotate'):
						rot_eul = Euler([sum(z) for z in zip(rot_eul, toolRotRads)], "XYZ")
					else: # Assumes 'Slide'
						slide_loc = Vector([sum(z) for z in zip(slide_loc, toolSlideUnits)])

				# At step 0 these are the original euler\location (or location after pre-step), else the eul\loc just set
				target.rotation_euler = rot_eul 
				target.location = slide_loc
				bpy.ops.object.select_all(action='DESELECT')
				target.select = True
				bpy.context.scene.objects.active = target
				
				if (i >= vars.StartSteps): # Execute tool action at this step
					bpy.ops.object.modifier_add(type='BOOLEAN')
					mod = target.modifiers
					mod[0].name = "MMTool"
					if (vars.MMAction == 'Diff'):
						# print('diff: ',rot_eul, slide_loc)
						mod[0].operation = 'DIFFERENCE'
					else: # Assumes 'Union'
						# print('union: ',rot_eul, slide_loc)
						mod[0].operation = 'UNION'
					if (vars.MMAction != 'None'):
						mod[0].object = tool
						bpy.ops.object.modifier_apply(apply_as='DATA', modifier=mod[0].name)
					
				i += 1
			r += 1
			
		if (vars.ReturnToLoc == True):
			print('Return!!!: ', return2_eul, return2_loc)
			target.rotation_euler = return2_eul
			target.location = return2_loc
			
		if self.country == '':
			print('Done')
		else:
			print("Don't Make Cuts from %s!" % self.country)
		return {"FINISHED"}
# End class mmtoolButton

def register():
	bpy.utils.register_class(ToolsPanel)
	bpy.utils.register_class(mmtoolButton)
	Scene.Target = bpy.props.StringProperty()
	Scene.Tool = bpy.props.StringProperty()
	Scene.MMAction = EnumProperty(items=(('None', "None", "No tooling"),
						('Diff', "Diff", "Do Boolean Difference"),
						('Union', "Union", "Do Boolean Union")),						
					name="MMAction",
					default = 'Diff',
					description="Action for the Multi Machine.")
	Scene.MMMove = EnumProperty(items=(('Slide', "Slide", "Slide the target on the axis"),
						('Rotate', "Rotate", "Rotate the target on the axis")),
					name="MMMove",
					default = 'Rotate',
					description="What action should happen in the machining sequence.")
	Scene.MMToolXVal = FloatProperty(name='MMToolXVal', default = 0, min=-100000, max=100000, precision=5, description="Number of degrees or units to move target on X axis.")
	Scene.MMToolYVal = FloatProperty(name='MMToolYVal', default = 0, min=-100000, max=100000, precision=5, description="Number of degrees or units to move target on Y axis.")
	Scene.MMToolZVal = FloatProperty(name='MMToolZVal', default = 0, min=-100000, max=100000, precision=5, description="Number of degrees or units to move target on Z axis.")
	Scene.NumSteps = IntProperty(name='NumSteps', min=1, max=10000, description="Number tooling steps to take.")
	Scene.StartSteps = IntProperty(name='StartSteps', min=0, max=10000, description="The step at which to start tooling (current location is zero).")
	Scene.MMPreStep = EnumProperty(items=(('None', "None", "No Pre-step"),
						('Slide', "Slide", "Slide the target on the axis"),
						('Rotate', "Rotate", "Rotate the target on the axis")),
					name="MMPreStep",
					default = 'None',
					description="Movement for the Pre-step (done once before each tooling sequence).")
	Scene.MMPreStepXVal = FloatProperty(name='MMPreStepXVal', default = 0, min=-100000, max=100000, precision=5, description="Number of degrees or units to move target on X axis in pre-step.")
	Scene.MMPreStepYVal = FloatProperty(name='MMPreStepYVal', default = 0, min=-100000, max=100000, precision=5, description="Number of degrees or units to move target on Y axis in pre-step..")
	Scene.MMPreStepZVal = FloatProperty(name='MMPreStepZVal', default = 0, min=-100000, max=100000, precision=5, description="Number of degrees or units to move target on Z axis in pre-step..")
	Scene.RepeaterCnt = IntProperty(name='RepeaterCnt', min=1, max=1000, description="Number of times to repeat the pre-step and tooling sequence.", default = 1)
	Scene.ReturnToLoc = BoolProperty(name='ReturnToLoc')

def unregister():
	bpy.utils.unregister_class(ToolsPanel)
	bpy.utils.unregister_class(mmtoolButton)

if __name__ == "__main__":
	register()