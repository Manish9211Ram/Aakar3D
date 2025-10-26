@echo off
REM ============================================================================
REM AAKAR3D ML SERVICE SETUP SCRIPT (Windows)
REM Automated setup for Indian House Text-to-Blender Generator
REM ============================================================================

echo ================================================================================
echo 🏛️  AAKAR3D ML SERVICE SETUP
echo    Indian House Text-to-Blender Generator Integration
echo ================================================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version') do set python_version=%%i
echo ✓ Python version: %python_version%

REM Navigate to ml-service directory
cd ml-service

echo.
echo 📦 Setting up Python virtual environment...

REM Create virtual environment
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate.bat

echo ✓ Virtual environment created and activated

echo.
echo 📚 Installing Python dependencies...

REM Upgrade pip
python -m pip install --upgrade pip

REM Install PyTorch (CPU version by default)
echo Installing PyTorch...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

REM Install other ML dependencies
echo Installing ML dependencies...
pip install transformers sentence-transformers accelerate

REM Install 3D processing libraries
echo Installing 3D processing libraries...
pip install open3d trimesh pymeshlab

REM Install computer vision libraries
echo Installing computer vision libraries...
pip install opencv-python-headless Pillow scikit-image

REM Install scientific computing libraries
echo Installing scientific computing libraries...
pip install numpy scipy scikit-learn matplotlib pandas

REM Install web framework
echo Installing web framework...
pip install flask flask-cors requests

REM Install utilities
echo Installing utilities...
pip install huggingface_hub tqdm python-dotenv

echo ✓ All dependencies installed successfully

echo.
echo 🔧 Setting up Blender integration...

REM Check if Blender is installed
blender --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Blender not found in PATH
    echo    Please install Blender and add it to your system PATH
    echo    Download from: https://www.blender.org/download/
) else (
    echo ✓ Blender found in PATH
)

echo.
echo 📁 Creating output directories...

REM Create output directories
if not exist "indian_house_blender_output" mkdir indian_house_blender_output
if not exist "..\backend\uploads\ml-generated" mkdir "..\backend\uploads\ml-generated"

echo ✓ Output directories created

echo.
echo 🧪 Testing ML service...

REM Test the ML service
python -c "
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

if errorlevel 1 (
    echo ❌ ML service test failed
    pause
    exit /b 1
)

echo ✓ ML service test successful

echo.
echo 🌐 Backend integration setup...

REM Navigate to backend directory
cd ..\backend

REM Check if package.json exists
if exist "package.json" (
    echo ✓ Express.js backend found
    
    REM Install axios and multer
    echo Installing backend dependencies...
    npm install axios multer
    
    echo ✓ Backend dependencies updated
) else (
    echo ⚠️  Backend package.json not found
    echo    Please ensure you're in the correct directory
)

echo.
echo ⚛️  Frontend integration setup...

REM Navigate to frontend directory
cd ..\frontend

REM Check if package.json exists
if exist "package.json" (
    echo ✓ React frontend found
    
    REM Install axios
    echo Installing frontend dependencies...
    npm install axios
    
    echo ✓ Frontend dependencies updated
) else (
    echo ⚠️  Frontend package.json not found
    echo    Please ensure you're in the correct directory
)

echo.
echo ================================================================================
echo 🎉 SETUP COMPLETE!
echo ================================================================================
echo.
echo 📝 Next Steps:
echo.
echo 1. 🚀 Start the ML service:
echo    cd ml-service
echo    venv\Scripts\activate
echo    python api/app.py
echo.
echo 2. 🔧 Start the backend server:
echo    cd backend
echo    npm start
echo.
echo 3. ⚛️  Start the frontend:
echo    cd frontend
echo    npm start
echo.
echo 4. 🌐 Access the application:
echo    Frontend: http://localhost:3000
echo    Backend API: http://localhost:5000
echo    ML Service: http://localhost:5001
echo.
echo 💡 Usage Examples:
echo    • "modern 2 floor villa with 4 bedrooms, balcony, parking"
echo    • "traditional Kerala house with courtyard and sloped roof"
echo    • "Rajasthani haveli with jali work and dome"
echo.
echo 📚 Documentation:
echo    • ML Integration Plan: ML_INTEGRATION_PLAN.md
echo    • API Documentation: ml-service/api/app.py
echo    • Frontend Component: frontend/src/components/MLGenerator.js
echo.
echo ================================================================================

pause