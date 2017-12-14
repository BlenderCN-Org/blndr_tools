##############################
# 
# - Start with a fresh file with no objects
# - Open the Console in place of the timeline on the bottom of the screen
# - Shift-A a cylinder and make it location 0,0,0 and dimensions 1,1,.5 and rename it "Coin_Main"
# - Shift-A a 2nd cylinder and make it location 0,-0.505,0 and dimensions .035,.035,1 and rename it "Edge_Cutter"
# - Paste this script into the Console and press return on line with no tab
# 
##############################
import bpy
import math
from mathutils import Vector
from functools import reduce

bl_info = {
    "name": "Edge_Rotate_Cutter",
    "author": "DS",
    "version": (0,0,1),
    "description": "Does boolean difference on an object in circlular pattern",
    "location": "View3D > Tool Shelf > ERCutter",
    "warning": "",
    "category": "Object"}

#    def execute(self, context):
#        objs_to_move = [o for o in context.selected_objects if o != context.active_object]
#        for o in objs_to_move:
#        	align_faces(o, context.active_object)
#        return {'FINISHED'}

#x=0
#coin = bpy.data.objects["Coin_Main"]
#cutter = bpy.data.objects["Edge_Cutter"]

#for i in range(0, 119):
#	coin.rotation_euler = (0,0,x)
#	bpy.ops.object.select_all(action='DESELECT')
#	coin.select = True
#	bpy.context.scene.objects.active = coin
#	bpy.ops.object.modifier_add(type='BOOLEAN')
#	mod = coin.modifiers
#	mod[0].name = "CutEdge"
#	mod[0].operation = 'DIFFERENCE'
#	mod[0].object = cutter
#	bpy.ops.object.modifier_apply(apply_as='DATA', modifier=mod[0].name)
#	x=x+0.0528 ### + 3.025 deg in radians???
#	i += 1

class EdgeRotateCutter(bpy.types.Operator):
    """Edge Rotate Cutter"""
    bl_idname = "object.edge_rotate_cutter"
    bl_label = "Edge Rotate Cutter"
    bl_options = {'REGISTER', 'UNDO'}

    target_obj = bpy.props.IntProperty(name="Target", default=2, min=1, max=100)
    cutter_obj = bpy.props.IntProperty(name="Cutter", default=2, min=1, max=100)
    rot_axis = bpy.props.EnumProperty(items= (("X", "X", "", "", 0),    
                                           ("Y", "Y", "", "", 1),    
                                           ("Z", "Z", "", "", 2)) ,  
                                   name = "Rotation Axis:")
    num_rotations = bpy.props.IntProperty(name="Number_of_rotations", default=2, min=1, max=100)
    lim_cuts = bpy.props.IntProperty(name="Limit_to_steps", default=2, min=1, max=100)

    def execute(self, context):
        scene = context.scene
        cursor = scene.cursor_location
        obj = scene.objects.active

        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(EdgeRotateCutter.bl_idname)

# store keymaps here to access after registration
addon_keymaps = []

def register():
    bpy.utils.register_class(EdgeRotateCutter)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.utils.unregister_class(EdgeRotateCutter)
    bpy.types.VIEW3D_MT_object.remove(menu_func)

if __name__ == "__main__":
    register()