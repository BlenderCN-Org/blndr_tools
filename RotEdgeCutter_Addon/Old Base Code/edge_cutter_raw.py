##############################
# 
# - Start with a fresh file with no objects
# - Open the Console in place of the timeline on the bottom of the screen
# - Shift-A a cylinder and make it location 0,0,0 and dimensions 1,1,.5 and rename it "Coin_Main"
# - Shift-A a 2nd cylinder and make it location 0,-0.505,0 and dimensions .035,.035,1 and rename it "Edge_Cutter"
# - Paste this script into the Console and press return on line with no tab
# 
##############################

x=0
coin = bpy.data.objects["Coin_Main"]
cutter = bpy.data.objects["Edge_Cutter"]

for i in range(0, 119):
	coin.rotation_euler = (0,0,x)
	bpy.ops.object.select_all(action='DESELECT')
	coin.select = True
	bpy.context.scene.objects.active = coin
	bpy.ops.object.modifier_add(type='BOOLEAN')
	mod = coin.modifiers
	mod[0].name = "CutEdge"
	mod[0].operation = 'DIFFERENCE'
	mod[0].object = cutter
	bpy.ops.object.modifier_apply(apply_as='DATA', modifier=mod[0].name)
	x=x+0.0528 ### + 3.025 deg in radians???
	i += 1