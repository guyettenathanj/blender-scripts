def cleanup_mesh_objects():
    # Switch to object mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    # Iterate over all objects in the scene
    for obj in bpy.data.objects:
        # Check if the object is a mesh
        if obj.type == 'MESH':
            # Select the mesh object
            obj.select_set(True)
            # Delete the selected object
            bpy.ops.object.delete() 
