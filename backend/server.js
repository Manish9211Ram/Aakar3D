const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const axios = require('axios');
require('dotenv').config();

const app = express();

// Middleware
app.use(cors({
  origin: ['http://localhost:3000', 'http://127.0.0.1:3000'],
  credentials: true
}));
app.use(express.json());

// MongoDB Connection
const MONGODB_URI = 'mongodb://localhost:27017/aakar3d';
const JWT_SECRET = 'aakar3d_secret_key_2025';

mongoose.connect(MONGODB_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
})
.then(() => console.log('✅ Connected to MongoDB'))
.catch(err => console.error('❌ MongoDB connection error:', err));

// User Schema
const userSchema = new mongoose.Schema({
  fullName: {
    type: String,
    required: true,
    trim: true
  },
  username: {
    type: String,
    required: true,
    unique: true,
    trim: true,
    lowercase: true
  },
  email: {
    type: String,
    required: true,
    unique: true,
    trim: true,
    lowercase: true
  },
  password: {
    type: String,
    required: true,
    minlength: 6
  }
}, {
  timestamps: true
});

const User = mongoose.model('User', userSchema);

// ===== ROUTES =====

// Health Check
app.get('/api/health', (req, res) => {
  res.json({ message: 'Aakar3D Backend is running!' });
});

// SIGNUP Route
app.post('/api/signup', async (req, res) => {
  try {
    const { fullName, username, email, password } = req.body;

    // Validation
    if (!fullName || !username || !email || !password) {
      return res.status(400).json({ 
        error: 'All fields are required' 
      });
    }

    if (password.length < 6) {
      return res.status(400).json({ 
        error: 'Password must be at least 6 characters long' 
      });
    }

    // Check if user already exists
    const existingUser = await User.findOne({
      $or: [{ email }, { username }]
    });

    if (existingUser) {
      if (existingUser.email === email) {
        return res.status(400).json({ 
          error: 'Email already registered' 
        });
      }
      if (existingUser.username === username) {
        return res.status(400).json({ 
          error: 'Username already taken' 
        });
      }
    }

    // Hash password
    const saltRounds = 12;
    const hashedPassword = await bcrypt.hash(password, saltRounds);

    // Create new user
    const newUser = new User({
      fullName,
      username,
      email,
      password: hashedPassword
    });

    await newUser.save();

    // Generate JWT token
    const token = jwt.sign(
      { 
        userId: newUser._id,
        username: newUser.username,
        email: newUser.email 
      },
      JWT_SECRET,
      { expiresIn: '7d' }
    );

    res.status(201).json({
      message: 'Account created successfully!',
      token,
      user: {
        id: newUser._id,
        fullName: newUser.fullName,
        username: newUser.username,
        email: newUser.email
      }
    });

  } catch (error) {
    console.error('Signup error:', error);
    res.status(500).json({ 
      error: 'Internal server error. Please try again.' 
    });
  }
});

// LOGIN Route
app.post('/api/login', async (req, res) => {
  try {
    const { emailOrUsername, password } = req.body;

    // Validation
    if (!emailOrUsername || !password) {
      return res.status(400).json({ 
        error: 'Email/Username and password are required' 
      });
    }

    // Find user by email or username
    const user = await User.findOne({
      $or: [
        { email: emailOrUsername.toLowerCase() },
        { username: emailOrUsername.toLowerCase() }
      ]
    });

    if (!user) {
      return res.status(400).json({ 
        error: 'Invalid credentials' 
      });
    }

    // Check password
    const isPasswordValid = await bcrypt.compare(password, user.password);

    if (!isPasswordValid) {
      return res.status(400).json({ 
        error: 'Invalid credentials' 
      });
    }

    // Generate JWT token
    const token = jwt.sign(
      { 
        userId: user._id,
        username: user.username,
        email: user.email 
      },
      JWT_SECRET,
      { expiresIn: '7d' }
    );

    res.json({
      message: 'Login successful!',
      token,
      user: {
        id: user._id,
        fullName: user.fullName,
        username: user.username,
        email: user.email
      }
    });

  } catch (error) {
    console.error('Login error:', error);
    res.status(500).json({ 
      error: 'Internal server error. Please try again.' 
    });
  }
});

