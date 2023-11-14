import bpy

def delete_all_actions():
    # Loop over all actions in the data block
    for action in bpy.data.actions:
        # Remove the action
        bpy.data.actions.remove(action)


def delete_all_materials():
    # Loop over all materials in the data block
    for material in bpy.data.materials:
        # Use the user_clear() method to unset users of this material (if any)
        material.user_clear()
        # Remove the material
        bpy.data.materials.remove(material)
        
        
def animate_color_change(obj, colors, frames):
    """
    Animates color change for a given object over specified frames.

    :param obj: The Blender object to animate.
    :param colors: A list of RGBA color tuples.
    :param frames: A list of frame numbers corresponding to each color.
    """
    # Create a new material and assign it to the object
    material_name = f'{obj.name}_AnimatedColor'
    material = bpy.data.materials.new(name=material_name)
    obj.active_material = material

    # Animate color change by iterating over the provided colors and frames
    for frame_number, color in zip(frames, colors):
        obj.active_material.diffuse_color = color
        obj.active_material.keyframe_insert('diffuse_color', frame=frame_number)
        
        

# cleanup all previous materials and keyframes
delete_all_materials()
delete_all_actions()

# Fetch the Cube object directly without checking if it exists
cube = bpy.data.objects['Cube']

# Define colors and frames for the animation
color_changes = [(1, 0, 0, 1),  # Red
                 (0, 1, 0, 0)]  # Green
key_frames = [1, 250]

# Call the function with the Cube object, color changes, and key frames
animate_color_change(cube, color_changes, key_frames)
