# 🏛️ Aakar3D Advanced ML Service

Professional 3D house generation with real model creation using Open3D and advanced NLP.

## 🚀 Features

### ✨ Advanced 3D Generation
- **Real 3D Models**: Generates actual PLY, OBJ, GLTF, and STL files
- **Procedural Architecture**: Rule-based 3D model creation
- **Multiple Formats**: Web-friendly GLTF, 3D printing STL, and more
- **Realistic Materials**: Color variation and material properties

### 🧠 Intelligent Text Processing
- **Advanced NLP**: Using spaCy for semantic understanding
- **Style Detection**: Recognizes 8+ architectural styles
- **Context Awareness**: Understands room types, features, dimensions
- **Confidence Scoring**: Provides accuracy metrics

### 🏗️ Supported Architectures
1. **Modern** - Clean, minimalist design
2. **Traditional** - Classic Indian architecture  
3. **Kerala Style** - Traditional Kerala with sloped roofs
4. **Rajasthani** - Royal style with domes and carvings
5. **Bengali** - Cultural artistic designs
6. **Punjabi** - Farmhouse style
7. **South Indian** - Dravidian temple architecture
8. **Colonial** - British colonial bungalows

### 🏠 House Types
- Villa, Bungalow, Apartment, Cottage
- Farmhouse, Townhouse, Mansion, Duplex, Penthouse

## 📦 Installation

### Basic Setup (JSON generation only)
```bash
pip install flask flask-cors
python simple_app.py
```

### Advanced Setup (Real 3D models)
```bash
# Install advanced requirements
pip install -r requirements_advanced.txt

# Install spaCy model
python -m spacy download en_core_web_sm

# Run advanced service
python advanced_app.py
```

### Windows Quick Setup
```bash
setup_advanced.bat
```

### Linux/Mac Quick Setup
```bash
chmod +x setup_advanced.sh
./setup_advanced.sh
```

## 🎯 API Endpoints

### Generate from Text
```http
POST /generate
Content-Type: application/json

{
  "description": "A modern 3-floor villa with swimming pool and garden"
}
```

### Generate from Form
```http
POST /generate_house_from_form
Content-Type: application/json

{
  "style": "modern",
  "type": "villa", 
  "floors": 3,
  "rooms": ["bedroom", "kitchen", "living_room"],
  "features": ["swimming_pool", "garden"],
  "primaryColor": "white",
  "material": "concrete",
  "width": 15,
  "height": 12,
  "depth": 10
}
```

### Get Configuration Options
```http
GET /config_options
```

### Download 3D Files
```http
GET /download/{filename}.ply
GET /download/{filename}.obj
GET /download/{filename}.gltf
GET /download/{filename}.stl
```

## 📁 Generated Files

Each generation creates:
- **PLY file** - Point cloud format
- **OBJ file** - Wavefront 3D model
- **GLTF file** - Web-friendly 3D format
- **STL file** - 3D printing format
- **Metadata JSON** - Generation details

## 🔧 Advanced Features

### Real 3D Geometry Creation
```python
from models.advanced_3d_generator import Advanced3DGenerator

generator = Advanced3DGenerator()
result = generator.generate_house_3d({
    'style': 'modern',
    'floors': 2,
    'features': ['balcony', 'garden']
})
```

### Intelligent Text Parsing
```python
from models.intelligent_parser import IntelligentTextParser

parser = IntelligentTextParser()
attributes = parser.extract_detailed_attributes(
    "A traditional Kerala house with wooden balcony"
)
# Returns: {'style': 'kerala', 'features': ['balcony'], ...}
```

## 🎨 Customization Options

### Colors
White, Red, Blue, Green, Yellow, Brown, Orange, Pink, Purple, Grey, Black, Beige

### Materials  
Brick, Wood, Concrete, Stone, Glass, Metal, Marble, Granite, Bamboo, Tile

### Features
Swimming Pool, Garden, Balcony, Garage, Fireplace, Security, Solar Panels, Elevator

### Rooms
Bedroom, Living Room, Kitchen, Bathroom, Study, Dining Room, Guest Room, Kids Room

## 🧪 Testing

### Test Basic Generation
```bash
python -c "
import requests
response = requests.post('http://localhost:5001/generate', 
    json={'description': 'modern white villa'})
print(response.json())
"
```

### Test Advanced Features
```bash
python test_advanced.py
```

## 📊 Performance

- **Generation Time**: 2-5 seconds per model
- **File Sizes**: 50KB - 2MB depending on complexity
- **Supported Complexity**: Up to 10,000 vertices
- **Memory Usage**: ~100MB per generation

## 🔍 Troubleshooting

### Common Issues

**Import Error: No module named 'open3d'**
```bash
pip install open3d==0.17.0
```

**spaCy model not found**
```bash
python -m spacy download en_core_web_sm
```

**Generation fails silently**
- Check `/health` endpoint
- Verify all dependencies installed
- Check server logs for errors

### Dependencies
- Python 3.8+
- Open3D 0.17.0+
- Trimesh 3.23.5+
- spaCy 3.6.1+
- Flask 2.3.3+

## 📈 Roadmap

- [ ] Machine Learning training pipeline
- [ ] Texture mapping support  
- [ ] Animation generation
- [ ] VR/AR export formats
- [ ] Cloud deployment
- [ ] Real-time collaboration

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- Open3D for 3D processing
- spaCy for NLP capabilities
- Trimesh for mesh operations
- Flask for web framework