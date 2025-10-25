
# Simple Blender Script for modern bungalow
import bpy

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# House attributes
num_floors = 2
style = "modern"
house_type = "bungalow"

print(f"Creating {num_floors}-floor {style} {house_type}")

# Create basic house structure
# Foundation
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0.1))
foundation = bpy.context.active_object
foundation.name = "Foundation"
foundation.scale = (5, 6, 0.1)

# Floors
for i in range(num_floors):
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0.5 + i * 3))
    floor = bpy.context.active_object
    floor.name = f"Floor_{i+1}"
    floor.scale = (4.5, 5.5, 1.5)

# Basic roof
if style in ['traditional', 'kerala']:
    # Sloped roof
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, num_floors * 3 + 1))
    roof = bpy.context.active_object
    roof.name = "Roof"
    roof.scale = (5, 6, 0.5)
else:
    # Flat roof
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, num_floors * 3 + 0.2))
    roof = bpy.context.active_object
    roof.name = "Roof"
    roof.scale = (4.8, 5.8, 0.2)

# Add some windows
for i in range(num_floors):
    for j in range(3):
        bpy.ops.mesh.primitive_cube_add(
            size=1, 
            location=(4.6, -3 + j * 2, 1 + i * 3)
        )
        window = bpy.context.active_object
        window.name = f"Window_{i}_{j}"
        window.scale = (0.1, 0.8, 1.2)

# Add main door
bpy.ops.mesh.primitive_cube_add(size=1, location=(4.6, 0, 1))
door = bpy.context.active_object
door.name = "Main_Door"
door.scale = (0.1, 0.8, 2)

# Add lighting
bpy.ops.object.light_add(type='SUN', location=(10, 10, 20))
sun = bpy.context.active_object
sun.data.energy = 3

# Add camera
bpy.ops.object.camera_add(location=(15, -15, 10))
camera = bpy.context.active_object
bpy.context.scene.camera = camera

# Save file
bpy.ops.wm.save_as_mainfile(filepath=r"./output\house_20251026_013412.blend")
print(f"House saved to: ./output\house_20251026_013412.blend")
