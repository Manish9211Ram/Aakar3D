# 🤖 ML Service for Aakar3D

## 📁 Folder Structure
```
ml-service/
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── main.py               # Main application entry point
├── config.py             # Configuration settings
├── models/               # Trained ML models
│   ├── model_files_here
│   └── model_config.json
├── utils/                # Utility functions
│   ├── preprocessing.py
│   ├── postprocessing.py
│   └── helpers.py
├── api/                  # API related files
│   ├── endpoints.py
│   ├── schemas.py
│   └── middleware.py
└── tests/               # Test files
    ├── test_model.py
    └── test_api.py
```

## 🚀 Setup Instructions
1. Install dependencies: `pip install -r requirements.txt`
2. Run the service: `python main.py`
3. API will be available at: `http://localhost:8000`

## 📡 API Endpoints
- `POST /predict` - Main prediction endpoint
- `GET /health` - Health check
- `GET /model-info` - Model information

## 🔧 Integration with Aakar3D
This ML service integrates with the main Aakar3D application through REST API calls.