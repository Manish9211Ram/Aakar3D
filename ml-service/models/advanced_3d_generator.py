"""
Advanced 3D House Generator with Real Model Creation
Supports actual 3D model generation using Open3D and procedural modeling
"""

import numpy as np
import open3d as o3d
import trimesh
import json
import os
from datetime import datetime
import random
import math
from typing import Dict, List, Tuple, Any

class Advanced3DGenerator:
    """Real 3D model generator for Indian houses"""
    
    def __init__(self):
        self.output_dir = "output"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Color mappings for materials
        self.colors = {
            'red': [0.8, 0.2, 0.2],
            'blue': [0.2, 0.2, 0.8],
            'green': [0.2, 0.8, 0.2],
            'yellow': [0.8, 0.8, 0.2],
            'white': [0.9, 0.9, 0.9],
            'brown': [0.6, 0.4, 0.2],
            'orange': [0.8, 0.5, 0.2],
            'pink': [0.8, 0.6, 0.7],
            'purple': [0.6, 0.2, 0.8],
            'grey': [0.5, 0.5, 0.5],
            'black': [0.1, 0.1, 0.1],
            'cream': [0.9, 0.9, 0.8]
        }
        
        # Material properties
        self.materials = {
            'brick': {'roughness': 0.8, 'color_variation': 0.1},
            'wood': {'roughness': 0.6, 'color_variation': 0.15},
            'concrete': {'roughness': 0.7, 'color_variation': 0.05},
            'stone': {'roughness': 0.9, 'color_variation': 0.2},
            'glass': {'roughness': 0.1, 'color_variation': 0.02},
            'metal': {'roughness': 0.3, 'color_variation': 0.05}
        }
        
    def create_box_geometry(self, width: float, height: float, depth: float, 
                           center: Tuple[float, float, float] = (0, 0, 0)) -> o3d.geometry.TriangleMesh:
        """Create a box geometry"""
        box = o3d.geometry.TriangleMesh.create_box(width, height, depth)
        box.translate(center)
        return box
    
    def create_cylinder_geometry(self, radius: float, height: float, 
                                center: Tuple[float, float, float] = (0, 0, 0)) -> o3d.geometry.TriangleMesh:
        """Create a cylinder geometry"""
        cylinder = o3d.geometry.TriangleMesh.create_cylinder(radius, height)
        cylinder.translate(center)
        return cylinder
    
    def create_roof(self, width: float, depth: float, height: float, 
                   roof_type: str = "peaked", center: Tuple[float, float, float] = (0, 0, 0)) -> o3d.geometry.TriangleMesh:
        """Create different types of roofs"""
        if roof_type == "flat":
            roof = self.create_box_geometry(width, 0.2, depth, center)
        elif roof_type == "peaked":
            # Create a peaked roof using triangular prism
            vertices = np.array([
                [-width/2, 0, -depth/2],  # bottom corners
                [width/2, 0, -depth/2],
                [width/2, 0, depth/2],
                [-width/2, 0, depth/2],
                [0, height, -depth/2],    # top ridge
                [0, height, depth/2]
            ])
            
            faces = np.array([
                [0, 1, 4],  # front triangle
                [1, 2, 5],  # right side
                [2, 3, 5],  # back triangle  
                [3, 0, 4],  # left side
                [4, 5, 1],  # right roof face
                [4, 5, 2],
                [5, 4, 3],  # left roof face
                [4, 0, 3],
                [0, 1, 2],  # bottom face
                [0, 2, 3]
            ])
            
            roof = o3d.geometry.TriangleMesh()
            roof.vertices = o3d.utility.Vector3dVector(vertices)
            roof.triangles = o3d.utility.Vector3iVector(faces)
            roof.translate(center)
            
        elif roof_type == "dome":
            roof = o3d.geometry.TriangleMesh.create_sphere(min(width, depth)/2)
            roof.translate((center[0], center[1] + height/2, center[2]))
            
        return roof
    
    def create_window(self, width: float, height: float, 
                     center: Tuple[float, float, float] = (0, 0, 0)) -> o3d.geometry.TriangleMesh:
        """Create a window with frame"""
        # Window frame
        frame = self.create_box_geometry(width, height, 0.1, center)
        
        # Window glass (slightly inset)
        glass_center = (center[0], center[1], center[2] - 0.05)
        glass = self.create_box_geometry(width * 0.9, height * 0.9, 0.02, glass_center)
        
        # Combine frame and glass
        window = frame + glass
        return window
    
    def create_door(self, width: float, height: float, 
                   center: Tuple[float, float, float] = (0, 0, 0)) -> o3d.geometry.TriangleMesh:
        """Create a door"""
        door = self.create_box_geometry(width, height, 0.1, center)
        
        # Add door handle
        handle_center = (center[0] + width/3, center[1] - height/3, center[2] + 0.05)
        handle = o3d.geometry.TriangleMesh.create_sphere(0.05)
        handle.translate(handle_center)
        
        door += handle
        return door
    
    def create_balcony(self, width: float, depth: float, height: float,
                      center: Tuple[float, float, float] = (0, 0, 0)) -> o3d.geometry.TriangleMesh:
        """Create a balcony with railings"""
        # Balcony floor
        floor = self.create_box_geometry(width, 0.1, depth, center)
        
        # Railings
        railing_height = 1.0
        railing_thickness = 0.05
        
        # Front railing
        front_railing = self.create_box_geometry(width, railing_height, railing_thickness,
                                                (center[0], center[1] + railing_height/2, center[2] + depth/2))
        
        # Side railings
        left_railing = self.create_box_geometry(railing_thickness, railing_height, depth,
                                               (center[0] - width/2, center[1] + railing_height/2, center[2]))
        right_railing = self.create_box_geometry(railing_thickness, railing_height, depth,
                                                (center[0] + width/2, center[1] + railing_height/2, center[2]))
        
        balcony = floor + front_railing + left_railing + right_railing
        return balcony
    
    def apply_color_and_material(self, mesh: o3d.geometry.TriangleMesh, 
                                color: str, material: str) -> o3d.geometry.TriangleMesh:
        """Apply color and material properties to mesh"""
        base_color = self.colors.get(color, [0.5, 0.5, 0.5])
        material_props = self.materials.get(material, {'roughness': 0.5, 'color_variation': 0.1})
        
        # Add color variation for more realistic look
        variation = material_props['color_variation']
        varied_color = [
            max(0, min(1, base_color[0] + random.uniform(-variation, variation))),
            max(0, min(1, base_color[1] + random.uniform(-variation, variation))),
            max(0, min(1, base_color[2] + random.uniform(-variation, variation)))
        ]
        
        # Paint the mesh
        mesh.paint_uniform_color(varied_color)
        
        return mesh
    
    def generate_house_3d(self, attributes: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a complete 3D house model"""
        
        # Extract attributes
        floors = attributes.get('floors', 1)
        style = attributes.get('style', 'modern')
        color = attributes.get('color', 'white')
        material = attributes.get('material', 'brick')
        rooms = attributes.get('rooms', ['bedroom', 'kitchen'])
        features = attributes.get('features', [])
        dimensions = attributes.get('dimensions', {'width': 10, 'height': 8, 'depth': 8})
        
        # House dimensions
        width = dimensions['width']
        height_per_floor = dimensions['height'] / floors
        depth = dimensions['depth']
        
        # Create main structure
        house_meshes = []
        
        # Create floors
        for floor in range(floors):
            floor_height = height_per_floor
            floor_y = floor * height_per_floor
            
            # Main building structure
            building = self.create_box_geometry(width, floor_height, depth, 
                                              (0, floor_y + floor_height/2, 0))
            building = self.apply_color_and_material(building, color, material)
            house_meshes.append(building)
            
            # Add windows based on rooms
            num_windows = len(rooms) if rooms else 2
            for i in range(num_windows):
                window_x = (i - num_windows/2 + 0.5) * (width / num_windows)
                window_center = (window_x, floor_y + floor_height/2, depth/2 + 0.1)
                
                window = self.create_window(1.5, 2.0, window_center)
                window = self.apply_color_and_material(window, 'brown', 'wood')
                house_meshes.append(window)
            
            # Add door on ground floor
            if floor == 0:
                door_center = (0, height_per_floor/3, depth/2 + 0.1)
                door = self.create_door(1.0, 2.5, door_center)
                door = self.apply_color_and_material(door, 'brown', 'wood')
                house_meshes.append(door)
            
            # Add balcony if it's a feature
            if 'balcony' in features and floor > 0:
                balcony_center = (0, floor_y, depth/2 + 1.5)
                balcony = self.create_balcony(4.0, 2.0, 0.1, balcony_center)
                balcony = self.apply_color_and_material(balcony, 'grey', 'concrete')
                house_meshes.append(balcony)
        
        # Create roof
        roof_height = 2.0
        roof_center = (0, floors * height_per_floor + roof_height/2, 0)
        
        if style in ['traditional', 'kerala']:
            roof_type = "peaked"
        elif style in ['rajasthani', 'mughal']:
            roof_type = "dome"
        else:
            roof_type = "flat"
            
        roof = self.create_roof(width + 1, depth + 1, roof_height, roof_type, roof_center)
        roof = self.apply_color_and_material(roof, 'red', 'brick')
        house_meshes.append(roof)
        
        # Add garden/landscaping if feature exists
        if 'garden' in features:
            garden_base = self.create_box_geometry(width + 4, 0.1, depth + 4, (0, -0.05, 0))
            garden_base = self.apply_color_and_material(garden_base, 'green', 'wood')
            house_meshes.append(garden_base)
            
            # Add some trees (simple cylinders)
            for i in range(3):
                tree_x = random.uniform(-width/2 - 1, width/2 + 1)
                tree_z = random.uniform(-depth/2 - 1, depth/2 + 1)
                tree = self.create_cylinder_geometry(0.3, 4.0, (tree_x, 2.0, tree_z))
                tree = self.apply_color_and_material(tree, 'brown', 'wood')
                house_meshes.append(tree)
                
                # Tree top
                tree_top = o3d.geometry.TriangleMesh.create_sphere(1.5)
                tree_top.translate((tree_x, 5.0, tree_z))
                tree_top = self.apply_color_and_material(tree_top, 'green', 'wood')
                house_meshes.append(tree_top)
        
        # Combine all meshes
        final_mesh = house_meshes[0]
        for mesh in house_meshes[1:]:
            final_mesh += mesh
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"house_3d_{timestamp}"
        
        # Save as PLY file (3D format)
        ply_path = os.path.join(self.output_dir, f"{filename}.ply")
        o3d.io.write_triangle_mesh(ply_path, final_mesh)
        
        # Save as OBJ file (more universal)
        obj_path = os.path.join(self.output_dir, f"{filename}.obj")
        o3d.io.write_triangle_mesh(obj_path, final_mesh)
        
        # Convert to trimesh for additional formats
        try:
            vertices = np.asarray(final_mesh.vertices)
            faces = np.asarray(final_mesh.triangles)
            
            if len(vertices) > 0 and len(faces) > 0:
                trimesh_obj = trimesh.Trimesh(vertices=vertices, faces=faces)
                
                # Save as GLTF (web-friendly)
                gltf_path = os.path.join(self.output_dir, f"{filename}.gltf")
                trimesh_obj.export(gltf_path)
                
                # Save as STL (3D printing)
                stl_path = os.path.join(self.output_dir, f"{filename}.stl")
                trimesh_obj.export(stl_path)
        except Exception as e:
            print(f"Warning: Could not export additional formats: {e}")
        
        # Generate metadata
        metadata = {
            'model_id': filename,
            'generated_at': timestamp,
            'attributes': attributes,
            'files': {
                'ply': ply_path,
                'obj': obj_path,
                'gltf': f"{filename}.gltf" if 'gltf_path' in locals() else None,
                'stl': f"{filename}.stl" if 'stl_path' in locals() else None
            },
            'statistics': {
                'vertices': len(final_mesh.vertices),
                'triangles': len(final_mesh.triangles),
                'floors': floors,
                'features_count': len(features)
            }
        }
        
        # Save metadata
        metadata_path = os.path.join(self.output_dir, f"{filename}_metadata.json")
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return {
            'success': True,
            'model_id': filename,
            'files': metadata['files'],
            'statistics': metadata['statistics'],
            'download_links': {
                'ply': f"/download/{filename}.ply",
                'obj': f"/download/{filename}.obj",
                'gltf': f"/download/{filename}.gltf",
                'stl': f"/download/{filename}.stl"
            }
        }
    
    def create_preview_image(self, mesh: o3d.geometry.TriangleMesh, 
                           filename: str) -> str:
        """Create a preview image of the 3D model"""
        try:
            # Create visualizer
            vis = o3d.visualization.Visualizer()
            vis.create_window(visible=False)
            
            # Add mesh
            vis.add_geometry(mesh)
            
            # Set camera
            ctr = vis.get_view_control()
            ctr.set_front([0.5, -0.5, -0.5])
            ctr.set_lookat([0, 0, 0])
            ctr.set_up([0, 1, 0])
            ctr.set_zoom(0.8)
            
            # Render and save
            preview_path = os.path.join(self.output_dir, f"{filename}_preview.png")
            vis.capture_screen_image(preview_path)
            vis.destroy_window()
            
            return preview_path
        except Exception as e:
            print(f"Could not create preview: {e}")
            return None