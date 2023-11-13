import bpy
import math
import mathutils
from functools import partial

# Function to create children meshes recursively
def create_recursive_children(parent_mesh, recursive_depth, number_of_children, shrinking_factor, current_depth=0, offset_distance=1):
    # Base case: stop recursion when the current depth exceeds the desired recursive depth
    if current_depth >= recursive_depth:
        return

    # Scale down the child mesh by the shrinking factor
    child_scale = [dim * shrinking_factor for dim in parent_mesh.scale]

    # Calculate the radius and angle for positioning child meshes evenly in a circle around the parent
    radius = max(parent_mesh.dimensions) * (0.75 if current_depth == 0 else offset_distance)
    angle_between_children = 2 * math.pi / number_of_children

    for i in range(number_of_children):
        # Positioning logic for child meshes
        angle = angle_between_children * i
        x_offset = math.cos(angle) * radius
        y_offset = math.sin(angle) * radius

        # Duplicate the parent mesh data for the new child mesh
        new_mesh = parent_mesh.data.copy()
        new_object = bpy.data.objects.new(parent_mesh.name + "_child", new_mesh)
        bpy.context.collection.objects.link(new_object)
        new_object.location = parent_mesh.location + mathutils.Vector((x_offset, y_offset, 0))  # Adjust Z if necessary
        new_object.scale = tuple(child_scale)
        new_object.parent = parent_mesh

        # Recursive call to create children for the new child mesh
        create_recursive_children(new_object, recursive_depth, number_of_children, shrinking_factor, current_depth + 1, radius * shrinking_factor)

# Function to clean up the scene by removing children meshes
def cleanup_children_except_original(original_name):
    objects_to_remove = [obj for obj in bpy.data.objects if obj.name != original_name and obj.name.startswith(original_name)]
    for obj in objects_to_remove:
        bpy.data.objects.remove(obj, do_unlink=True)

# Function to ensure the original parent mesh exists
def ensure_original_exists(original_name):
    if original_name not in bpy.data.objects:
        bpy.ops.mesh.primitive_cube_add()
        cube = bpy.context.active_object
        cube.name = original_name
        cube.location = (0, 0, 0)  # Reset location to world origin
    return bpy.data.objects[original_name]

# Function to change the color of the mesh over time
def change_color(obj, frame_start, frame_end, depth_level, start_with_color, end_with_color):
    if not obj.data.materials:
        mat = bpy.data.materials.new(name="Material")
        obj.data.materials.append(mat)
    else:
        mat = obj.data.materials[0]
    
    mat.use_nodes = False
    mat.diffuse_color = start_with_color
    mat.keyframe_insert(data_path="diffuse_color", frame=frame_start)
    mat.diffuse_color = end_with_color
    mat.keyframe_insert(data_path="diffuse_color", frame=frame_end)

# Function to spin the mesh around the Z-axis
def spin_cube(obj, frame_start, frame_end, depth_level):
    obj.rotation_mode = 'XYZ'
    obj.keyframe_insert(data_path="rotation_euler", frame=frame_start)  # Insert starting keyframe
    obj.rotation_euler[2] += (depth_level + 1) * 2 * math.pi  # Full spin multiplied by depth level
    obj.keyframe_insert(data_path="rotation_euler", frame=frame_end)  # Insert ending keyframe

# Function to animate a transformation across a recursive hierarchy
def animate_recursive_transform(obj, transform_func, frame_start, frame_end, current_depth=0):
    transform_func(obj, frame_start, frame_end, current_depth)
    for child in obj.children:
        animate_recursive_transform(child, transform_func, frame_start, frame_end, current_depth + 1)

# Main script execution
if __name__ == "__main__":
    # Disable undo to save memory during operation
    bpy.context.preferences.edit.use_global_undo = False

    original_name = 'Cube'
    parent_mesh = ensure_original_exists(original_name)

    cleanup_children_except_original(original_name)

    create_recursive_children(parent_mesh, 3, 7, 0.5)

    # Animate transformations
    frame_start = 1
    frame_end = 100

    # Define the color change function with pre-set colors
    start_color = (1, 0, 0, 1)  # Red in RGBA
    end_color = (0, 0, 1, 1)  # Blue in RGBA
    color_change_func = partial(change_color, start_with_color=start_color, end_with_color=end_color)

    animate_recursive_transform(parent_mesh, color_change_func, frame_start, frame_end)

    # Define the spin function
    spin_func = partial(spin_cube)

    animate_recursive_transform(parent_mesh, spin_func, frame_start, frame_end)

    # Re-enable undo after operations are completed
    bpy.context.preferences.edit.use_global_undo = True
