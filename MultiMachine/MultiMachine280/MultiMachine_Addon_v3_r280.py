# 20190101 - Bpy2.8 upgrade
#
# ToDo:
# - clean up menu layout - box and divide like old
# - make execute work? go back to original version without F6?
# - Add Tetra code

bl_info = {
    "name" : "Multi_Machine_280",
    "description": "Set of tools to: 1) Do boolean differences or unions on an target using an object (tool) in a parameter driven pattern (rotate or slide). 2) Create Tetrahedron or Tetrahedron sections mesh objects to scene ",
    "author": "DSchwant",
    "blender": (2, 80, 0),
    "version": (0,0,-1.10),
    "location": "View3D",
    "category" : "Object"
}

# LOAD MODUL #    
import bpy

from bpy import *
from bpy.props import *
from bpy.props import EnumProperty, IntProperty, FloatProperty, BoolProperty, StringProperty

from bpy.types import WindowManager
from bpy.types import Scene
from bpy.types import Panel
from bpy.types import Menu
from bpy.types import Operator
from bpy.types import PropertyGroup
from bpy.types import AddonPreferences

import math
from math import radians
from mathutils import Vector, Euler
import os

## Interface objects and properties
bpy.types.Scene.Target = PointerProperty(type=bpy.types.Object)
bpy.types.Scene.Tool = PointerProperty(type=bpy.types.Object)
Scene.MMAction = EnumProperty(items=(('Diff', "Diff", "Do Boolean Difference"),
                    ('Union', "Union", "Do Boolean Union")),						
                name="Should the tool boolean diff or boolean union?",
                default = 'Diff',
                description="Action for the MultiBool Machine.")
Scene.MMMove = EnumProperty(items=(('Slide', "Slide", "Slide the target on the axis"),
                    ('Rotate', "Rotate", "Rotate the target on the axis")),
                name="Movement for the tooling",
                default = 'Rotate',
                description="What action should happen in the machining sequence.")
Scene.MMToolXVal = FloatProperty(name='MMToolXVal', default = 0, min=-100000, max=100000, precision=5, description="Number of degrees or units to move target on X axis.")
Scene.MMToolYVal = FloatProperty(name='MMToolYVal', default = 0, min=-100000, max=100000, precision=5, description="Number of degrees or units to move target on Y axis.")
Scene.MMToolZVal = FloatProperty(name='MMToolZVal', default = 0, min=-100000, max=100000, precision=5, description="Number of degrees or units to move target on Z axis.")
Scene.NumSteps = IntProperty(name='Number of Steps', min=1, max=10000, description="Number tooling steps to take.")
Scene.StartSteps = IntProperty(name='Step to start tooling', min=0, max=10000, description="The step at which to start tooling (current location is zero).")


Scene.MMPreStep = EnumProperty(items=(('None', "None", "No Pre-step"),
                    ('Slide', "Slide", "Slide the target on the axis"),
                    ('Rotate', "Rotate", "Rotate the target on the axis")),
                name="MMPreStep",
                default = 'None',
                description="Movement for the Pre-step (done once before each tooling step sequence).")
Scene.MMPreStepXVal = FloatProperty(name='MMPreStepXVal', default = 0, min=-100000, max=100000, precision=5, description="Number of degrees or units to move target on X axis in pre-step.")
Scene.MMPreStepYVal = FloatProperty(name='MMPreStepYVal', default = 0, min=-100000, max=100000, precision=5, description="Number of degrees or units to move target on Y axis in pre-step..")
Scene.MMPreStepZVal = FloatProperty(name='MMPreStepZVal', default = 0, min=-100000, max=100000, precision=5, description="Number of degrees or units to move target on Z axis in pre-step..")

Scene.RepeaterCnt = IntProperty(name='RepeaterCnt', min=1, max=1000, description="Number of times to repeat the pre-step and tooling sequence.", default = 1)

Scene.ReturnToLoc =  BoolProperty(name='ReturnToLoc', default = True)

# PANEL #
class MM_PT_panel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "MultiBool"
    ##bl_idname = "VIEW_3D_TOOLS_Multi_Machine_v3_r280"
    bl_category = "MM"
    bl_context = "objectmode"

    def draw(self, context):
        global custom_icons;

        layout = self.layout
        scene = context.scene
        
        row = layout.row()
        layout.prop_search(scene, "Target", scene, "objects")
        row = layout.row()
        row.prop_search(scene, "Tool", scene, "objects")
        row = layout.row()
        row.prop(scene, "MMAction", text="Action")
        row = layout.row()
        row.prop(scene, "MMMove", text="Move")
        row = layout.row()
        row.prop(scene, "MMToolXVal", text="X")
        row = layout.row()
        row.prop(scene, "MMToolYVal", text="Y")
        row = layout.row()
        row.prop(scene, "MMToolZVal", text="Z")
        row = layout.row()
        row.prop(scene, "NumSteps", text="Num. Steps")
        row = layout.row()
        row.prop(scene, "StartSteps", text="Start at Step")
        
        row = layout.row()
        row.prop(scene, "MMPreStep", text="Pre-Move")
        row = layout.row()
        row.prop(scene, "MMPreStepXVal", text="X")
        row = layout.row()
        row.prop(scene, "MMPreStepYVal", text="Y")
        row = layout.row()
        row.prop(scene, "MMPreStepZVal", text="Z")
      
        row = layout.row()
        row.prop(scene, "RepeaterCnt", text="Sequence Repeat")
        row = layout.row()
        row.prop(scene, "ReturnToLoc", text="Return To Start")
        row = layout.row()
        row.operator("tool.exec", text="Execute")

# OPERATOR #
class MM_OT_execButton(Operator):
    bl_idname = "tool.exec"
    bl_label = "Make It So"
    #bl_options = {'REGISTER', 'UNDO'} 

    def execute(self, context):
        os.system("cls")
        vars = context.scene
        target = bpy.data.objects[vars.Target.name]
        tool = bpy.data.objects[vars.Tool.name]
        orig_Euler = target.rotation_euler
        orig_Location = target.location
        print('target: ', target)
        print('tool: ', tool)
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
                target.select_set(True)
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
            
        if self.bpSP == '':
            print('Done')
        else:
            print("Don't Make Cuts from %s!" % self.bpSP)
        return {"FINISHED"}


# RESET #
class MM_OT_resetButton(Operator):
    bl_idname = "reset.exec"
    bl_label = "Reset values"
    bl_options = {'REGISTER', 'UNDO'}
 
    bpSPRS : StringProperty()

    def execute(self, context):

        resetVars.Target = ""
        resetVars.Tool = ""
        resetVars.MMAction = "None"
        resetVars.MMPreStep = "None"
        resetVars.MMToolXVal = 0
        resetVars.MMToolYVal = 0
        resetVars.MMToolZVal = 0
        resetVars.NumSteps = 0
        resetVars.StartSteps = 0
        resetVars.MMPreStepXVal = 0
        resetVars.MMPreStepYVal = 0
        resetVars.MMPreStepZVal = 0
        resetVars.RepeaterCnt = 0
        resetVars.ReturnToLoc = True
            
        if self.bpSPRS == '':
            print('Done')
        else:
            print("Don't Make Cuts from %s!" % self.bpSPRS)
        return {"FINISHED"}

classes = ( MM_PT_panel, MM_OT_execButton, MM_OT_resetButton )

register, unregister = bpy.utils.register_classes_factory(classes)
    
if __name__ == "__main__":
    register()