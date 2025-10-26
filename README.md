# Aakar3D - AI-Powered Architecture Visualization Platform

🏗️ **A revolutionary 3D architecture visualization platform with AI-powered Indian house generation**

## 🌟 Features

### 🤖 AI/ML Integration (NEW!)
- 🏛️ **Text-to-3D House Generator** - Generate complete Indian house models from natural language descriptions
- 🎨 **Indian Architectural Styles** - Support for Kerala, Rajasthani, Colonial, Modern, and more styles
- 📐 **Intelligent Parsing** - Advanced NLP for extracting house features, dimensions, and specifications
- 🏗️ **Blender Integration** - Generates complete .blend files with materials, lighting, and camera setup
- 🔧 **Customizable Output** - Multiple floors, room types, architectural features, and landscaping
- 💾 **Export Ready** - Download .blend files, scripts, and metadata for further customization

### Frontend (React.js)
- ✨ **3D Logo Animation** - Rotating 3D logo with CSS animations and mouse parallax effects
- 🤖 **ML Generator Component** - Interactive interface for AI house generation
- 🎨 **Modern UI/UX** - Glassmorphism design with gradient backgrounds
- 🔐 **Authentication System** - Complete login/signup with JWT tokens
- 📱 **Responsive Design** - Works seamlessly across all devices
- 🎯 **Dashboard** - User dashboard with AI-powered 3D model functionality
- 🔄 **Real-time Validation** - Form validation with instant feedback

### Backend (Express.js + MongoDB)
- 🤖 **ML Service Integration** - RESTful API for AI house generation
- 🛡️ **Secure Authentication** - JWT-based auth with bcrypt password hashing
- 📊 **MongoDB Integration** - User management with Mongoose ODM
- 🔒 **Password Security** - Advanced encryption and validation
- 🌐 **CORS Enabled** - Cross-origin resource sharing configured
- ⚡ **RESTful API** - Clean API endpoints for all operations
- 🔄 **Auto-restart** - Nodemon for development hot reloading

## 🚀 Technology Stack

### Frontend
- **React.js** - Component-based UI library
- **CSS3** - Advanced animations and styling
- **JavaScript ES6+** - Modern JavaScript features
- **Axios** - HTTP client for API calls
- **Local Storage** - Client-side token storage

### Backend
- **Express.js** - Fast, minimalist web framework
- **MongoDB** - NoSQL database for user data
- **Mongoose** - MongoDB object modeling
- **JWT** - JSON Web Tokens for authentication
- **bcryptjs** - Password hashing library
- **CORS** - Cross-origin resource sharing
- **Axios** - HTTP client for ML service integration
- **Multer** - File upload middleware
- **Nodemon** - Development auto-restart

### 🤖 ML Service (NEW!)
- **Python 3.8+** - Core ML service language
- **PyTorch** - Deep learning framework
- **Transformers** - Hugging Face NLP models
- **DistilBERT** - Lightweight BERT for text processing
- **Open3D** - 3D data processing
- **Trimesh** - 3D mesh processing
- **OpenCV** - Computer vision library
- **Flask** - Python web framework for ML API
- **Blender Python API** - 3D content creation

## 📁 Project Structure

