import bpy
import random

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

def color_faces_randomly(mesh_object):
    """
    Colors each face of a given mesh object with a random color.
    
    :param mesh_object: The mesh object to color. Must be of type 'MESH'.
    """

    # Ensure the object is a mesh
    if mesh_object.type != 'MESH':
        raise ValueError("Provided object is not a mesh")

    # Create a new material with a vertex color layer
    mat = bpy.data.materials.new(name="RandomFaceColorMaterial")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    vcol = mat.node_tree.nodes.new(type="ShaderNodeVertexColor")
    mat.node_tree.links.new(bsdf.inputs['Base Color'], vcol.outputs['Color'])

    # Assign the material to the mesh
    if len(mesh_object.data.materials) > 0:
        mesh_object.data.materials[0] = mat
    else:
        mesh_object.data.materials.append(mat)

    # Enable vertex color painting
    if not mesh_object.data.vertex_colors:
        mesh_object.data.vertex_colors.new()

    # Get the vertex color layer
    color_layer = mesh_object.data.vertex_colors.active

    # Assign a random color to each face
    for poly in mesh_object.data.polygons:
        color = [random.random() for _ in range(3)] + [1]  # RGB + Alpha
        for idx in poly.loop_indices:
            color_layer.data[idx].color = color

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


# Reset the scene using cleanup function/s
cleanup_mesh_objects()

# Parameters for the sphere
location = (0, 0, 0)
radius = 1
segments = 200  # Adjust this value for horizontal subdivisions
rings = 200    # Adjust this value for vertical subdivisions

# Create a UV sphere
created_sphere = create_uv_sphere(location, radius, segments, rings)

# Apply the color function to the created sphere
color_faces_randomly(created_sphere)
