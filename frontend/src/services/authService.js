// Authentication Service for Aakar3D Frontend

const API_BASE_URL = 'http://localhost:5000/api';

class AuthService {
  constructor() {
    this.token = localStorage.getItem('aakar3d_token');
    this.user = JSON.parse(localStorage.getItem('aakar3d_user') || 'null');
  }

  // Signup user
  async signup(userData) {
    try {
      const response = await fetch(`${API_BASE_URL}/signup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData)
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Signup failed');
      }

      // Store token and user data
      this.token = data.token;
      this.user = data.user;
      localStorage.setItem('aakar3d_token', data.token);
      localStorage.setItem('aakar3d_user', JSON.stringify(data.user));

      return {
        success: true,
        message: data.message,
        user: data.user
      };

    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  // Login user
  async login(credentials) {
    try {
      const response = await fetch(`${API_BASE_URL}/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials)
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Login failed');
      }

      // Store token and user data
      this.token = data.token;
      this.user = data.user;
      localStorage.setItem('aakar3d_token', data.token);
      localStorage.setItem('aakar3d_user', JSON.stringify(data.user));

      return {
        success: true,
        message: data.message,
        user: data.user
      };

    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  // Logout user
  logout() {
    this.token = null;
    this.user = null;
    localStorage.removeItem('aakar3d_token');
    localStorage.removeItem('aakar3d_user');
    
    return {
      success: true,
      message: 'Logged out successfully'
    };
  }

  // Get user profile
  async getProfile() {
    try {
      if (!this.token) {
        throw new Error('No token available');
      }

      const response = await fetch(`${API_BASE_URL}/profile`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${this.token}`,
          'Content-Type': 'application/json',
        }
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to get profile');
      }

      return {
        success: true,
        user: data.user
      };

    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  // Check if user is authenticated
  isAuthenticated() {
    return !!this.token && !!this.user;
  }

  // Get current user
  getCurrentUser() {
    return this.user;
  }

  // Get auth token
  getToken() {
    return this.token;
  }

  // Validate email format
  isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  // Validate username format
  isValidUsername(username) {
    const usernameRegex = /^[a-zA-Z0-9_]{3,20}$/;
    return usernameRegex.test(username);
  }

  // Validate password strength
  isValidPassword(password) {
    return password.length >= 6;
  }
}

// Create singleton instance
const authService = new AuthService();

export default authService;