```
AAKAR/
├── frontend/                 # React.js frontend application
│   ├── public/              # Static assets
│   ├── src/
│   │   ├── components/      # React components
│   │   │   ├── Navbar.js    # Navigation component
│   │   │   ├── HeroSection.js # Landing page with 3D logo
│   │   │   ├── Dashboard.js # User dashboard
│   │   │   ├── MLGenerator.js # AI house generator interface
│   │   │   └── MLGenerator.css # ML component styles
│   │   ├── App.js           # Main app component
│   │   └── index.js         # React entry point
│   └── package.json         # Frontend dependencies
├── backend/                 # Express.js backend server
│   ├── config/              # Configuration files
│   ├── middleware/          # Custom middleware
│   ├── models/              # MongoDB models
│   ├── routes/              # API route handlers
│   │   ├── auth.js          # Authentication routes
│   │   └── ml.js            # ML service integration routes
│   ├── uploads/             # File upload storage
│   │   └── ml-generated/    # ML generated files
│   ├── server.js            # Server entry point
│   └── package.json         # Backend dependencies
├── ml-service/              # 🤖 AI/ML Service (NEW!)
│   ├── models/              # ML model definitions
│   │   ├── text_parser.py   # NLP text parsing
│   │   ├── blender_generator.py # Blender script generation
│   │   └── __init__.py
│   ├── utils/               # Utility functions
│   │   ├── config.py        # ML service configuration
│   │   └── __init__.py
│   ├── api/                 # ML API endpoints
│   │   ├── app.py           # Flask ML API server
│   │   ├── pipeline.py      # ML generation pipeline
│   │   └── __init__.py
│   ├── main.py              # Main ML service entry point
│   ├── requirements.txt     # Python dependencies
│   └── README.md            # ML service documentation
├── setup_ml_service.sh      # 🛠️ Automated setup script (Linux/Mac)
├── setup_ml_service.bat     # 🛠️ Automated setup script (Windows)
├── ML_INTEGRATION_PLAN.md   # 📋 Comprehensive ML integration documentation
└── README.md                # Project documentation
```
│   │   │   ├── Login.js     # Login form
│   │   │   └── Signup.js    # Registration form
│   │   ├── services/        # API services
│   │   │   └── authService.js # Authentication service
│   │   └── App.js           # Main application component
│   └── package.json         # Frontend dependencies
├── backend/                 # Express.js backend API
│   ├── node_modules/        # Backend dependencies (included)
│   ├── server.js            # Main server file
│   ├── package.json         # Backend dependencies
│   └── .env                 # Environment variables
└── README.md               # Project documentation
```

## 🔧 Installation & Setup

### Prerequisites
- **Node.js** (v14 or higher)
- **MongoDB** (local or cloud instance)
- **Python 3.8+** (for ML service)
- **Blender** (optional, for .blend file generation)
- **Git**

### 🚀 Quick Setup (Automated)

**Option 1: Use the automated setup script**

For Windows:
```bash
setup_ml_service.bat
```

For Linux/Mac:
```bash
chmod +x setup_ml_service.sh
./setup_ml_service.sh
```

This script will:
- ✅ Set up Python virtual environment
- ✅ Install all ML dependencies
- ✅ Configure Blender integration
- ✅ Install backend/frontend dependencies
- ✅ Run ML service tests
- ✅ Create necessary directories

### 🛠️ Manual Setup

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Install dependencies:**
   ```bash
   npm install axios multer  # ML integration dependencies
   npm install  # Install all other dependencies
   ```

3. **Create environment file:**
   ```bash
   # Create .env file in backend directory
   MONGODB_URI=mongodb://localhost:27017/aakar3d
   JWT_SECRET=your_super_secret_jwt_key_here_make_it_long_and_secure
   PORT=5000
   ML_SERVICE_URL=http://localhost:5001
   ```

4. **Start the backend server:**
   ```bash
   npm start
   # or for development
   npm run dev
   ```

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install axios  # For ML API calls
   npm install  # Install all other dependencies
   ```

3. **Start the frontend development server:**
   ```bash
   npm start
   ```

### 🤖 ML Service Setup

1. **Navigate to ML service directory:**
   ```bash
   cd ml-service
   ```

2. **Create Python virtual environment:**
   ```bash
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On Linux/Mac:
   source venv/bin/activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Start the ML service:**
   ```bash
   python api/app.py
   ```

### � Access the Application

Once all services are running:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000  
- **ML Service**: http://localhost:5001

## �🌐 API Endpoints

### Authentication
- `POST /api/signup` - User registration
- `POST /api/login` - User login
- `GET /api/profile` - Get user profile (protected)

### 🤖 ML Service Endpoints (NEW!)
- `GET /api/ml/health` - ML service health check
- `POST /api/ml/generate-house` - Generate house from text description
- `GET /api/ml/examples` - Get example house descriptions
- `POST /api/ml/generate-example/:id` - Generate from predefined example
- `GET /api/ml/styles` - Get available architectural styles
- `GET /api/ml/download/:filename` - Download generated files
- `POST /api/ml/bulk-generate` - Batch generation from multiple descriptions

### Request/Response Examples

#### Signup
```javascript
// POST /api/signup
{
  "fullName": "John Doe",
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securePassword123"
}
```

#### Login
```javascript
// POST /api/login
{
  "emailOrUsername": "john@example.com", // or "johndoe"
  "password": "securePassword123"
}
```

#### 🤖 Generate House (NEW!)
```javascript
// POST /api/ml/generate-house
{
  "description": "modern 2 floor villa with 4 bedrooms, balcony, swimming pool, white and glass facade, 40x50 feet",
  "style": "modern",        // optional
  "floors": 2,              // optional
  "outputName": "my_villa"  // optional
}

