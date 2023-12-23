def cleanup_mesh_objects():
    """
    Deletes all mesh objects in the current scene.
    """
    # Switch to object mode
    if bpy.context.active_object and bpy.context.active_object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    # Iterate over all objects in the scene
    meshes_to_delete = [obj for obj in bpy.data.objects if obj.type == 'MESH']

    # Check if there are any mesh objects to delete
    if meshes_to_delete:
        # Deselect all objects
        bpy.ops.object.select_all(action='DESELECT')

        # Select mesh objects
        for mesh in meshes_to_delete:
            mesh.select_set(True)

        # Delete the selected objects
        bpy.ops.object.delete() 
    else:
        print("No mesh objects found to delete.")
