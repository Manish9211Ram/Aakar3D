"""
Basic test for ML service without heavy dependencies
"""

from flask import Flask, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Indian House Blender Generator",
        "version": "3.0",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/test', methods=['GET'])
def test_basic():
    """Basic test endpoint"""
    return jsonify({
        "success": True,
        "message": "ML service basic test successful",
        "python_version": f"{os.sys.version}",
        "working_directory": os.getcwd()
    })

@app.route('/styles', methods=['GET'])
def get_styles():
    """Get available architectural styles"""
    styles = [
        'modern', 'traditional', 'colonial', 'contemporary',
        'kerala', 'rajasthani', 'bengali', 'south_indian'
    ]
    
    return jsonify({
        "success": True,
        "styles": styles,
        "message": "Styles loaded successfully"
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🏛️ BASIC ML SERVICE TEST")
    print("="*60)
    print("🌐 Starting server on http://localhost:5001")
    print("🔧 Test endpoints:")
    print("  GET /health - Health check")
    print("  GET /test - Basic functionality test")
    print("  GET /styles - Available styles")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=5001, debug=True)