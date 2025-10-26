import React, { useState } from 'react';
import authService from '../services/authService';
import './AuthPages.css';

const Signup = ({ onSwitchToLogin, onSignupSuccess }) => {
  const [formData, setFormData] = useState({
    fullName: '',
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    
    // Clear messages when user starts typing
    if (error) setError('');
    if (success) setSuccess('');
  };

  const validateForm = () => {
    // Full name validation
    if (!formData.fullName || formData.fullName.trim().length < 2) {
      setError('Full name must be at least 2 characters long');
      return false;
    }

    // Username validation
    if (!authService.isValidUsername(formData.username)) {
      setError('Username must be 3-20 characters and contain only letters, numbers, and underscores');
      return false;
    }

    // Email validation
    if (!authService.isValidEmail(formData.email)) {
      setError('Please enter a valid email address');
      return false;
    }

    // Password validation
    if (!authService.isValidPassword(formData.password)) {
      setError('Password must be at least 6 characters long');
      return false;
    }

    // Confirm password validation
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return false;
    }

    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    setSuccess('');

    try {
      // Validate form
      if (!validateForm()) {
        setIsLoading(false);
        return;
      }

      // Attempt signup
      const result = await authService.signup({
        fullName: formData.fullName.trim(),
        username: formData.username.trim(),
        email: formData.email.trim().toLowerCase(),
        password: formData.password
      });

      if (result.success) {
        setSuccess('Account created successfully! You can now login.');
        
        // Notify parent component of successful signup
        if (onSignupSuccess) {
          onSignupSuccess(result.user);
        }
        
        // Clear form
        setFormData({
          fullName: '',
          username: '',
          email: '',
          password: '',
          confirmPassword: ''
        });
        
        // Optional: auto-switch to login after a delay
        setTimeout(() => {
          if (onSwitchToLogin) {
            onSwitchToLogin();
          }
        }, 3000);
        
      } else {
        setError(result.error || 'Signup failed');
      }
    } catch (err) {
      setError('Network error. Please try again.');
      console.error('Signup error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-container">
        {/* Logo Section */}
        <div className="auth-logo-section">
          <div className="auth-logo">
            <img src="/aakar3d-logo.png" alt="Aakar3D Logo" />
          </div>
          <h1 className="auth-brand-title">Aakar 3D</h1>
          <p className="auth-brand-subtitle">Build • Create • Innovate</p>
        </div>

        <div className="auth-header">
          <h1>Create Account</h1>
          <p>Join Aakar3D today and start building amazing 3D houses</p>
        </div>

        {error && (
          <div className="error-message">
            <span className="error-icon">⚠️</span>
            {error}
          </div>
        )}

        {success && (
          <div className="success-message">
            <span className="success-icon">✅</span>
            {success}
          </div>
        )}

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label htmlFor="fullName">Full Name</label>
            <input
              type="text"
              id="fullName"
              name="fullName"
              value={formData.fullName}
              onChange={handleInputChange}
              required
              placeholder="Enter your full name"
              disabled={isLoading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleInputChange}
              required
              placeholder="Choose a username"
              disabled={isLoading}
            />
            <small className="form-hint">3-20 characters, letters, numbers, and underscores only</small>
          </div>

          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleInputChange}
              required
              placeholder="Enter your email"
              disabled={isLoading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleInputChange}
              required
              placeholder="Create a password"
              disabled={isLoading}
            />
            <small className="form-hint">Minimum 6 characters</small>
          </div>

          <div className="form-group">
            <label htmlFor="confirmPassword">Confirm Password</label>
            <input
              type="password"
              id="confirmPassword"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleInputChange}
              required
              placeholder="Confirm your password"
              disabled={isLoading}
            />
          </div>

          <button 
            type="submit" 
            className="auth-button"
            disabled={isLoading}
          >
            {isLoading ? (
              <>
                <span className="loading-spinner"></span>
                Creating Account...
              </>
            ) : 'Create Account'}
          </button>

          <div className="auth-switch">
            <p>Already have an account? 
              <span 
                onClick={!isLoading ? onSwitchToLogin : undefined} 
                className={`switch-link ${isLoading ? 'disabled' : ''}`}
              >
                Login here
              </span>
            </p>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Signup;