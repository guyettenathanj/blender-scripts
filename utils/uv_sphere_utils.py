import bpy
import bmesh


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
        
        

def create_uv_sphere(location, radius, segments, rings):
    """
    Creates a UV sphere at a given location with specified radius, segments, and rings.
    
    :param location: Tuple specifying the location of the sphere.
    :param radius: Radius of the sphere.
    :param segments: Number of segments (longitude).
    :param rings: Number of rings (latitude).
    """
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, segments=segments, ring_count=rings, location=location)
    return bpy.context.active_object

def select_poles_of_uv_sphere(sphere):
    """
    Selects the top and bottom vertices (poles) of a UV sphere. and leaves it in edit mode.
    This currently ONLY works if the sphere hasn't been rotated and is lined up perfectly.

    :param sphere: The UV sphere object to modify. Must be of type 'MESH'.
    """
    if sphere.type != 'MESH':
        raise ValueError("Provided object is not a mesh")

    # Switch to edit mode
    bpy.ops.object.mode_set(mode='EDIT')

    # Get bmesh representation
    bm = bmesh.from_edit_mesh(sphere.data)
    bm.verts.ensure_lookup_table()

    # Initialize min and max z values and corresponding vertices
    max_z = min_z = bm.verts[0].co.z
    top_vert = bottom_vert = bm.verts[0]

    # Find the top and bottom vertices
    for vert in bm.verts:
        if vert.co.z > max_z:
            max_z = vert.co.z
            top_vert = vert
        elif vert.co.z < min_z:
            min_z = vert.co.z
            bottom_vert = vert

    # Deselect all vertices
    bpy.ops.mesh.select_all(action='DESELECT')

    # Select the top and bottom vertices
    top_vert.select = True
    bottom_vert.select = True

    # Update the mesh
    bmesh.update_edit_mesh(sphere.data)




# Reset the scene using cleanup function/s
cleanup_mesh_objects()

# Parameters for the sphere
location = (0, 0, 0)
radius = 1
segments = 20  # Adjust this value for horizontal subdivisions
rings = 5    # Adjust this value for vertical subdivisions

# Create a UV sphere
created_sphere = create_uv_sphere(location, radius, segments, rings)

# Get the poles in edit mode... 
select_poles_of_uv_sphere(created_sphere)