// Response
{
  "success": true,
  "message": "House generated successfully",
  "data": {
    "files": {
      "blend_file": "/path/to/house.blend",
      "script_file": "/path/to/script.py",
      "metadata_file": "/path/to/metadata.json"
    },
    "attributes": {
      "style": "modern",
      "num_floors": 2,
      "house_type": "villa",
      "rooms": ["bedroom", "living_room", "kitchen", "bathroom"],
      "features": ["balcony", "swimming_pool"],
      "dimensions": {"width": 12.192, "length": 15.24, "height": 3.0}
    },
    "processing_time": 45.67
  }
}
```

## 🏛️ ML Usage Examples

### Supported House Descriptions

**Modern Houses:**
```
"modern 3 floor villa with glass facade, 5 bedrooms, terrace garden, swimming pool, parking, white and grey, 50x60 feet"

"contemporary duplex with flat roof terrace garden, 6 bedrooms, study, 3 bathrooms, balconies, parking for 2 cars, cream colored"
```

**Traditional Indian Houses:**
```
"traditional Kerala nalukettu house with courtyard, sloped roof, veranda, 2 floors, 4 bedrooms, wooden pillars, red tiles"

"Rajasthani haveli with jali work, courtyard, fountain, 3 floors, 6 bedrooms, dome, sandstone, terrace"

"south Indian traditional house with courtyard, pillars, sloped roof, 2 floors, 4 bedrooms, puja room, terracotta tiles"
```

**Colonial Style:**
```
"colonial bungalow with pillars, veranda, 3 floors, 8 bedrooms, dining hall, compound wall, garden, white with brown accents"
```

### Supported Features
- **Architectural Styles**: Modern, Traditional, Kerala, Rajasthani, Colonial, Contemporary, etc.
- **Room Types**: Bedrooms, Living room, Kitchen, Bathroom, Puja room, Study, etc.
- **Features**: Balcony, Terrace, Courtyard, Swimming pool, Garden, Parking, etc.
- **Materials**: Concrete, Brick, Wood, Stone, Glass, etc.
- **Colors**: White, Cream, Brown, Red, Blue, etc.

## 🎨 UI Features

### 🤖 AI House Generator (NEW!)
- **Interactive Interface** - User-friendly text input for house descriptions
- **Style Selection** - Choose from multiple Indian architectural styles
- **Real-time Generation** - Live progress tracking during model creation
- **Example Gallery** - Pre-built examples for quick generation
- **File Downloads** - Download .blend files, scripts, and metadata
- **Responsive Design** - Works on all devices and screen sizes

### 3D Logo Animation
- **Rotation Animation** - Continuous Y-axis rotation
- **Mouse Parallax** - Logo follows mouse movement
- **Glassmorphism** - Modern translucent design
- **Responsive** - Adapts to all screen sizes

### Authentication Pages
- **Non-scrollable Design** - Fixed viewport pages
- **Real-time Validation** - Instant form feedback
- **Loading States** - Professional loading indicators
- **Error Handling** - User-friendly error messages

### Dashboard
- **Welcome Interface** - Personalized user greeting
- **AI Integration** - Access to ML house generation features
- **Clean Layout** - Modern card-based design

## 🔐 Security Features

- **Password Hashing** - bcrypt with salt rounds
- **JWT Authentication** - Secure token-based auth
- **Input Validation** - Server-side validation
- **CORS Protection** - Configured cross-origin policies
- **Environment Variables** - Secure configuration management

## 📱 Responsive Design

- **Mobile First** - Optimized for mobile devices
- **Tablet Support** - Perfect tablet experience
- **Desktop Enhanced** - Full desktop features
- **Cross-browser** - Works on all modern browsers

## 🚀 Deployment

### Backend Deployment
1. Set environment variables on your hosting platform
2. Ensure MongoDB connection string is configured
3. Deploy to services like Heroku, Railway, or Vercel

### Frontend Deployment
1. Build the React app: `npm run build`
2. Deploy to services like Netlify, Vercel, or GitHub Pages
3. Update API base URL for production

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Manish Ram** - [@Manish9211Ram](https://github.com/Manish9211Ram)

## 🙏 Acknowledgments

- React.js community for the amazing framework
- Express.js for the robust backend framework
- MongoDB for the flexible database solution
- All contributors and supporters of this project

---

**Made with ❤️ for the architecture visualization community**