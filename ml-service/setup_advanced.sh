#!/bin/bash
echo "========================================"
echo "  AAKAR3D ML SERVICE SETUP (ADVANCED)"
echo "========================================"

echo ""
echo "🔧 Installing advanced ML requirements..."
pip install -r requirements_advanced.txt

echo ""
echo "📦 Installing spacy model..."
python -m spacy download en_core_web_sm

echo ""
echo "🧪 Testing imports..."
python -c "import open3d; print('✅ Open3D installed')"
python -c "import trimesh; print('✅ Trimesh installed')"
python -c "import spacy; print('✅ Spacy installed')"

echo ""
echo "🚀 Starting advanced ML service..."
python advanced_app.py