"""
Flask API for Indian House Blender Generator
RESTful API for integrating with Aakar3D frontend
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import sys
import json
from datetime import datetime

# Add the ml-service directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our ML modules
from main import generate_house_api, quick_generate
from utils.config import IndianHouseBlenderConfig

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Initialize configuration
config = IndianHouseBlenderConfig()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Indian House Blender Generator",
        "version": "3.0",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/generate', methods=['POST'])
def generate_house():
    """
    Generate house from text description
    
    Expected JSON payload:
    {
        "description": "modern 2 floor villa with 4 bedrooms",
        "style": "modern",  // optional
        "floors": 2,        // optional
        "output_name": "my_house"  // optional
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'description' not in data:
            return jsonify({
                "success": False,
                "error": "Missing 'description' in request body"
            }), 400
        
        description = data['description']
        style = data.get('style')
        floors = data.get('floors')
        output_name = data.get('output_name')
        
        # Generate output directory for this request
        output_dir = os.path.join(config.output_dir, datetime.now().strftime("%Y%m%d_%H%M%S"))
        
        # Generate house
        result = generate_house_api(
            description=description,
            style=style,
            floors=floors,
            output_dir=output_dir
        )
        
        if result['success']:
            return jsonify({
                "success": True,
                "message": "House generated successfully",
                "data": {
                    "files": result['files'],
                    "attributes": result['attributes'],
                    "processing_time": result['processing_time']
                }
            })
        else:
            return jsonify({
                "success": False,
                "error": result.get('error', 'Unknown error')
            }), 500
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500

@app.route('/generate/examples', methods=['GET'])
def get_examples():
    """Get example house descriptions"""
    examples = [
        {
            "id": "kerala",
            "name": "Kerala Nalukettu",
            "description": "traditional Kerala nalukettu house with courtyard, sloped roof, veranda, 2 floors, 4 bedrooms, wooden pillars, red tiles",
            "style": "kerala",
            "image": "/static/examples/kerala.jpg"
        },
        {
            "id": "rajasthani",
            "name": "Rajasthani Haveli",
            "description": "Rajasthani haveli with jali work, courtyard, fountain, 3 floors, 6 bedrooms, dome, sandstone, terrace",
            "style": "rajasthani",
            "image": "/static/examples/rajasthani.jpg"
        },
        {
            "id": "modern",
            "name": "Modern Villa",
            "description": "modern 3 floor villa with glass facade, 5 bedrooms, terrace garden, swimming pool, parking, white and grey, 50x60 feet",
            "style": "modern",
            "image": "/static/examples/modern.jpg"
        },
        {
            "id": "colonial",
            "name": "Colonial Bungalow",
            "description": "colonial bungalow with pillars, veranda, 2 floors, 6 bedrooms, compound wall, garden, white with brown trim",
            "style": "colonial",
            "image": "/static/examples/colonial.jpg"
        }
    ]
    
    return jsonify({
        "success": True,
        "examples": examples
    })

@app.route('/generate/example/<example_id>', methods=['POST'])
def generate_example(example_id):
    """Generate house from predefined example"""
    examples = {
        "kerala": "traditional Kerala nalukettu house with courtyard, sloped roof, veranda, 2 floors, 4 bedrooms, wooden pillars, red tiles",
        "rajasthani": "Rajasthani haveli with jali work, courtyard, fountain, 3 floors, 6 bedrooms, dome, sandstone, terrace",
        "modern": "modern 3 floor villa with glass facade, 5 bedrooms, terrace garden, swimming pool, parking, white and grey, 50x60 feet",
        "colonial": "colonial bungalow with pillars, veranda, 2 floors, 6 bedrooms, compound wall, garden, white with brown trim"
    }
    
    if example_id not in examples:
        return jsonify({
            "success": False,
            "error": f"Example '{example_id}' not found"
        }), 404
    
    try:
        description = examples[example_id]
        output_dir = os.path.join(config.output_dir, f"example_{example_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        result = quick_generate(description, output_dir)
        
        if result['success']:
            return jsonify({
                "success": True,
                "message": f"Example '{example_id}' generated successfully",
                "data": {
                    "files": {
                        "blend_file": result['blend_file'],
                        "script_file": result['script_file'],
                        "metadata_file": result['metadata_file']
                    },
                    "attributes": result['attributes'],
                    "processing_time": result['processing_time']
                }
            })
        else:
            return jsonify({
                "success": False,
                "error": result.get('error', 'Unknown error')
            }), 500
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500

@app.route('/styles', methods=['GET'])
def get_styles():
    """Get available architectural styles"""
    return jsonify({
        "success": True,
        "styles": config.architectural_styles,
        "house_types": config.house_types,
        "roof_types": config.roof_types,
        "room_types": config.room_types,
        "features": config.feature_types
    })

@app.route('/download/<path:filename>', methods=['GET'])
def download_file(filename):
    """Download generated files"""
    try:
        file_path = os.path.join(config.output_dir, filename)
        
        if not os.path.exists(file_path):
            return jsonify({
                "success": False,
                "error": "File not found"
            }), 404
        
        return send_file(file_path, as_attachment=True)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Download error: {str(e)}"
        }), 500

@app.route('/status', methods=['GET'])
def get_status():
    """Get service status and configuration"""
    return jsonify({
        "success": True,
        "status": {
            "service": "Indian House Blender Generator API",
            "version": "3.0",
            "device": config.device,
            "output_directory": config.output_dir,
            "blender_executable": config.blender_executable,
            "supported_styles": len(config.architectural_styles),
            "supported_house_types": len(config.house_types),
            "supported_features": len(config.feature_types)
        }
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500

if __name__ == '__main__':
    print("\n" + "="*90)
    print("🚀 INDIAN HOUSE BLENDER GENERATOR API")
    print("="*90)
    print("🏠 API Endpoints:")
    print("  GET  /health                     - Health check")
    print("  POST /generate                   - Generate house from description")
    print("  GET  /generate/examples          - Get example descriptions")
    print("  POST /generate/example/<id>      - Generate from example")
    print("  GET  /styles                     - Get available styles/options")
    print("  GET  /download/<filename>        - Download generated files")
    print("  GET  /status                     - Get service status")
    print("="*90)
    print("🌐 Starting server on http://localhost:5001")
    print("="*90 + "\n")
    
    app.run(host='0.0.0.0', port=5001, debug=True)