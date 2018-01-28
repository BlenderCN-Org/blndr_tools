bpy.ops.mesh.dissolve_mode(use_verts=True)
bpy.ops.mesh.select_all(action='TOGGLE')
bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
bpy.ops.mesh.select_all(action='TOGGLE')

