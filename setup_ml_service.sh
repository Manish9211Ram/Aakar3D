#!/bin/bash

# ============================================================================
# AAKAR3D ML SERVICE SETUP SCRIPT
# Automated setup for Indian House Text-to-Blender Generator
# ============================================================================

echo "================================================================================"
echo "🏛️  AAKAR3D ML SERVICE SETUP"
echo "   Indian House Text-to-Blender Generator Integration"
echo "================================================================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✓ Python version: $python_version"

# Navigate to ml-service directory
cd ml-service

echo ""
echo "📦 Setting up Python virtual environment..."

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    source venv/Scripts/activate
else
    # Linux/Mac
    source venv/bin/activate
fi

echo "✓ Virtual environment created and activated"

echo ""
echo "📚 Installing Python dependencies..."

# Upgrade pip
pip install --upgrade pip

# Install PyTorch (CPU version by default)
echo "Installing PyTorch..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install other ML dependencies
echo "Installing ML dependencies..."
pip install transformers sentence-transformers accelerate

# Install 3D processing libraries
echo "Installing 3D processing libraries..."
pip install open3d trimesh pymeshlab

# Install computer vision libraries
echo "Installing computer vision libraries..."
pip install opencv-python-headless Pillow scikit-image

# Install scientific computing libraries
echo "Installing scientific computing libraries..."
pip install numpy scipy scikit-learn matplotlib pandas

# Install web framework
echo "Installing web framework..."
pip install flask flask-cors requests

# Install utilities
echo "Installing utilities..."
pip install huggingface_hub tqdm python-dotenv

echo "✓ All dependencies installed successfully"

echo ""
echo "🔧 Setting up Blender integration..."

# Check if Blender is installed
if command -v blender &> /dev/null; then
    echo "✓ Blender found in PATH"
    blender_path=$(which blender)
    echo "  Path: $blender_path"
else
    echo "⚠️  Blender not found in PATH"
    echo "   Please install Blender and add it to your system PATH"
    echo "   Download from: https://www.blender.org/download/"
fi

echo ""
echo "📁 Creating output directories..."

# Create output directories
mkdir -p indian_house_blender_output
mkdir -p ../backend/uploads/ml-generated

echo "✓ Output directories created"

echo ""
echo "🧪 Testing ML service..."

# Test the ML service
python3 -c "
try:
    from utils.config import IndianHouseBlenderConfig
    config = IndianHouseBlenderConfig()
    print('✓ Configuration loaded successfully')
    
    from models.text_parser import EnhancedIndianHouseParser
    parser = EnhancedIndianHouseParser(config)
    print('✓ Text parser loaded successfully')
    
    # Test parsing
    result = parser.parse_text('modern 2 floor house with 4 bedrooms')
    print('✓ Text parsing test successful')
    print(f'  Style: {result[\"style\"]}')
    print(f'  Floors: {result[\"num_floors\"]}')
    print(f'  Rooms: {len(result[\"rooms\"])} rooms detected')
    
except Exception as e:
    print(f'❌ Test failed: {e}')
    exit(1)
"

if [ $? -eq 0 ]; then
    echo "✓ ML service test successful"
else
    echo "❌ ML service test failed"
    exit 1
fi

echo ""
echo "🌐 Backend integration setup..."

# Navigate to backend directory
cd ../backend

# Check if package.json exists
if [ -f "package.json" ]; then
    echo "✓ Express.js backend found"
    
    # Install axios if not present
    if ! npm list axios &> /dev/null; then
        echo "Installing axios for ML service integration..."
        npm install axios
    fi
    
    # Install multer if not present
    if ! npm list multer &> /dev/null; then
        echo "Installing multer for file uploads..."
        npm install multer
    fi
    
    echo "✓ Backend dependencies updated"
else
    echo "⚠️  Backend package.json not found"
    echo "   Please ensure you're in the correct directory"
fi

echo ""
echo "⚛️  Frontend integration setup..."

# Navigate to frontend directory
cd ../frontend

# Check if package.json exists
if [ -f "package.json" ]; then
    echo "✓ React frontend found"
    
    # Install axios if not present
    if ! npm list axios &> /dev/null; then
        echo "Installing axios for API calls..."
        npm install axios
    fi
    
    echo "✓ Frontend dependencies updated"
else
    echo "⚠️  Frontend package.json not found"
    echo "   Please ensure you're in the correct directory"
fi

echo ""
echo "================================================================================"
echo "🎉 SETUP COMPLETE!"
echo "================================================================================"
echo ""
echo "📝 Next Steps:"
echo ""
echo "1. 🚀 Start the ML service:"
echo "   cd ml-service"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "   venv\\Scripts\\activate"
else
    echo "   source venv/bin/activate"
fi
echo "   python api/app.py"
echo ""
echo "2. 🔧 Start the backend server:"
echo "   cd backend"
echo "   npm start"
echo ""
echo "3. ⚛️  Start the frontend:"
echo "   cd frontend"
echo "   npm start"
echo ""
echo "4. 🌐 Access the application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:5000"
echo "   ML Service: http://localhost:5001"
echo ""
echo "💡 Usage Examples:"
echo '   • "modern 2 floor villa with 4 bedrooms, balcony, parking"'
echo '   • "traditional Kerala house with courtyard and sloped roof"'
echo '   • "Rajasthani haveli with jali work and dome"'
echo ""
echo "📚 Documentation:"
echo "   • ML Integration Plan: ML_INTEGRATION_PLAN.md"
echo "   • API Documentation: ml-service/api/app.py"
echo "   • Frontend Component: frontend/src/components/MLGenerator.js"
echo ""
echo "================================================================================"