import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import HeroSection from './components/HeroSection';
import AakarDashboard from './components/AakarDashboard';
import Login from './components/Login';
import Signup from './components/Signup';
import authService from './services/authService';
import './App.css';

function App() {
  const [currentView, setCurrentView] = useState('home'); // 'home', 'login', 'signup', 'dashboard'
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check if user is already authenticated on app load
    const checkAuth = async () => {
      try {
        if (authService.isAuthenticated()) {
          const result = await authService.getProfile();
          if (result.success) {
            setUser(result.user);
            // Keep currentView as 'home' instead of auto-redirecting to dashboard
            // User can manually navigate to dashboard via navbar
          } else {
            // Token might be expired, clear it
            authService.logout();
          }
        }
      } catch (error) {
        console.error('Auth check error:', error);
      } finally {
        setIsLoading(false);
      }
    };

    checkAuth();
  }, []);

  const handleLogin = () => {
    setCurrentView('login');
  };

  const handleSignup = () => {
    setCurrentView('signup');
  };

  const handleLoginSuccess = (userData) => {
    setUser(userData);
    setCurrentView('dashboard'); // Redirect to dashboard after login
  };

  const handleSignupSuccess = (userData) => {
    setUser(userData);
    setCurrentView('dashboard'); // Redirect to dashboard after signup
  };

  const handleLogout = () => {
    authService.logout();
    setUser(null);
    setCurrentView('home');
  };

  if (isLoading) {
    return (
      <div className="App">
        <div style={{ 
          display: 'flex', 
          justifyContent: 'center', 
          alignItems: 'center', 
          height: '100vh',
          fontSize: '1.2rem',
          color: '#667eea',
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
        }}>
          <div style={{ textAlign: 'center', color: 'white' }}>
            <div style={{ fontSize: '2rem', marginBottom: '1rem' }}>🚀</div>
            Loading Aakar3D...
          </div>
        </div>
      </div>
    );
  }

  // Render auth pages
  if (currentView === 'login') {
    return (
      <Login 
        onSwitchToSignup={() => setCurrentView('signup')}
        onLoginSuccess={handleLoginSuccess}
      />
    );
  }

  if (currentView === 'signup') {
    return (
      <Signup 
        onSwitchToLogin={() => setCurrentView('login')}
        onSignupSuccess={handleSignupSuccess}
      />
    );
  }

  // Render dashboard if user is logged in
  if (currentView === 'dashboard' && user) {
    return (
      <AakarDashboard 
        user={user}
        onLogout={handleLogout}
      />
    );
  }

  // Render main app (home page)
  return (
    <div className="App">
      {/* Navigation */}
      <Navbar 
        user={user}
        onLogin={handleLogin}
        onSignup={handleSignup}
        onLogout={handleLogout}
      />
      
      {/* Hero Section */}
      <HeroSection user={user} />
    </div>
  );
}

export default App;
