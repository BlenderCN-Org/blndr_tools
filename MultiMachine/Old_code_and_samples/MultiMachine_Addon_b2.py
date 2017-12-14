######################################################
# Still to do:
# - internal documentation
# - Take out debug prints to console
# - Add repeater
######################################################

bl_info = {
	"name": "Multi_Machine",
	"author": "DS",
	"version": (0,0,1),
	"description": "Does boolean differences or unions on an target using an object (tool) in a parameter driven pattern (rotate or slide).",
	"location": "View3D > Tool Shelf > MultiMachine",
	"warning": "",
	"category": "Object"}
	
import bpy
import math
from bpy.types import Scene
from bpy.props import EnumProperty, IntProperty, FloatProperty
from math import radians

class ToolsPanel(bpy.types.Panel):
	bl_label = "Multi Machine"
	bl_idname = "VIEW_3D_TOOLS_Multi_Machine"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"
	bl_category = "MM"
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
		row.prop(scene, "MMToolAxis", text="Axis")
		row = box.row()
		row.prop(scene, "NumSteps", text="Num. Steps")
		row = box.row()
		row.prop(scene, "NumUnits", text="Num. Units")
		row = box.row()
		row.prop(scene, "StartSteps", text="Start at Step")
		row = box.row()
		row.prop(scene, "LimSteps", text="Stop at Step")

		box = layout.box()
		box.label("Pre-step:")
		row = box.row()
		row.prop(scene, "MMPreStep", text="Move")
		row = box.row()
		row.prop(scene, "MMPreStepAxis", text="Axis")
		row = box.row()
		row.prop(scene, "PreStepDeg", text="Degrees")
		row = box.row()
		row.prop(scene, "PreStepUnits", text="Units")
		row = box.row()

		box = layout.box() #
		row = box.row()
		row.prop(scene, "RepeaterCnt", text="Repeat")
		row = box.row()
		row.operator("tool.exec", text="Execute")
# End class ToolsPanel
	
class mmtoolButton(bpy.types.Operator):
	bl_idname = "tool.exec"
	bl_label = "Make Diff or Union"
	country = bpy.props.StringProperty()
	
	def execute(self, context):
		vars = context.scene
		target = bpy.data.objects[vars.Target]
		tool = bpy.data.objects[vars.Tool]
		get_Euler = target.rotation_euler
		get_Location = target.location
		print(get_Euler)
		print(get_Location)
		rot_loc_X = get_Euler[0]
		rot_loc_Y = get_Euler[1]
		rot_loc_Z = get_Euler[2]
		slide_loc_X = get_Location[0]
		slide_loc_Y = get_Location[1]
		slide_loc_Z = get_Location[2]
		stepRads = radians(360 / vars.NumSteps)
		
		for r in range(0, vars.RepeaterCnt):
			if (vars.LimSteps > vars.NumSteps):
				vars.LimSteps = vars.NumSteps

			if (vars.MMPreStep =='Rotate'):
				if vars.MMPreStepAxis == 'X':
					rot_loc_X=rot_loc_X + radians(vars.PreStepDeg)
				elif vars.MMPreStepAxis == 'Y':
					rot_loc_Y=rot_loc_Y + radians(vars.PreStepDeg)
				else: # Assumes 'Z'
					rot_loc_Z=rot_loc_Z + radians(vars.PreStepDeg)
			elif (vars.MMPreStep =='Slide'):
				if vars.MMPreStepAxis == 'X':
					slide_loc_X=slide_loc_X + vars.PreStepUnits
				elif vars.MMPreStepAxis == 'Y':
					slide_loc_Y=slide_loc_Y + vars.PreStepUnits
				else: # Assumes 'Z'
					slide_loc_Z=slide_loc_Z + vars.PreStepUnits	
				
			for i in range(0, vars.LimSteps+1):
				target.rotation_euler = (rot_loc_X,rot_loc_Y,rot_loc_Z) # At step 0 this is the original location (or location after pre-step), else the location set at end of previous step
				target.location = (slide_loc_X,slide_loc_Y,slide_loc_Z)
				bpy.ops.object.select_all(action='DESELECT')
				target.select = True
				bpy.context.scene.objects.active = target
				
				if (i >= vars.StartSteps): # Execute tool action at this step
					bpy.ops.object.modifier_add(type='BOOLEAN')
					mod = target.modifiers
					mod[0].name = "MMTool"
					if (vars.MMAction == 'Diff'):
						mod[0].operation = 'DIFFERENCE'
					else: # Assumes 'Union
						mod[0].operation = 'UNION'
					mod[0].object = tool
					bpy.ops.object.modifier_apply(apply_as='DATA', modifier=mod[0].name)
					
				if (vars.MMMove == 'Rotate'):
					if vars.MMToolAxis == 'X':
						rot_loc_X=rot_loc_X + stepRads
					elif vars.MMToolAxis == 'Y':
						rot_loc_Y=rot_loc_Y + stepRads
					else: # Assumes 'Z'
						rot_loc_Z=rot_loc_Z + stepRads
				else: # Assumes 'Slide'
					if vars.MMToolAxis == 'X':
						slide_loc_X=slide_loc_X + vars.NumUnits
					elif vars.MMToolAxis == 'Y':
						slide_loc_Y=slide_loc_Y + vars.NumUnits
					else: # Assumes 'Z'
						slide_loc_Z=slide_loc_Z + vars.NumUnits
				i += 1
			r += 1
			
		if self.country == '':
			print(context.scene.Target)
			print(context.scene.Tool)
			print(context.scene.MMToolAxis)
			print(get_Euler)
			print(context.scene.NumSteps)
			print(context.scene.LimSteps)
			print("Execute")
		else:
			print("Don't Make Cuts from %s!" % self.country)
		return {"FINISHED"}
