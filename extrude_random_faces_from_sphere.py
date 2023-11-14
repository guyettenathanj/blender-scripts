import bpy
import random
import bmesh

def clear_scene():
    """Clears all objects in the Blender scene."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def create_sphere_and_extrude(number_of_faces, min_extrude_distance, max_extrude_distance):
    """Creates a UV sphere and extrudes a number of random quad faces along their normals.

    Args:
    number_of_faces (int): The number of random faces to extrude.
    min_extrude_distance (float): The minimum distance to extrude each selected face.
    max_extrude_distance (float): The maximum distance to extrude each selected face.
    """
    # Create a UV Sphere
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))
    
    # Get the active mesh
    obj = bpy.context.active_object
    mesh = obj.data

    for _ in range(number_of_faces):
        # Switch to Edit Mode
        bpy.ops.object.mode_set(mode='EDIT')

        # Get BMesh representation
        bm = bmesh.from_edit_mesh(mesh)

        # Deselect all faces
        for face in bm.faces:
            face.select = False

        # Select a random quad face
        quads = [f for f in bm.faces if len(f.verts) == 4]
        if quads:
            random_face = random.choice(quads)
            random_face.select = True

            # Calculate the normal of the selected face
            face_normal = random_face.normal

            # Random extrusion value within the specified range
            extrude_value = random.uniform(min_extrude_distance, max_extrude_distance)

            # Extrude the selected face along its normal
            bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": face_normal * extrude_value})

            # Update the mesh
            bmesh.update_edit_mesh(mesh, loop_triangles=True)

        # Switch back to Object Mode
        bpy.ops.object.mode_set(mode='OBJECT')

# Clear the scene
clear_scene()

# Create a sphere and extrude multiple random quads with random extrusion distances
create_sphere_and_extrude(number_of_faces=3, min_extrude_distance=0.5, max_extrude_distance=2)
