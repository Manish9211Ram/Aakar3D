import React from 'react';
import './Navbar.css';

const Navbar = ({ user, onLogin, onSignup, onLogout }) => {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        {/* Logo/Brand */}
        <div className="navbar-brand">
          <h2>Aakar3D</h2>
        </div>

        {/* Navigation Links */}
        <div className="navbar-menu">
          <ul className="navbar-nav">
            <li className="nav-item">
              <a href="#home" className="nav-link">Home</a>
            </li>
            <li className="nav-item">
              <a href="#features" className="nav-link">Features</a>
            </li>
            <li className="nav-item">
              <a href="#resources" className="nav-link">Resources</a>
            </li>
            <li className="nav-item">
              <a href="#docs" className="nav-link">Docs</a>
            </li>
          </ul>
        </div>

        {/* Auth Buttons */}
        <div className="navbar-auth">
          {user ? (
            <div className="user-menu">
              <span className="user-greeting">Hi, {user.fullName || user.username}!</span>
              <button className="btn btn-logout" onClick={onLogout}>LOGOUT</button>
            </div>
          ) : (
            <>
              <button className="btn btn-login" onClick={onLogin}>LOGIN</button>
              <button className="btn btn-signin" onClick={onSignup}>SIGN UP</button>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;