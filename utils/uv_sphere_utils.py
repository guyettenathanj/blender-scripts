import bpy
import bmesh

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
segments = 200  # Adjust this value for horizontal subdivisions
rings = 200    # Adjust this value for vertical subdivisions

# Create a UV sphere
created_sphere = create_uv_sphere(location, radius, segments, rings)

# Get the poles in edit mode... 
select_poles_of_uv_sphere(created_sphere)
