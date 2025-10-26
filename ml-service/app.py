#!/usr/bin/env python3
"""
Aakar3D ML House Generator - Hackathon Version
Enhanced to generate DIFFERENT house models based on user input
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import json
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Ensure output directory exists
os.makedirs('output', exist_ok=True)

class AdvancedHouseGenerator:
    def __init__(self):
        """Initialize the advanced house generator with comprehensive knowledge"""
        
        self.architectural_styles = {
            'modern': {
                'description': 'Clean lines, large windows, flat roofs',
                'roof_type': 'flat',
                'materials': ['glass', 'steel', 'concrete'],
                'colors': ['white', 'gray', 'black']
            },
            'traditional': {
                'description': 'Classic Indian architecture',
                'roof_type': 'sloped',
                'materials': ['brick', 'wood', 'tile'],
                'colors': ['red', 'brown', 'cream']
            },
            'kerala': {
                'description': 'Traditional Kerala style with sloped roofs',
                'roof_type': 'steep_slope',
                'materials': ['wood', 'tile', 'laterite'],
                'colors': ['brown', 'red', 'cream']
            },
            'rajasthani': {
                'description': 'Royal Rajasthani with domes and arches',
                'roof_type': 'dome',
                'materials': ['sandstone', 'marble'],
                'colors': ['golden', 'red', 'cream']
            },
            'contemporary': {
                'description': 'Mix of traditional and modern',
                'roof_type': 'mixed',
                'materials': ['glass', 'wood', 'stone'],
                'colors': ['white', 'brown', 'gray']
            }
        }
        
        self.house_types = {
            'villa': {'size_multiplier': 1.2, 'floors': [2, 3]},
            'bungalow': {'size_multiplier': 1.0, 'floors': [1]},
            'cottage': {'size_multiplier': 0.8, 'floors': [1, 2]},
            'mansion': {'size_multiplier': 1.8, 'floors': [2, 3, 4]},
            'apartment': {'size_multiplier': 0.6, 'floors': [1]},
            'townhouse': {'size_multiplier': 0.9, 'floors': [2, 3]},
            'farmhouse': {'size_multiplier': 1.4, 'floors': [1, 2]},
            'palace': {'size_multiplier': 2.0, 'floors': [3, 4]},
            'haveli': {'size_multiplier': 1.6, 'floors': [2, 3]}
        }
        
        self.room_types = [
            'bedroom', 'living_room', 'kitchen', 'bathroom', 'dining_room',
            'study_room', 'guest_room', 'master_bedroom', 'balcony', 'terrace',
            'garage', 'store_room', 'prayer_room', 'garden', 'courtyard'
        ]
        
        self.features = [
            'swimming_pool', 'garden', 'parking', 'security', 'elevator',
            'air_conditioning', 'solar_panels', 'water_tank', 'compound_wall',
            'gate', 'intercom', 'cctv', 'inverter', 'generator', 'balcony',
            'terrace', 'courtyard', 'fountain'
        ]
        
        self.colors = [
            'white', 'cream', 'beige', 'brown', 'red', 'blue', 'green',
            'yellow', 'orange', 'pink', 'grey', 'black', 'golden', 'silver'
        ]

    def parse_text_description(self, description):
        """Parse text description to extract house attributes"""
        desc_lower = description.lower()
        
        # Detect style
        style = 'modern'  # default
        for style_name in self.architectural_styles.keys():
            if style_name in desc_lower:
                style = style_name
                break
        
        # Detect house type
        house_type = 'villa'  # default
        for type_name in self.house_types.keys():
            if type_name in desc_lower:
                house_type = type_name
                break
        
        # Detect floors
        floors = 2  # default
        for i in range(1, 6):
            if f'{i} floor' in desc_lower or f'{i} story' in desc_lower or f'{i} storey' in desc_lower:
                floors = i
                break
        
        # Detect size keywords
        size = 'medium'
        if any(word in desc_lower for word in ['small', 'tiny', 'compact']):
            size = 'small'
        elif any(word in desc_lower for word in ['large', 'big', 'spacious']):
            size = 'large'
        elif any(word in desc_lower for word in ['huge', 'massive', 'enormous']):
            size = 'very_large'
        
        # Detect colors
        detected_colors = []
        for color in self.colors:
            if color in desc_lower:
                detected_colors.append(color)
        if not detected_colors:
            detected_colors = ['white']  # default
        
        # Detect rooms
        detected_rooms = []
        for room in self.room_types:
            if room.replace('_', ' ') in desc_lower or room in desc_lower:
                detected_rooms.append(room)
        
        # Detect features
        detected_features = []
        for feature in self.features:
            if feature.replace('_', ' ') in desc_lower or feature in desc_lower:
                detected_features.append(feature)
        
        return {
            'style': style,
            'house_type': house_type,
            'floors': floors,
            'size': size,
            'colors': detected_colors,
            'rooms': detected_rooms,
            'features': detected_features,
            'original_description': description
        }

    def generate_3d_model_data(self, attributes):
        """Generate varied 3D model data based on attributes"""
        
        # Size affects dimensions significantly
        size_multipliers = {
            'small': 0.6, 'medium': 1.0, 'large': 1.4, 'very_large': 1.8
        }
        multiplier = size_multipliers.get(attributes['size'], 1.0)
        
        # House type affects dimensions
        house_config = self.house_types.get(attributes['house_type'], self.house_types['villa'])
        type_multiplier = house_config['size_multiplier']
        
        # Calculate base dimensions with variation
        base_width = random.uniform(6, 10) * multiplier * type_multiplier
        base_length = random.uniform(8, 12) * multiplier * type_multiplier
        floor_height = 3.0 + random.random() * 1.0
        total_height = attributes['floors'] * floor_height
        
        style = attributes['style']
        objects = []
        
        # Main building structure varies by style
        main_color = self._get_color_hex(attributes['colors'][0]) if attributes['colors'] else '#FFFFFF'
        
        if style == 'modern':
            # Modern: Geometric blocks
            objects.append({
                'type': 'box',
                'dimensions': {'width': base_width, 'height': total_height, 'depth': base_length},
                'position': {'x': 0, 'y': total_height/2, 'z': 0},
                'material': 'wall',
                'color': main_color
            })
            
            # Additional modern elements
            if attributes['floors'] > 1:
                objects.append({
                    'type': 'box',
                    'dimensions': {'width': base_width*0.7, 'height': floor_height, 'depth': base_length*0.6},
                    'position': {'x': base_width*0.3, 'y': total_height + floor_height/2, 'z': 0},
                    'material': 'wall',
                    'color': main_color
                })
                
        elif style == 'rajasthani':
            # Rajasthani: Multi-level with domes
            objects.append({
                'type': 'box',
                'dimensions': {'width': base_width, 'height': total_height*0.7, 'depth': base_length},
                'position': {'x': 0, 'y': total_height*0.35, 'z': 0},
                'material': 'wall',
                'color': '#F4A460'
            })
            
            # Upper level
            objects.append({
                'type': 'box',
                'dimensions': {'width': base_width*0.8, 'height': total_height*0.3, 'depth': base_length*0.8},
                'position': {'x': 0, 'y': total_height*0.85, 'z': 0},
                'material': 'wall',
                'color': '#F4A460'
            })
            
            # Dome
            objects.append({
                'type': 'sphere',
                'radius': base_width*0.2,
                'position': {'x': 0, 'y': total_height + base_width*0.2, 'z': 0},
                'material': 'dome',
                'color': '#DAA520'
            })
            
        else:
            # Traditional/Kerala/Contemporary
            objects.append({
                'type': 'box',
                'dimensions': {'width': base_width, 'height': total_height, 'depth': base_length},
                'position': {'x': 0, 'y': total_height/2, 'z': 0},
                'material': 'wall',
                'color': main_color
            })
        
        # Roof based on style
        if style == 'modern':
            # Flat roof
            objects.append({
                'type': 'box',
                'dimensions': {'width': base_width + 0.5, 'height': 0.3, 'depth': base_length + 0.5},
                'position': {'x': 0, 'y': total_height + 0.15, 'z': 0},
                'material': 'roof_modern',
                'color': '#708090'
            })
        elif style != 'rajasthani':
            # Sloped roof
            roof_color = '#DC143C' if style == 'traditional' else '#8B4513'
            objects.append({
                'type': 'pyramid',
                'radius': max(base_width, base_length) * 0.7,
                'height': 2.5,
                'position': {'x': 0, 'y': total_height + 1.25, 'z': 0},
                'material': 'roof_traditional',
                'color': roof_color
            })
        
        # Windows - vary by floors and size
        windows_per_floor = min(int(base_width / 3), 4)
        window_size = 1.2
        
        for floor in range(attributes['floors']):
            floor_y = floor * floor_height + floor_height * 0.6
            
            for i in range(windows_per_floor):
                x_pos = -base_width/2 + (i + 1) * base_width/(windows_per_floor + 1)
                objects.append({
                    'type': 'box',
                    'dimensions': {'width': window_size, 'height': window_size, 'depth': 0.1},
                    'position': {'x': x_pos, 'y': floor_y, 'z': base_length/2 + 0.05},
                    'material': 'window',
                    'color': '#87CEEB'
                })
        
        # Door
        door_width = 1.0 + random.random() * 0.5
        door_height = 2.0 + random.random() * 0.5
        objects.append({
            'type': 'box',
            'dimensions': {'width': door_width, 'height': door_height, 'depth': 0.1},
            'position': {'x': 0, 'y': door_height/2, 'z': base_length/2 + 0.05},
            'material': 'door',
            'color': '#8B4513'
        })
        
        # Add features based on detected features
        if 'garden' in attributes['features']:
            for i in range(random.randint(2, 5)):
                x = random.uniform(-base_width*1.5, base_width*1.5)
                z = random.uniform(-base_length*1.5, base_length*1.5)
                if abs(x) > base_width/2 + 2 and abs(z) > base_length/2 + 2:
                    objects.append({
                        'type': 'cylinder',
                        'radiusTop': 0.3,
                        'radiusBottom': 0.3,
                        'height': 4,
                        'position': {'x': x, 'y': 2, 'z': z},
                        'material': 'tree',
                        'color': '#228B22'
                    })
        
        if 'swimming_pool' in attributes['features']:
            objects.append({
                'type': 'box',
                'dimensions': {'width': 6, 'height': 0.5, 'depth': 4},
                'position': {'x': base_width + 4, 'y': -0.25, 'z': 0},
                'material': 'window',
                'color': '#0080FF'
            })
        
        if 'parking' in attributes['features'] or 'garage' in attributes['features']:
            objects.append({
                'type': 'box',
                'dimensions': {'width': 4, 'height': 3, 'depth': 6},
                'position': {'x': -base_width/2 - 2, 'y': 1.5, 'z': base_length/2 - 1},
                'material': 'wall',
                'color': '#C0C0C0'
            })
        
        # House type specific modifications
        house_type = attributes.get('house_type', 'villa')
        if house_type == 'bungalow':
            for obj in objects:
                if obj['type'] == 'box' and 'height' in obj['dimensions']:
                    obj['dimensions']['height'] = min(obj['dimensions']['height'], 4)
        elif house_type == 'mansion' or house_type == 'palace':
            for obj in objects:
                if obj['type'] == 'box' and 'height' in obj['dimensions']:
                    obj['dimensions']['height'] *= 1.3
                    obj['dimensions']['width'] *= 1.2
        
        return {
            'type': 'house_model',
            'style': style,
            'attributes': attributes,
            'objects': objects,
            'metadata': {
                'total_objects': len(objects),
                'base_dimensions': f"{base_width:.1f}x{base_length:.1f}x{total_height:.1f}",
                'generation_strategy': 'attribute_based_variation',
                'timestamp': datetime.now().isoformat()
            }
        }

    def _get_color_hex(self, color_name):
        """Convert color name to hex"""
        color_map = {
            'white': '#FFFFFF', 'cream': '#F5F5DC', 'beige': '#F5F5DC',
            'brown': '#8B4513', 'red': '#DC143C', 'blue': '#0077BE',
            'green': '#228B22', 'yellow': '#FFD700', 'orange': '#FF8C00',
            'pink': '#FFC0CB', 'grey': '#808080', 'gray': '#808080',
            'black': '#2F2F2F', 'golden': '#FFD700', 'silver': '#C0C0C0'
        }
        return color_map.get(color_name.lower(), '#FFFFFF')

    def generate_house(self, description):
        """Main function to generate house from description"""
        try:
            logger.info(f"Generating house for: {description}")
            
            # Parse the description
            attributes = self.parse_text_description(description)
            logger.info(f"Parsed attributes: {attributes}")
            
            # Generate 3D model data
            model_data = self.generate_3d_model_data(attributes)
            
            # Create timestamp for unique identification
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Save model data to file
            output_file = f"output/house_{timestamp}_3d.json"
            with open(output_file, 'w') as f:
                json.dump(model_data, f, indent=2)
            
            # Save metadata
            metadata = {
                'timestamp': timestamp,
                'description': description,
                'attributes': attributes,
                'model_file': output_file,
                'generated_at': datetime.now().isoformat()
            }
            
            metadata_file = f"output/house_{timestamp}_metadata.json"
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            logger.info(f"House generated successfully: {output_file}")
            
            return {
                'success': True,
                'model_data': model_data,
                'attributes': attributes,
                'metadata': metadata,
                'files': {
                    'model': output_file,
                    'metadata': metadata_file
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating house: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

# Initialize the generator
house_generator = AdvancedHouseGenerator()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Aakar3D ML House Generator',
        'version': '2.0.0',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/generate', methods=['POST'])
def generate_house():
    """Generate house from text description"""
    try:
        data = request.get_json()
        description = data.get('description', '')
        
        if not description:
            return jsonify({
                'success': False,
                'error': 'Description is required'
            }), 400
        
        logger.info(f"Generating house: {description}")
        
        result = house_generator.generate_house(description)
        
        if result['success']:
            return jsonify({
                'success': True,
                'data': result['model_data'],
                'attributes': result['attributes'],
                'metadata': result['metadata']
            })
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 500
            
    except Exception as e:
        logger.error(f"Error in generate endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/generate_house_from_form', methods=['POST'])
def generate_house_from_form():
    """Generate house from form data"""
    try:
        form_data = request.get_json()
        
        # Convert form data to description
        description_parts = []
        
        if form_data.get('style'):
            description_parts.append(f"{form_data['style']} style")
        
        if form_data.get('house_type'):
            description_parts.append(f"{form_data['house_type']}")
        
        if form_data.get('floors'):
            description_parts.append(f"{form_data['floors']} floors")
        
        if form_data.get('colors'):
            colors = ', '.join(form_data['colors'])
            description_parts.append(f"with {colors} colors")
        
        if form_data.get('rooms'):
            rooms = ', '.join(form_data['rooms'])
            description_parts.append(f"including {rooms}")
        
        if form_data.get('features'):
            features = ', '.join(form_data['features'])
            description_parts.append(f"with {features}")
        
        description = ' '.join(description_parts)
        
        logger.info(f"Form generated description: {description}")
        
        result = house_generator.generate_house(description)
        
        if result['success']:
            return jsonify({
                'success': True,
                'data': result['model_data'],
                'attributes': result['attributes'],
                'metadata': result['metadata']
            })
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 500
            
    except Exception as e:
        logger.error(f"Error in form generate endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/config_options', methods=['GET'])
def get_config_options():
    """Get configuration options for the form"""
    return jsonify({
        'styles': list(house_generator.architectural_styles.keys()),
        'house_types': list(house_generator.house_types.keys()),
        'colors': house_generator.colors,
        'rooms': house_generator.room_types,
        'features': house_generator.features
    })

@app.route('/examples', methods=['GET'])
def get_examples():
    """Get example descriptions"""
    examples = [
        {
            'id': 1,
            'title': 'Modern Villa',
            'description': 'A modern 3-floor villa with white and gray colors, swimming pool, garden, and large windows'
        },
        {
            'id': 2,
            'title': 'Traditional Kerala House',
            'description': 'A traditional Kerala style house with 2 floors, brown wooden balcony, red tile roof, and courtyard'
        },
        {
            'id': 3,
            'title': 'Rajasthani Haveli',
            'description': 'A royal Rajasthani haveli with golden sandstone, domes, courtyard, and traditional arches'
        },
        {
            'id': 4,
            'title': 'Small Cottage',
            'description': 'A small cottage with 1 floor, garden, wooden doors, and cream colors'
        }
    ]
    
    return jsonify({
        'success': True,
        'examples': examples
    })

if __name__ == '__main__':
    print("=" * 70)
    print("🏛️  AAKAR3D PROPER ML HOUSE GENERATOR")
    print("=" * 70)
    print("🌐 Starting server on http://localhost:5001")
    print("📚 Available endpoints:")
    print("  GET  /health              - Health check")
    print("  POST /generate            - Generate house from text")
    print("  POST /generate_house_from_form - Generate from form data")
    print("  GET  /config_options      - Get configuration options")
    print("  GET  /examples            - Get example descriptions")
    print("=" * 70)
    
    app.run(host='0.0.0.0', port=5001, debug=True)