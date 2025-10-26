import React, { useState } from 'react';
import authService from '../services/authService';
import './AuthPages.css';

const Login = ({ onSwitchToSignup, onLoginSuccess }) => {
  const [formData, setFormData] = useState({
    emailOrUsername: '',
    password: ''
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

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    setSuccess('');

    try {
      // Validate inputs
      if (!formData.emailOrUsername || !formData.password) {
        setError('Please fill in all fields');
        setIsLoading(false);
        return;
      }

      // Attempt login
      const result = await authService.login({
        emailOrUsername: formData.emailOrUsername,
        password: formData.password
      });

      if (result.success) {
        setSuccess('Login successful! Redirecting...');
        
        // Notify parent component of successful login
        if (onLoginSuccess) {
          onLoginSuccess(result.user);
        }
        
        // Clear form
        setFormData({
          emailOrUsername: '',
          password: ''
        });
        
        // Optional: redirect after a delay
        setTimeout(() => {
          // window.location.href = '/dashboard'; // Uncomment for redirect
        }, 2000);
        
      } else {
        setError(result.error || 'Login failed');
      }
    } catch (err) {
      setError('Network error. Please try again.');
      console.error('Login error:', err);
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
          <h1>Welcome Back</h1>
          <p>Login to your Aakar3D account and continue building</p>
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
            <label htmlFor="emailOrUsername">Email or Username</label>
            <input
              type="text"
              id="emailOrUsername"
              name="emailOrUsername"
              value={formData.emailOrUsername}
              onChange={handleInputChange}
              required
              placeholder="Enter your email or username"
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
              placeholder="Enter your password"
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
                Logging in...
              </>
            ) : 'Login'}
          </button>

          <div className="auth-switch">
            <p>Don't have an account? 
              <span 
                onClick={!isLoading ? onSwitchToSignup : undefined} 
                className={`switch-link ${isLoading ? 'disabled' : ''}`}
              >
                Sign up here
              </span>
            </p>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Login;