######################################################
# Originally from https://en.wikibooks.org/wiki/Blender_3D:_Noob_to_Pro/Advanced_Tutorials/Python_Scripting/Addon_User_Interface
# To Do:
# - document
# - 
######################################################

bl_info = {
    "name": "Add_Mesh_Tetrahedron_v2",
    "author": "DS",
    "version": (0,0,1),
    "description": "Adds tetrahedron",
    "location": "View3D > Tool Shelf > Tetra",
    "warning": "",
    "category": "Object"}

import bpy
from bpy.types import Scene
from bpy.props import IntProperty, BoolProperty

import math
from math import sqrt
from mathutils import Vector

class TetrahedronMakerPanel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_category = "Tetra"
    bl_label = "Add Tetrahedron"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        box = layout.box()
        row = box.row()
        row.prop(scene, "sideLen", text="Length of Edge")
        row = box.row()
        row.prop(scene, "faceOnly", text="Face Only?")
        row = box.row()
        row.prop(scene, "centerOnPlane", text="Center on Plane?")
        row = box.row(False)
        row.operator("mesh.make_tetrahedron", text="Add Tetrahedron")

class MakeTetrahedron(bpy.types.Operator):
    bl_idname = "mesh.make_tetrahedron"
    bl_label = "Add Tetrahedron"
    bl_options = {"UNDO"}
    
    def execute(self, context):
        vars = context.scene
        rad1Val = vars.sideLen / sqrt(3)
        if (vars.faceOnly == True):
            depthVal = vars.sideLen / 12 * sqrt(6)
            objName = "tetra_face_"
            centerZ = (vars.sideLen / 12 * sqrt(6))/4
        else:
            depthVal = vars.sideLen / 3 * sqrt(6)
            objName = "tetra_"
            centerZ = vars.sideLen / 12 * sqrt(6)
        bpy.ops.mesh.primitive_cone_add(vertices=3, radius1=rad1Val, radius2=0, depth=depthVal)
        bpy.context.active_object.name = objName+str(vars.sideLen)
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
        if (vars.centerOnPlane == True):
            bpy.context.active_object.location = Vector((0,0,centerZ))


        return {"FINISHED"}

def register():
    bpy.utils.register_class(MakeTetrahedron)
    bpy.utils.register_class(TetrahedronMakerPanel)
    Scene.sideLen = IntProperty(name='Length of Edge', min=1, max=300, description="Length of Edge.")
    Scene.faceOnly = BoolProperty(name='Face Only?', default= False, description="Do you want to generate only one of the 4 faces?")
    Scene.centerOnPlane = BoolProperty(name='Face Only?', default= False, description="Do you want to generate only one of the 4 faces?")

def unregister():
    bpy.utils.unregister_class(MakeTetrahedron)
    bpy.utils.unregister_class(TetrahedronMakerPanel)

if __name__ == "__main__":
    register()