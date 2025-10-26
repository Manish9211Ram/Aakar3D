"""
Blender Script Generator
Generates comprehensive Blender Python scripts for Indian house creation
"""

import json
from typing import Dict

class BlenderScriptGenerator:
    """
    Generate Blender Python scripts for creating complete house scenes
    """
    
    def __init__(self):
        self.script_template = ""
    
    def generate_blender_script(
        self,
        mesh_data: Dict,
        attributes: Dict,
        output_blend_path: str
    ) -> str:
        """
        Generate complete Blender Python script
        
        Args:
            mesh_data: Mesh geometry data
            attributes: House attributes
            output_blend_path: Output .blend file path
        
        Returns:
            Blender script as string
        """
        script = f'''
import bpy
import bmesh
import math
from mathutils import Vector, Matrix
import os

# Clear existing scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# Scene setup
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.device = 'GPU'

# ============================================================================
# HOUSE ATTRIBUTES
# ============================================================================

attributes = {json.dumps(attributes, indent=4)}

# ============================================================================
# MATERIALS
# ============================================================================

def create_material(name, color, roughness=0.5, metallic=0.0):
    """Create PBR material"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    # Output node
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (300, 0)
    
    # Principled BSDF
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    bsdf.inputs['Base Color'].default_value = color + (1.0,)
    bsdf.inputs['Roughness'].default_value = roughness
    bsdf.inputs['Metallic'].default_value = metallic
    
    # Link
    mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

# Create materials based on house attributes
colors = attributes.get('colors', ['white'])
materials = attributes.get('materials', ['concrete'])

# Color mapping
color_map = {{
    'white': (1.0, 1.0, 1.0),
    'cream': (1.0, 0.99, 0.82),
    'beige': (0.96, 0.96, 0.86),
    'brown': (0.65, 0.16, 0.16),
    'red': (0.8, 0.1, 0.1),
    'yellow': (1.0, 1.0, 0.0),
    'orange': (1.0, 0.65, 0.0),
    'pink': (1.0, 0.75, 0.8),
    'blue': (0.0, 0.3, 0.8),
    'green': (0.0, 0.6, 0.0),
    'grey': (0.5, 0.5, 0.5),
    'gray': (0.5, 0.5, 0.5),
    'sandstone': (0.87, 0.72, 0.53),
    'terracotta': (0.9, 0.45, 0.36)
}}

# Primary wall material
wall_color = color_map.get(colors[0] if colors else 'white', (1.0, 1.0, 1.0))
wall_material = create_material("Wall_Material", wall_color, roughness=0.7)

# Roof material
roof_material = create_material("Roof_Material", (0.6, 0.3, 0.2), roughness=0.9)

# Window glass material
glass_material = create_material("Glass_Material", (0.7, 0.8, 0.9), roughness=0.1, metallic=0.5)

# Door material
door_material = create_material("Door_Material", (0.4, 0.2, 0.1), roughness=0.6)

# Ground material
ground_material = create_material("Ground_Material", (0.3, 0.5, 0.2), roughness=0.9)

# ============================================================================
# HOUSE GENERATION FUNCTIONS
# ============================================================================

def create_foundation(width, length, height=0.5):
    """Create foundation/plinth"""
    bpy.ops.mesh.primitive_cube_add(size=1)
    foundation = bpy.context.active_object
    foundation.name = "Foundation"
    foundation.scale = (width/2 + 0.3, length/2 + 0.3, height/2)
    foundation.location = (0, 0, height/2)
    foundation.data.materials.append(wall_material)
    return foundation

def create_floor(width, length, height, floor_num):
    """Create building floor"""
    bpy.ops.mesh.primitive_cube_add(size=1)
    floor = bpy.context.active_object
    floor.name = f"Floor_{{floor_num}}"
    floor.scale = (width/2, length/2, height/2)
    floor.location = (0, 0, (floor_num - 0.5) * height)
    floor.data.materials.append(wall_material)
    return floor

def create_window(x, y, z, width=1.2, height=1.5):
    """Create window"""
    bpy.ops.mesh.primitive_cube_add(size=1)
    window = bpy.context.active_object
    window.name = "Window"
    window.scale = (0.1, width/2, height/2)
    window.location = (x, y, z)
    window.data.materials.append(glass_material)
    return window

def create_door(x, y, z, width=1.0, height=2.2):
    """Create door"""
    bpy.ops.mesh.primitive_cube_add(size=1)
    door = bpy.context.active_object
    door.name = "Door"
    door.scale = (0.1, width/2, height/2)
    door.location = (x, y, z)
    door.data.materials.append(door_material)
    return door

def create_flat_roof(width, length, height, floor_num):
    """Create flat roof"""
    bpy.ops.mesh.primitive_cube_add(size=1)
    roof = bpy.context.active_object
    roof.name = "Roof_Flat"
    roof.scale = (width/2 + 0.2, length/2 + 0.2, 0.15)
    roof.location = (0, 0, floor_num * height + 0.15)
    roof.data.materials.append(roof_material)
    return roof

def create_sloped_roof(width, length, height, floor_num, style='gabled'):
    """Create sloped roof"""
    roof_height = 2.0
    
    if style in ['traditional', 'kerala', 'south_indian']:
        # Steep slope for traditional
        roof_height = 2.5
    
    # Create pyramid roof
    verts = [
        (-width/2 - 0.3, -length/2 - 0.3, floor_num * height),
        (width/2 + 0.3, -length/2 - 0.3, floor_num * height),
        (width/2 + 0.3, length/2 + 0.3, floor_num * height),
        (-width/2 - 0.3, length/2 + 0.3, floor_num * height),
        (0, 0, floor_num * height + roof_height)
    ]
    
    faces = [
        (0, 1, 4),
        (1, 2, 4),
        (2, 3, 4),
        (3, 0, 4)
    ]
    
    mesh = bpy.data.meshes.new("Roof_Mesh")
    mesh.from_pydata(verts, [], faces)
    roof = bpy.data.objects.new("Roof_Sloped", mesh)
    bpy.context.collection.objects.link(roof)
    roof.data.materials.append(roof_material)
    
    return roof

def create_balcony(x, y, z, width=2.0, depth=1.5):
    """Create balcony"""
    # Balcony floor
    bpy.ops.mesh.primitive_cube_add(size=1)
    balcony = bpy.context.active_object
    balcony.name = "Balcony_Floor"
    balcony.scale = (0.1, width/2, depth/2)
    balcony.location = (x, y, z)
    balcony.data.materials.append(wall_material)
    
    # Balcony railing
    for i in range(4):
        angle = i * math.pi / 2
        rx = x + (depth/2) * math.cos(angle)
        ry = y + (depth/2) * math.sin(angle)
        
        bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=1.0)
        railing = bpy.context.active_object
        railing.name = f"Railing_{{i}}"
        railing.location = (rx, ry, z + 0.5)
        railing.data.materials.append(wall_material)
    
    return balcony

def create_pillar(x, y, base_height, total_height, radius=0.3):
    """Create decorative pillar"""
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=total_height)
    pillar = bpy.context.active_object
    pillar.name = "Pillar"
    pillar.location = (x, y, base_height + total_height/2)
    pillar.data.materials.append(wall_material)
    return pillar

def create_courtyard(width, length):
    """Create central courtyard"""
    court_width = width * 0.4
    court_length = length * 0.4
    
    bpy.ops.mesh.primitive_plane_add(size=1)
    courtyard = bpy.context.active_object
    courtyard.name = "Courtyard"
    courtyard.scale = (court_width/2, court_length/2, 1)
    courtyard.location = (0, 0, 0.01)
    courtyard.data.materials.append(ground_material)
    
    return courtyard

def create_jali_pattern(x, y, z, width, height):
    """Create Jali (lattice) pattern"""
    jali_mat = create_material("Jali_Material", (0.9, 0.85, 0.7), roughness=0.5)
    
    # Create grid pattern
    num_holes = 5
    hole_size = 0.15
    spacing = width / (num_holes + 1)
    
    for i in range(num_holes):
        for j in range(num_holes):
            bpy.ops.mesh.primitive_cube_add(size=hole_size)
            hole = bpy.context.active_object
            hole.name = f"Jali_Hole_{{i}}_{{j}}"
            hole.location = (
                x,
                y - width/2 + (i+1)*spacing,
                z - height/2 + (j+1)*spacing
            )
            hole.data.materials.append(jali_mat)

def create_veranda(width, length, height):
    """Create veranda/porch"""
    veranda_depth = 2.5
    
    # Veranda floor
    bpy.ops.mesh.primitive_cube_add(size=1)
    veranda = bpy.context.active_object
    veranda.name = "Veranda_Floor"
    veranda.scale = (0.1, width/2, veranda_depth/2)
    veranda.location = (0, -length/2 - veranda_depth/2, 0.05)
    veranda.data.materials.append(wall_material)
    
    # Veranda pillars
    num_pillars = 4
    for i in range(num_pillars):
        px = -width/2 + (i * width/(num_pillars-1))
        create_pillar(px, -length/2 - veranda_depth, 0, height, radius=0.25)
    
    # Veranda roof
    bpy.ops.mesh.primitive_cube_add(size=1)
    v_roof = bpy.context.active_object
    v_roof.name = "Veranda_Roof"
    v_roof.scale = (width/2 + 0.2, veranda_depth/2 + 0.2, 0.15)
    v_roof.location = (0, -length/2 - veranda_depth/2, height + 0.15)
    v_roof.data.materials.append(roof_material)
    
    return veranda

# ============================================================================
# BUILD HOUSE
# ============================================================================

num_floors = attributes.get('num_floors', 2)
style = attributes.get('style', 'modern')
dims = attributes.get('dimensions', {{'width': 10, 'length': 12, 'height': 3}})
rooms = attributes.get('rooms', [])
features = attributes.get('features', [])

width = dims['width']
length = dims['length']
floor_height = dims['height']

print(f"Building {{num_floors}}-floor {{style}} house...")

# Create foundation
foundation = create_foundation(width, length, 0.5)

# Create floors
floors = []
for i in range(1, num_floors + 1):
    floor = create_floor(width, length, floor_height, i)
    floors.append(floor)
    
    # Add windows
    window_spacing = 2.5
    num_windows = int(width / window_spacing)
    
    for j in range(num_windows):
        wx = -width/2 + (j + 0.5) * window_spacing
        
        # Front windows
        create_window(
            width/2 + 0.05,
            wx,
            (i - 0.5) * floor_height + floor_height/2,
            width=1.0,
            height=1.4
        )
        
        # Back windows
        create_window(
            -width/2 - 0.05,
            wx,
            (i - 0.5) * floor_height + floor_height/2,
            width=1.0,
            height=1.4
        )

# Add main door (ground floor, front)
create_door(
    width/2 + 0.05,
    0,
    floor_height/2,
    width=1.2,
    height=2.2
)

# Create roof based on style
if style in ['modern', 'contemporary']:
    roof = create_flat_roof(width, length, floor_height, num_floors)
elif style in ['traditional', 'kerala', 'south_indian', 'rajasthani']:
    roof = create_sloped_roof(width, length, floor_height, num_floors, style)
else:
    roof = create_flat_roof(width, length, floor_height, num_floors)

# Add balconies if present
if 'balcony' in rooms:
    for i in range(2, num_floors + 1):
        create_balcony(
            width/2 + 1.0,
            0,
            (i - 0.5) * floor_height,
            width=2.5,
            depth=1.5
        )

# Add veranda for traditional styles
if 'veranda' in rooms or style in ['traditional', 'kerala']:
    create_veranda(width, length, floor_height)

# Add courtyard for traditional styles
if 'courtyard' in features or style in ['traditional', 'kerala', 'rajasthani']:
    create_courtyard(width, length)

# Add pillars for colonial/traditional
if 'pillars' in features or style in ['colonial', 'rajasthani']:
    # Corner pillars
    corners = [
        (-width/2, -length/2),
        (width/2, -length/2),
        (width/2, length/2),
        (-width/2, length/2)
    ]
    for cx, cy in corners:
        create_pillar(cx, cy, 0, num_floors * floor_height, radius=0.35)

# Add Jali for Rajasthani style
if 'jali' in features or style == 'rajasthani':
    create_jali_pattern(
        width/2 + 0.05,
        0,
        floor_height * 1.5,
        width=3.0,
        height=2.0
    )

# ============================================================================
# LANDSCAPING
# ============================================================================

# Ground plane
bpy.ops.mesh.primitive_plane_add(size=1)
ground = bpy.context.active_object
ground.name = "Ground"
ground.scale = (width * 2, length * 2, 1)
ground.location = (0, 0, -0.01)
ground.data.materials.append(ground_material)

# Add garden if specified
if 'garden' in features:
    # Trees
    for i in range(4):
        tx = (-width - 2) + i * (2*width + 4) / 3
        
        # Tree trunk
        bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=3)
        trunk = bpy.context.active_object
        trunk.name = f"Tree_Trunk_{{i}}"
        trunk.location = (tx, length + 3, 1.5)
        trunk_mat = create_material(f"Trunk_{{i}}", (0.4, 0.2, 0.1), 0.8)
        trunk.data.materials.append(trunk_mat)
        
        # Tree canopy
        bpy.ops.mesh.primitive_ico_sphere_add(radius=1.5)
        canopy = bpy.context.active_object
        canopy.name = f"Tree_Canopy_{{i}}"
        canopy.location = (tx, length + 3, 4)
        canopy_mat = create_material(f"Canopy_{{i}}", (0.1, 0.6, 0.1), 0.9)
        canopy.data.materials.append(canopy_mat)

# Compound wall if specified
if 'compound_wall' in features:
    wall_height = 2.0
    wall_thickness = 0.2
    
    # Front wall with gate
    bpy.ops.mesh.primitive_cube_add(size=1)
    front_wall = bpy.context.active_object
    front_wall.name = "Compound_Wall_Front"
    front_wall.scale = (wall_thickness/2, (width*1.5)/2, wall_height/2)
    front_wall.location = (width + 2, 0, wall_height/2)
    wall_mat = create_material("Compound_Wall", (0.7, 0.7, 0.6), 0.8)
    front_wall.data.materials.append(wall_mat)

# ============================================================================
# LIGHTING
# ============================================================================

# Sun light
bpy.ops.object.light_add(type='SUN', location=(10, 10, 20))
sun = bpy.context.active_object
sun.name = "Sun"
sun.data.energy = 3.0
sun.rotation_euler = (math.radians(45), 0, math.radians(45))

# Area light for ambient
bpy.ops.object.light_add(type='AREA', location=(0, 0, 15))
area_light = bpy.context.active_object
area_light.name = "Area_Light"
area_light.data.energy = 500
area_light.data.size = 20

# Point lights for accent
for i in range(2):
    bpy.ops.object.light_add(type='POINT', location=((-1)**i * width, 0, floor_height * num_floors + 2))
    point = bpy.context.active_object
    point.name = f"Point_Light_{{i}}"
    point.data.energy = 200

# ============================================================================
# CAMERA
# ============================================================================

# Create camera
bpy.ops.object.camera_add(location=(width * 1.5, -length * 1.8, floor_height * num_floors * 0.7))
camera = bpy.context.active_object
camera.name = "Camera"

# Point camera at house
direction = Vector((0, 0, floor_height * num_floors / 2)) - camera.location
rot_quat = direction.to_track_quat('-Z', 'Y')
camera.rotation_euler = rot_quat.to_euler()

# Set as active camera
scene.camera = camera

# ============================================================================
# RENDER SETTINGS
# ============================================================================

scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100
scene.cycles.samples = 128
scene.view_settings.view_transform = 'Filmic'

# ============================================================================
# SAVE BLEND FILE
# ============================================================================

output_path = r"{output_blend_path}"
bpy.ops.wm.save_as_mainfile(filepath=output_path)

print(f"✓ Saved Blender file: {{output_path}}")
print(f"  Floors: {{num_floors}}")
print(f"  Style: {{style}}")
print(f"  Dimensions: {{width}}m x {{length}}m x {{floor_height * num_floors}}m")
'''
        
        return script
    
    def save_script(self, script: str, script_path: str):
        """Save Blender script to file"""
        with open(script_path, 'w') as f:
            f.write(script)
        print(f"  ✓ Saved script: {script_path}")