# Aakar3D - Architecture Visualization Platform

🏗️ **A modern 3D architecture visualization platform built with React.js and Express.js**

## 🌟 Features

### Frontend (React.js)
- ✨ **3D Logo Animation** - Rotating 3D logo with CSS animations and mouse parallax effects
- 🎨 **Modern UI/UX** - Glassmorphism design with gradient backgrounds
- 🔐 **Authentication System** - Complete login/signup with JWT tokens
- 📱 **Responsive Design** - Works seamlessly across all devices
- 🎯 **Dashboard** - User dashboard with text-to-3D model functionality
- 🔄 **Real-time Validation** - Form validation with instant feedback

### Backend (Express.js + MongoDB)
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
- **Local Storage** - Client-side token storage

### Backend
- **Express.js** - Fast, minimalist web framework
- **MongoDB** - NoSQL database for user data
- **Mongoose** - MongoDB object modeling
- **JWT** - JSON Web Tokens for authentication
- **bcryptjs** - Password hashing library
- **CORS** - Cross-origin resource sharing
- **Nodemon** - Development auto-restart

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
- **Git**

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Install dependencies** (already included in repo):
   ```bash
   npm install
   ```

3. **Create environment file:**
   ```bash
   # Create .env file in backend directory
   MONGODB_URI=mongodb://localhost:27017/aakar3d
   JWT_SECRET=your_super_secret_jwt_key_here_make_it_long_and_secure
   PORT=5000
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
   npm install
   ```

3. **Start the frontend development server:**
   ```bash
   npm start
   ```

## 🌐 API Endpoints

### Authentication
- `POST /api/signup` - User registration
- `POST /api/login` - User login
- `GET /api/profile` - Get user profile (protected)

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

## 🎨 UI Features

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
- **Text to 3D Model** - Convert text descriptions to 3D models
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