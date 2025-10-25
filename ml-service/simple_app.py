"""
Simple ML API Server for Aakar3D
Basic text-to-house generation without heavy dependencies
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import json
import time
import os
import re
import math
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Simple configuration
class SimpleConfig:
    def __init__(self):
        self.output_dir = "./output"
        self.device = "cpu"
        os.makedirs(self.output_dir, exist_ok=True)

config = SimpleConfig()

# Enhanced text parser with detailed architecture
class AdvancedHouseParser:
    def __init__(self):
        self.styles = {
            'modern': ['modern', 'contemporary', 'minimalist', 'sleek', 'futuristic', 'glass'],
            'traditional': ['traditional', 'classic', 'ethnic', 'heritage', 'vintage', 'ancient'],
            'kerala': ['kerala', 'south indian', 'coconut', 'backwater', 'malabar', 'nalukettu'],
            'rajasthani': ['rajasthani', 'rajput', 'royal', 'palace', 'fort', 'desert', 'jharokha'],
            'colonial': ['colonial', 'british', 'victorian', 'anglo', 'european'],
            'mughal': ['mughal', 'islamic', 'indo-islamic', 'persian', 'dome', 'arch'],
            'mediterranean': ['mediterranean', 'spanish', 'italian', 'villa'],
            'farmhouse': ['farmhouse', 'rustic', 'country', 'barn']
        }
        
        self.house_types = {
            'palace': ['palace', 'maharaja', 'royal residence'],
            'haveli': ['haveli', 'mansion', 'grand house'],
            'villa': ['villa', 'luxury house', 'premium'],
            'bungalow': ['bungalow', 'single floor'],
            'cottage': ['cottage', 'small house', 'tiny house'],
            'farmhouse': ['farmhouse', 'rural house', 'countryside'],
            'duplex': ['duplex', 'twin house', 'double'],
            'penthouse': ['penthouse', 'top floor'],
            'townhouse': ['townhouse', 'row house']
        }
        
        self.room_types = {
            'bedroom': ['bedroom', 'master bedroom', 'guest room', 'bhk'],
            'living_room': ['living room', 'hall', 'lounge', 'sitting room'],
            'kitchen': ['kitchen', 'cooking area', 'pantry'],
            'bathroom': ['bathroom', 'washroom', 'toilet', 'powder room'],
            'dining_room': ['dining room', 'dining area'],
            'study': ['study', 'office', 'library', 'workspace'],
            'balcony': ['balcony', 'terrace', 'deck'],
            'veranda': ['veranda', 'porch', 'sit out'],
            'pooja_room': ['pooja room', 'temple', 'prayer room'],
            'guest_room': ['guest room', 'guest bedroom'],
            'storage': ['storage', 'store room', 'utility']
        }
        
        self.features = {
            'courtyard': ['courtyard', 'inner court', 'atrium'],
            'garden': ['garden', 'lawn', 'landscaping'],
            'swimming_pool': ['swimming pool', 'pool', 'jacuzzi'],
            'parking': ['parking', 'garage', 'car porch'],
            'elevator': ['elevator', 'lift'],
            'security': ['security', 'gate', 'watchman'],
            'solar': ['solar', 'solar panels', 'green energy'],
            'basement': ['basement', 'underground'],
            'rooftop': ['rooftop', 'terrace garden'],
            'fountain': ['fountain', 'water feature']
        }
        
        self.materials = {
            'brick': ['brick', 'red brick', 'clay brick'],
            'stone': ['stone', 'limestone', 'granite', 'natural stone'],
            'marble': ['marble', 'white marble', 'italian marble'],
            'wood': ['wood', 'wooden', 'timber', 'teak', 'oak'],
            'glass': ['glass', 'transparent', 'crystal', 'glazed'],
            'concrete': ['concrete', 'cement', 'rcc'],
            'sandstone': ['sandstone', 'yellow stone', 'beige stone'],
            'steel': ['steel', 'metal', 'iron'],
            'bamboo': ['bamboo', 'eco', 'sustainable']
        }
        
        self.colors = {
            'white': ['white', 'off white', 'cream'],
            'beige': ['beige', 'sand', 'tan'],
            'brown': ['brown', 'chocolate', 'coffee'],
            'red': ['red', 'maroon', 'crimson'],
            'blue': ['blue', 'navy', 'azure'],
            'green': ['green', 'olive', 'forest'],
            'yellow': ['yellow', 'golden', 'amber'],
            'grey': ['grey', 'gray', 'silver'],
            'orange': ['orange', 'terracotta', 'rust'],
            'pink': ['pink', 'rose', 'salmon']
        }
        
    def parse_text(self, text):
        text_lower = text.lower()
        
        attributes = {
            'text': text,
            'num_floors': self._extract_floors(text_lower),
            'style': self._extract_style(text_lower),
            'house_type': self._extract_house_type(text_lower),
            'rooms': self._extract_rooms(text_lower),
            'room_count': self._extract_room_count(text_lower),
            'features': self._extract_features(text_lower),
            'materials': self._extract_materials(text_lower),
            'colors': self._extract_colors(text_lower),
            'dimensions': self._extract_dimensions(text_lower),
            'windows': self._extract_windows(text_lower),
            'doors': self._extract_doors(text_lower),
            'budget_tier': self._extract_budget_tier(text_lower),
            'orientation': self._extract_orientation(text_lower)
        }
        
        return attributes
    
    def _extract_floors(self, text):
        patterns = [
            (r'(\d+)\s*(?:floor|story|storey)', lambda m: int(m.group(1))),
            (r'single\s*(?:floor|story)', lambda m: 1),
            (r'double\s*(?:floor|story)|duplex', lambda m: 2),
            (r'triple\s*(?:floor|story)', lambda m: 3),
            (r'(\d+)\s*bhk', lambda m: max(1, min(3, (int(m.group(1)) + 1) // 2)))
        ]
        
        for pattern, extractor in patterns:
            match = re.search(pattern, text)
            if match:
                return max(1, min(extractor(match), 5))
        
        # Smart defaults
        if any(word in text for word in ['cottage', 'bungalow']):
            return 1
        elif any(word in text for word in ['villa', 'mansion']):
            return 2
        elif any(word in text for word in ['haveli', 'palace']):
            return 3
        
        return 2
    
    def _extract_style(self, text):
        for style, keywords in self.styles.items():
            if any(keyword in text for keyword in keywords):
                return style
        return 'modern'
    
    def _extract_house_type(self, text):
        for house_type, keywords in self.house_types.items():
            if any(keyword in text for keyword in keywords):
                return house_type
        return 'bungalow'
    
    def _extract_rooms(self, text):
        found_rooms = []
        for room, keywords in self.room_types.items():
            if any(keyword in text for keyword in keywords):
                found_rooms.append(room)
        
        if not found_rooms:
            found_rooms = ['living_room', 'bedroom', 'kitchen', 'bathroom']
        
        return found_rooms
    
    def _extract_room_count(self, text):
        # Extract specific room counts
        room_counts = {}
        
        # Bedroom count
        bed_match = re.search(r'(\d+)\s*(?:bed|bedroom|bhk)', text)
        if bed_match:
            room_counts['bedrooms'] = int(bed_match.group(1))
        
        # Bathroom count  
        bath_match = re.search(r'(\d+)\s*(?:bath|bathroom)', text)
        if bath_match:
            room_counts['bathrooms'] = int(bath_match.group(1))
            
        return room_counts
    
    def _extract_features(self, text):
        found_features = []
        for feature, keywords in self.features.items():
            if any(keyword in text for keyword in keywords):
                found_features.append(feature)
        return found_features
    
    def _extract_materials(self, text):
        found_materials = []
        for material, keywords in self.materials.items():
            if any(keyword in text for keyword in keywords):
                found_materials.append(material)
        return found_materials if found_materials else ['brick']
    
    def _extract_colors(self, text):
        found_colors = []
        for color, keywords in self.colors.items():
            if any(keyword in text for keyword in keywords):
                found_colors.append(color)
        return found_colors if found_colors else ['white']
    
    def _extract_windows(self, text):
        window_info = {
            'style': 'standard',
            'count': 'auto',
            'size': 'medium'
        }
        
        if any(word in text for word in ['large window', 'big window', 'floor to ceiling']):
            window_info['size'] = 'large'
        elif any(word in text for word in ['small window', 'tiny window']):
            window_info['size'] = 'small'
            
        if any(word in text for word in ['bay window', 'bow window']):
            window_info['style'] = 'bay'
        elif any(word in text for word in ['french window', 'glass door']):
            window_info['style'] = 'french'
        elif any(word in text for word in ['jharokha', 'traditional window']):
            window_info['style'] = 'jharokha'
            
        return window_info
    
    def _extract_doors(self, text):
        door_info = {
            'main_door': 'wooden',
            'interior': 'standard',
            'count': 'auto'
        }
        
        if any(word in text for word in ['wooden door', 'teak door']):
            door_info['main_door'] = 'wooden'
        elif any(word in text for word in ['glass door', 'sliding door']):
            door_info['main_door'] = 'glass'
        elif any(word in text for word in ['metal door', 'steel door']):
            door_info['main_door'] = 'metal'
            
        return door_info
    
    def _extract_budget_tier(self, text):
        if any(word in text for word in ['luxury', 'premium', 'high end', 'expensive']):
            return 'luxury'
        elif any(word in text for word in ['budget', 'affordable', 'economic', 'cheap']):
            return 'budget'
        else:
            return 'standard'
    
    def _extract_orientation(self, text):
        if any(word in text for word in ['north facing', 'north']):
            return 'north'
        elif any(word in text for word in ['south facing', 'south']):
            return 'south'
        elif any(word in text for word in ['east facing', 'east']):
            return 'east'
        elif any(word in text for word in ['west facing', 'west']):
            return 'west'
        return 'auto'
    
    def _extract_dimensions(self, text):
        dims = {'width': 12.0, 'length': 15.0, 'height': 3.2}
        
        # Look for dimensions
        match = re.search(r'(\d+)\s*x\s*(\d+)\s*(?:feet|ft|meter|m)', text)
        if match:
            w, l = float(match.group(1)), float(match.group(2))
            if 'feet' in text or 'ft' in text:
                dims['width'] = w * 0.3048
                dims['length'] = l * 0.3048
            else:
                dims['width'] = w
                dims['length'] = l
        
        return dims
    
    def _extract_rooms(self, text):
        found_rooms = []
        for room, keywords in self.room_types.items():
            if any(keyword in text for keyword in keywords):
                found_rooms.append(room)
        return found_rooms if found_rooms else ['living_room', 'bedroom', 'kitchen', 'bathroom']
    
    def _extract_features(self, text):
        found_features = []
        for feature, keywords in self.features.items():
            if any(keyword in text for keyword in keywords):
                found_features.append(feature)
        return found_features
    
    def _extract_dimensions(self, text):
        # Simple dimension extraction
        dims = {'width': 10.0, 'length': 12.0, 'height': 3.0}
        
        # Look for dimensions like "30x40 feet"
        match = re.search(r'(\d+)\s*x\s*(\d+)\s*(?:feet|ft)', text)
        if match:
            w, l = float(match.group(1)), float(match.group(2))
            dims['width'] = w * 0.3048  # Convert feet to meters
            dims['length'] = l * 0.3048
        
        return dims
    
    def _extract_colors(self, text):
        colors = ['white', 'cream', 'brown', 'red', 'blue', 'green', 'grey', 'yellow']
        found_colors = []
        for color in colors:
            if color in text:
                found_colors.append(color)
        return found_colors if found_colors else ['white']

# Simple Blender script generator
class SimpleBlenderGenerator:
    def generate_basic_script(self, attributes, output_path):
        script = f'''
# Simple Blender Script for {attributes.get('style', 'modern')} {attributes.get('house_type', 'house')}
import bpy

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# House attributes
num_floors = {attributes.get('num_floors', 2)}
style = "{attributes.get('style', 'modern')}"
house_type = "{attributes.get('house_type', 'bungalow')}"

print(f"Creating {{num_floors}}-floor {{style}} {{house_type}}")

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
    floor.name = f"Floor_{{i+1}}"
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
        window.name = f"Window_{{i}}_{{j}}"
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
bpy.ops.wm.save_as_mainfile(filepath=r"{output_path}")
print(f"House saved to: {output_path}")
'''
        return script
    
    def generate_threejs_data(self, attributes):
        """Generate advanced Three.js compatible 3D data for different Indian house styles"""
        num_floors = attributes.get('num_floors', 2)
        style = attributes.get('style', 'modern')
        house_type = attributes.get('house_type', 'bungalow')
        colors = attributes.get('colors', ['white'])
        features = attributes.get('features', [])
        rooms = attributes.get('rooms', [])
        dimensions = attributes.get('dimensions', {})
        
        house_objects = []
        
        # Base dimensions based on house type
        if house_type == 'villa':
            base_width, base_length = 8, 10
            wall_height = 3.5
        elif house_type == 'bungalow':
            base_width, base_length = 6, 8
            wall_height = 3
        elif house_type == 'haveli':
            base_width, base_length = 12, 15
            wall_height = 4
        elif house_type == 'cottage':
            base_width, base_length = 5, 6
            wall_height = 2.5
        else:
            base_width, base_length = 7, 9
            wall_height = 3
        
        # Color mapping
        main_color = colors[0] if colors else 'white'
        color_map = {
            'white': '#F5F5F5', 'cream': '#F5F5DC', 'brown': '#D2B48C',
            'red': '#CD853F', 'blue': '#B0C4DE', 'green': '#98FB98',
            'grey': '#D3D3D3', 'yellow': '#F0E68C'
        }
        wall_color = color_map.get(main_color, '#F5F5F5')
        
        # Foundation - varies by style
        if style == 'traditional':
            # Raised foundation for traditional houses
            house_objects.append({
                "name": "Foundation",
                "type": "box",
                "position": [0, 0, 0.3],
                "scale": [base_width + 1, base_length + 1, 0.6],
                "color": "#8B4513",
                "material": "foundation"
            })
        else:
            house_objects.append({
                "name": "Foundation", 
                "type": "box",
                "position": [0, 0, 0.1],
                "scale": [base_width, base_length, 0.2],
                "color": "#696969",
                "material": "foundation"
            })
        
        # Main structure - floors
        for i in range(num_floors):
            floor_y = 0.5 + i * wall_height
            
            # Main walls
            house_objects.append({
                "name": f"Floor_{i+1}_Main",
                "type": "box",
                "position": [0, 0, floor_y + wall_height/2],
                "scale": [base_width, base_length, wall_height],
                "color": wall_color,
                "material": "wall"
            })
            
            # Add balconies for upper floors if mentioned
            if i > 0 and 'balcony' in rooms:
                house_objects.append({
                    "name": f"Balcony_{i+1}",
                    "type": "box", 
                    "position": [base_width/2 + 0.8, 0, floor_y + wall_height/2],
                    "scale": [1.6, 3, 0.2],
                    "color": "#D2B48C",
                    "material": "balcony"
                })
                
                # Balcony railing
                for j in range(3):
                    house_objects.append({
                        "name": f"Railing_{i}_{j}",
                        "type": "box",
                        "position": [base_width/2 + 0.8, -1.2 + j * 1.2, floor_y + wall_height - 0.3],
                        "scale": [1.6, 0.05, 0.8],
                        "color": "#8B4513",
                        "material": "railing"
                    })
        
        # Roof - different styles
        roof_height = 0.5 + num_floors * wall_height
        
        if style == 'traditional' or style == 'kerala':
            # Sloped traditional roof
            house_objects.append({
                "name": "Roof_Main",
                "type": "pyramid",
                "position": [0, 0, roof_height + 0.8],
                "scale": [base_width + 2, base_length + 2, 1.6],
                "color": "#DC143C",
                "material": "roof_traditional"
            })
            
            # Add traditional roof details
            house_objects.append({
                "name": "Roof_Ridge",
                "type": "box",
                "position": [0, 0, roof_height + 1.5],
                "scale": [base_width + 2.5, 0.3, 0.2],
                "color": "#B22222",
                "material": "roof_detail"
            })
            
        elif style == 'rajasthani':
            # Flat roof with decorative elements
            house_objects.append({
                "name": "Roof_Main",
                "type": "box",
                "position": [0, 0, roof_height + 0.2],
                "scale": [base_width, base_length, 0.4],
                "color": "#CD853F",
                "material": "roof_rajasthani"
            })
            
            # Add domes/chhatris
            for i in range(2):
                house_objects.append({
                    "name": f"Chhatri_{i}",
                    "type": "sphere",
                    "position": [-base_width/3 + i * base_width*2/3, 0, roof_height + 1],
                    "scale": [1, 1, 1],
                    "color": "#DAA520",
                    "material": "dome"
                })
        else:
            # Modern flat roof
            house_objects.append({
                "name": "Roof_Main",
                "type": "box", 
                "position": [0, 0, roof_height + 0.1],
                "scale": [base_width + 0.2, base_length + 0.2, 0.2],
                "color": "#708090",
                "material": "roof_modern"
            })
        
        # Windows - more realistic placement
        window_height = 1.2
        for i in range(num_floors):
            floor_y = 0.5 + i * wall_height
            
            # Front windows
            for j in range(min(3, max(2, len(rooms)))):
                house_objects.append({
                    "name": f"Window_Front_{i}_{j}",
                    "type": "box",
                    "position": [base_width/2 + 0.05, -base_length/3 + j * base_length/3, floor_y + wall_height - 0.8],
                    "scale": [0.1, 1.2, window_height],
                    "color": "#87CEEB",
                    "material": "window"
                })
            
            # Side windows
            for j in range(2):
                house_objects.append({
                    "name": f"Window_Side_{i}_{j}",
                    "type": "box",
                    "position": [0, base_length/2 + 0.05, floor_y + wall_height - 0.8],
                    "scale": [1, 0.1, window_height],
                    "color": "#87CEEB",
                    "material": "window"
                })
        
        # Doors
        # Main entrance
        house_objects.append({
            "name": "Main_Door",
            "type": "box",
            "position": [base_width/2 + 0.05, 0, 1.2],
            "scale": [0.1, 1.2, 2.4],
            "color": "#8B4513",
            "material": "door"
        })
        
        # Door frame
        house_objects.append({
            "name": "Door_Frame",
            "type": "box",
            "position": [base_width/2 + 0.1, 0, 1.3],
            "scale": [0.2, 1.4, 2.6],
            "color": "#654321",
            "material": "door_frame"
        })
        
        # Add courtyard if mentioned
        if 'courtyard' in features:
            house_objects.append({
                "name": "Courtyard",
                "type": "box",
                "position": [0, -base_length - 3, 0.05],
                "scale": [base_width, 4, 0.1],
                "color": "#F4A460",
                "material": "courtyard"
            })
            
            # Courtyard pillars
            for i in range(4):
                house_objects.append({
                    "name": f"Pillar_{i}",
                    "type": "cylinder",
                    "position": [-base_width/3 + i * base_width/3, -base_length - 1, 1.5],
                    "scale": [0.3, 0.3, 3],
                    "color": "#D2B48C",
                    "material": "pillar"
                })
        
        # Add garden if mentioned
        if 'garden' in features:
            for i in range(5):
                for j in range(3):
                    house_objects.append({
                        "name": f"Tree_{i}_{j}",
                        "type": "sphere",
                        "position": [base_width + 2 + i * 2, -base_length/2 + j * base_length/2, 2],
                        "scale": [1.5, 1.5, 1.5],
                        "color": "#228B22",
                        "material": "tree"
                    })
        
        return {
            "objects": house_objects,
            "camera": {
                "position": [base_width * 1.8, -base_length * 1.5, roof_height + 5],
                "target": [0, 0, roof_height/2]
            },
            "lighting": {
                "sun": {
                    "position": [base_width * 2, base_length * 2, roof_height + 10],
                    "intensity": 1.2
                },
                "ambient": {
                    "intensity": 0.4
                }
            },
            "metadata": {
                "style": style,
                "house_type": house_type,
                "floors": num_floors,
                "dimensions": f"{base_width}x{base_length}m",
                "features": features,
                "total_objects": len(house_objects)
            }
        }

# Initialize components
parser = AdvancedHouseParser()
blender_gen = SimpleBlenderGenerator()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "Simple ML House Generator",
        "version": "1.0",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/generate', methods=['POST'])
def generate_house():
    try:
        data = request.get_json()
        
        if not data or 'description' not in data:
            return jsonify({
                "success": False,
                "error": "Missing 'description' in request body"
            }), 400
        
        description = data['description']
        print(f"Generating house: {description}")
        
        # Parse the description
        start_time = time.time()
        attributes = parser.parse_text(description)
        
        # Generate output name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_name = f"house_{timestamp}"
        
        # Create script
        script_path = os.path.join(config.output_dir, f"{output_name}_script.py")
        blend_path = os.path.join(config.output_dir, f"{output_name}.blend")
        
        script = blender_gen.generate_basic_script(attributes, blend_path)
        
        # Save script
        with open(script_path, 'w') as f:
            f.write(script)
        
        # Generate 3D data for web viewer
        threejs_data = blender_gen.generate_threejs_data(attributes)
        threejs_path = os.path.join(config.output_dir, f"{output_name}_3d.json")
        
        with open(threejs_path, 'w') as f:
            json.dump(threejs_data, f, indent=2)
        
        # Create metadata
        metadata = {
            'description': description,
            'attributes': attributes,
            'generated_at': datetime.now().isoformat(),
            'files': {
                'script': f"{output_name}_script.py",
                'blend': f"{output_name}.blend",
                'threejs': f"{output_name}_3d.json"
            }
        }
        
        metadata_path = os.path.join(config.output_dir, f"{output_name}_metadata.json")
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        processing_time = time.time() - start_time
        
        return jsonify({
            "success": True,
            "message": "House generated successfully",
            "data": {
                "files": [
                    {
                        "name": f"{output_name}_script.py",
                        "type": "Python Script",
                        "url": f"/files/{output_name}_script.py",
                        "path": script_path
                    },
                    {
                        "name": f"{output_name}_metadata.json", 
                        "type": "Metadata",
                        "url": f"/files/{output_name}_metadata.json",
                        "path": metadata_path
                    },
                    {
                        "name": f"{output_name}_3d.json",
                        "type": "3D Model",
                        "url": f"/files/{output_name}_3d.json", 
                        "path": threejs_path
                    }
                ],
                "attributes": attributes,
                "processing_time": round(processing_time, 4),
                "output_directory": config.output_dir,
                "model_data": threejs_data
            }
        })
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/generate-form', methods=['POST'])
def generate_house_from_form():
    """Generate house from structured form data"""
    try:
        data = request.get_json()
        
        # Extract form data
        house_config = {
            'style': data.get('style', 'modern'),
            'house_type': data.get('house_type', 'bungalow'),
            'floors': int(data.get('floors', 2)),
            'bedrooms': int(data.get('bedrooms', 3)),
            'bathrooms': int(data.get('bathrooms', 2)),
            'rooms': data.get('rooms', []),
            'features': data.get('features', []),
            'colors': data.get('colors', ['white']),
            'materials': data.get('materials', ['brick']),
            'windows': data.get('windows', {}),
            'doors': data.get('doors', {}),
            'budget': data.get('budget', 'standard'),
            'area': data.get('area', {'width': 12, 'length': 15})
        }
        
        print(f"🏗️ Generating house from form: {house_config}")
        
        start_time = time.time()
        
        # Create comprehensive attributes
        attributes = {
            'text': f"Custom {house_config['style']} {house_config['house_type']}",
            'num_floors': house_config['floors'],
            'style': house_config['style'],
            'house_type': house_config['house_type'],
            'rooms': house_config['rooms'],
            'room_count': {
                'bedrooms': house_config['bedrooms'],
                'bathrooms': house_config['bathrooms']
            },
            'features': house_config['features'],
            'materials': house_config['materials'],
            'colors': house_config['colors'],
            'windows': house_config['windows'],
            'doors': house_config['doors'],
            'budget_tier': house_config['budget'],
            'dimensions': {
                'width': house_config['area']['width'],
                'length': house_config['area']['length'],
                'height': 3.2
            }
        }
        
        # Generate files
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_name = f"house_form_{timestamp}"
        
        script_path = os.path.join(config.output_dir, f"{output_name}_script.py")
        threejs_path = os.path.join(config.output_dir, f"{output_name}_3d.json")
        
        # Generate Blender script
        script = blender_gen.generate_basic_script(attributes, script_path.replace('_script.py', '.blend'))
        with open(script_path, 'w') as f:
            f.write(script)
        
        # Generate 3D data
        threejs_data = blender_gen.generate_threejs_data(attributes)
        with open(threejs_path, 'w') as f:
            json.dump(threejs_data, f, indent=2)
        
        # Create metadata
        metadata = {
            'description': f"Form-generated {house_config['style']} {house_config['house_type']}",
            'form_config': house_config,
            'attributes': attributes,
            'generated_at': datetime.now().isoformat(),
            'files': {
                'script': f"{output_name}_script.py",
                'threejs': f"{output_name}_3d.json"
            }
        }
        
        metadata_path = os.path.join(config.output_dir, f"{output_name}_metadata.json")
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        processing_time = time.time() - start_time
        
        return jsonify({
            "success": True,
            "message": "House generated successfully from form",
            "data": {
                "files": [
                    {
                        "name": f"{output_name}_script.py",
                        "type": "Python Script",
                        "url": f"/files/{output_name}_script.py",
                        "path": script_path
                    },
                    {
                        "name": f"{output_name}_metadata.json",
                        "type": "Metadata", 
                        "url": f"/files/{output_name}_metadata.json",
                        "path": metadata_path
                    },
                    {
                        "name": f"{output_name}_3d.json",
                        "type": "3D Model",
                        "url": f"/files/{output_name}_3d.json",
                        "path": threejs_path
                    }
                ],
                "attributes": attributes,
                "form_config": house_config,
                "processing_time": round(processing_time, 4),
                "output_directory": config.output_dir,
                "model_data": threejs_data
            }
        })
        
    except Exception as e:
        print(f"Error in form generation: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/config-options', methods=['GET'])
def get_config_options():
    """Get all available configuration options for the form"""
    return jsonify({
        "success": True,
        "options": {
            "styles": list(parser.styles.keys()),
            "house_types": list(parser.house_types.keys()),
            "room_types": list(parser.room_types.keys()),
            "features": list(parser.features.keys()),
            "materials": list(parser.materials.keys()),
            "colors": list(parser.colors.keys()),
            "window_styles": ['standard', 'bay', 'french', 'jharokha'],
            "door_types": ['wooden', 'glass', 'metal'],
            "budget_tiers": ['budget', 'standard', 'luxury'],
            "orientations": ['north', 'south', 'east', 'west', 'auto']
        }
    })

@app.route('/examples', methods=['GET'])
def get_examples():
    examples = [
        {
            "id": "modern_villa",
            "name": "Modern Villa",
            "description": "modern 2 floor villa with 4 bedrooms, living room, kitchen, 2 bathrooms, balcony, parking"
        },
        {
            "id": "kerala_house",
            "name": "Kerala Traditional",
            "description": "traditional Kerala house with courtyard, sloped roof, veranda, 3 bedrooms"
        },
        {
            "id": "rajasthani_haveli",
            "name": "Rajasthani Haveli",
            "description": "Rajasthani haveli with courtyard, 2 floors, 5 bedrooms, traditional design"
        }
    ]
    
    return jsonify({
        "success": True,
        "examples": examples
    })

@app.route('/styles', methods=['GET'])
def get_styles():
    return jsonify({
        "success": True,
        "styles": parser.styles,
        "house_types": parser.house_types,
        "room_types": parser.rooms,
        "features": parser.features
    })

@app.route('/files/<filename>', methods=['GET'])
def serve_file(filename):
    try:
        file_path = os.path.join(config.output_dir, filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({
                "success": False,
                "error": "File not found"
            }), 404
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🏛️  SIMPLE ML HOUSE GENERATOR")
    print("="*70)
    print("🌐 Starting server on http://localhost:5001")
    print("📚 Available endpoints:")
    print("  GET  /health     - Health check")
    print("  POST /generate   - Generate house")
    print("  GET  /examples   - Get examples")
    print("  GET  /styles     - Get available options")
    print("="*70 + "\n")
    
    app.run(host='0.0.0.0', port=5001, debug=True)