// Get User Profile (Protected Route)
app.get('/api/profile', authenticateToken, async (req, res) => {
  try {
    const user = await User.findById(req.user.userId).select('-password');
    
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    res.json({
      user: {
        id: user._id,
        fullName: user.fullName,
        username: user.username,
        email: user.email,
        createdAt: user.createdAt
      }
    });
  } catch (error) {
    console.error('Profile error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// ===== MIDDLEWARE =====

// ML Service Configuration
const ML_SERVICE_URL = 'http://localhost:5001';

// ===== ML SERVICE ROUTES =====

// ML Health Check
app.get('/api/ml/health', async (req, res) => {
  try {
    const response = await axios.get(`${ML_SERVICE_URL}/health`, {
      timeout: 5000
    });
    
    res.json({
      success: true,
      message: 'ML service is healthy',
      mlService: response.data
    });
  } catch (error) {
    console.error('ML service health check failed:', error.message);
    res.status(503).json({
      success: false,
      message: 'ML service unavailable',
      error: error.message
    });
  }
});

// Generate House
app.post('/api/ml/generate-house', async (req, res) => {
  try {
    const { description, style, floors } = req.body;
    
    if (!description) {
      return res.status(400).json({
        success: false,
        message: 'House description is required'
      });
    }
    
    console.log('🏠 Generating house:', description);
    
    // Call ML service
    const response = await axios.post(`${ML_SERVICE_URL}/generate`, {
      description,
      style,
      floors
    }, {
      timeout: 60000 // 1 minute timeout
    });
    
    console.log('✅ ML Response:', response.data);
    
    if (response.data.success) {
      res.json({
        success: true,
        message: 'House generated successfully',
        data: response.data.data
      });
    } else {
      res.status(500).json({
        success: false,
        message: 'House generation failed',
        error: response.data.error
      });
    }
    
  } catch (error) {
    console.error('❌ House generation error:', error.message);
    res.status(500).json({
      success: false,
      message: 'Server error during house generation',
      error: error.message
    });
  }
});

// Generate House from Form
app.post('/api/ml/generate-house-form', async (req, res) => {
  try {
    const formData = req.body;
    
    console.log('🏗️ Generating house from form data:', formData);
    
    // Call ML service with form data
    const response = await axios.post(`${ML_SERVICE_URL}/generate_house_from_form`, formData, {
      timeout: 60000 // 1 minute timeout
    });
    
    console.log('✅ ML Form Response:', response.data);
    
    if (response.data.success) {
      res.json({
        success: true,
        message: 'House generated successfully from form',
        data: response.data.data
      });
    } else {
      res.status(500).json({
        success: false,
        message: 'House generation from form failed',
        error: response.data.error
      });
    }
    
  } catch (error) {
    console.error('❌ House form generation error:', error.message);
    res.status(500).json({
      success: false,
      message: 'Server error during house form generation',
      error: error.message
    });
  }
});

// Get Configuration Options for Form
app.get('/api/ml/config-options', async (req, res) => {
  try {
    const response = await axios.get(`${ML_SERVICE_URL}/config_options`);
    
    res.json({
      success: true,
      data: response.data
    });
    
  } catch (error) {
    console.error('❌ Config options error:', error.message);
    res.status(500).json({
      success: false,
      message: 'Failed to get configuration options',
      error: error.message
    });
  }
});

// Get Examples
app.get('/api/ml/examples', async (req, res) => {
  try {
    const response = await axios.get(`${ML_SERVICE_URL}/examples`);
    
    res.json({
      success: true,
      examples: response.data.examples
    });
  } catch (error) {
    console.error('Failed to fetch examples:', error.message);
    res.status(500).json({
      success: false,
      message: 'Failed to fetch examples',
      error: error.message
    });
  }
});

// Get Styles
app.get('/api/ml/styles', async (req, res) => {
  try {
    const response = await axios.get(`${ML_SERVICE_URL}/styles`);
    
    res.json({
      success: true,
      styles: response.data.styles,
      houseTypes: response.data.house_types,
      roomTypes: response.data.room_types,
      features: response.data.features
    });
  } catch (error) {
    console.error('Failed to fetch styles:', error.message);
    res.status(500).json({
      success: false,
      message: 'Failed to fetch architectural styles',
      error: error.message
    });
  }
});

// ===== MIDDLEWARE =====

// JWT Authentication Middleware
function authenticateToken(req, res, next) {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    return res.status(401).json({ error: 'Access token required' });
  }

  jwt.verify(token, JWT_SECRET, (err, user) => {
    if (err) {
      return res.status(403).json({ error: 'Invalid or expired token' });
    }
    req.user = user;
    next();
  });
}

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Something went wrong!' });
});

// 404 handler - catch all unmatched routes
app.use((req, res) => {
  res.status(404).json({ error: 'Route not found' });
});

// Start server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
  console.log(`📊 MongoDB: ${MONGODB_URI}`);
});

module.exports = app;
