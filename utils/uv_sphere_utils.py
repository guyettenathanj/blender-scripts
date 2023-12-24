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
    
    
    
def get_triangular_face_indices(obj):
    # Ensure the passed object is a Blender Mesh object
    if obj is None or obj.type != 'MESH':
        print("The passed object is not a valid mesh.")
        return []

    # Ensure Blender is in object mode
    if bpy.context.active_object is not None:
        bpy.ops.object.mode_set(mode='OBJECT')

    # Make the passed object the active object and select it
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    # Switch to edit mode
    bpy.ops.object.mode_set(mode='EDIT')

    # Get the mesh data
    mesh = bmesh.from_edit_mesh(obj.data)

    # Create a collection for indices of triangular faces
    triangular_face_indices = []

    # Find and store indices of triangular faces
    for face in mesh.faces:
        if len(face.verts) == 3:
            triangular_face_indices.append(face.index)

    # Update the mesh and return to object mode
    bmesh.update_edit_mesh(obj.data)
    bpy.ops.object.mode_set(mode='OBJECT')

    return triangular_face_indices




def select_single_face(obj, tri_face_indices, face_index):
    if not tri_face_indices:
        print("No triangular face indices available.")
        return

    if face_index < 0 or face_index >= len(tri_face_indices):
        print("Invalid face index.")
        return

    # Ensure Blender is in object mode and object is selected
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    # Switch to edit mode
    bpy.ops.object.mode_set(mode='EDIT')

    # Get the mesh data
    mesh_data = bmesh.from_edit_mesh(obj.data)

    # Deselect all faces
    for face in mesh_data.faces:
        face.select = False

    # Select the specified face by index
    for face in mesh_data.faces:
        if face.index == tri_face_indices[face_index]:
            face.select = True
            break

    # Update the mesh
    bmesh.update_edit_mesh(obj.data)
    
    
def select_multiple_faces(obj, tri_face_indices, face_indices):
    if not tri_face_indices:
        print("No triangular face indices available.")
        return

    # Validate all face indices
    for face_index in face_indices:
        if face_index < 0 or face_index >= len(tri_face_indices):
            print(f"Invalid face index: {face_index}")
            return

    # Ensure Blender is in object mode and object is selected
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    # Switch to edit mode
    bpy.ops.object.mode_set(mode='EDIT')

    # Get the mesh data
    mesh_data = bmesh.from_edit_mesh(obj.data)
    
    # Deselect all faces
    for face in mesh_data.faces:
        face.select = False

    # Select the specified faces by indices
    for face in mesh_data.faces:
        if face.index in [tri_face_indices[i] for i in face_indices]:
            face.select = True

    # Update the mesh
    bmesh.update_edit_mesh(obj.data)



# Reset the scene using cleanup function/s
cleanup_mesh_objects()

# Parameters for the sphere
location = (0, 0, 0)
radius = 1
segments = 10  # Adjust this value for horizontal subdivisions
rings = 5    # Adjust this value for vertical subdivisions
    
# Create a UV sphere
created_sphere = create_uv_sphere(location, radius, segments, rings)

tri_face_indices = get_triangular_face_indices(created_sphere)

# times 2 because we do top and bottom alternating
range_list = [i for i in range(segments * 2)]

# this will select the top and bottom rings of the uv sphere
select_multiple_faces(created_sphere, tri_face_indices, range_list)
