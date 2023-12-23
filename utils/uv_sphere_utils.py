# code goes here, like how to easily select rings and segments...

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