# End class ToolsPanel

def register():
	bpy.utils.register_class(ToolsPanel)
	bpy.utils.register_class(mmtoolButton)
	Scene.Target = bpy.props.StringProperty()
	Scene.Tool = bpy.props.StringProperty()
	Scene.MMAction = EnumProperty(items=(('Diff', "Diff", "Do Boolean Difference"),
						('Union', "Union", "Do Boolean Union")),						
					name="Should the tool boolean diff or boolean union?",
					default = 'Diff',
					description="Action for the Multi Machine.")
	Scene.MMMove = EnumProperty(items=(('Slide', "Slide", "Slide the target on the axis"),
						('Rotate', "Rotate", "Rotate the target on the axis")),
					name="Movement for the tooling",
					default = 'Rotate',
					description="What action should happen in the machining sequence.")
	Scene.MMToolAxis = EnumProperty(items=(('Z', "Z", "Rotate on Z axis"),
						('Y', "Y", "Rotate on Y axis"),
						('X', "X", "Rotate on X axis")),						
					name="Rotation Axis",
					default = 'Z',
					description="Axis on which to rotate Target for action.")
	Scene.MMPreStep = EnumProperty(items=(('None', "None", "No Pre-step"),
						('Slide', "Slide", "Slide the target on the axis"),
						('Rotate', "Rotate", "Rotate the target on the axis")),
					name="Movement for the Pre-step",
					default = 'None',
					description="What action should happen before the machining sequence.")
	Scene.MMPreStepAxis = EnumProperty(items=(('Z', "Z", "On Z axis"),
						('Y', "Y", "On Y axis"),
						('X', "X", "On X axis")),						
					name="Pre-step action axis",
					default = 'Z',
					description="Axis for the pre-step move.")
	Scene.NumSteps = IntProperty(name='Number of Steps', min=1, max=10000, description="Number steps to divide full 360deg rotation into.")
	Scene.NumUnits = FloatProperty(name='UnitsToSlide', min=-100000, max=100000, description="Number of units to slide target.")
	Scene.StartSteps = IntProperty(name='Step to start tooling', min=0, max=10000, description="The step at which to start tooling.")
	Scene.LimSteps = IntProperty(name='Limit number of Steps', min=0, max=10000, description="Number steps to stop at.")
	Scene.PreStepDeg = IntProperty(name='The degrees for the pre-step rotation', min=-360, max=360, description="The degrees for the pre-step rotation.")
	Scene.PreStepUnits = FloatProperty(name='The units for the pre-step slide', min=-100000, max=100000, description="The units for the pre-step slide.")
	Scene.RepeaterCnt = IntProperty(name='Number of times to repeat the machine sequence.', min=1, max=1000, description="The number of times to repeat the machine sequence.", default = 1)

def unregister():
	bpy.utils.unregister_class(ToolsPanel)
	bpy.utils.unregister_class(mmtoolButton)

if __name__ == "__main__":
	register()