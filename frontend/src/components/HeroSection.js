import React, { useEffect, useRef } from 'react';
import './HeroSection.css';

const HeroSection = () => {
  const logoRef = useRef(null);

  useEffect(() => {
    // Initialize 3D logo animation
    initLogo3D();
    
    // Enhanced parallax mouse effect for logo
    const handleMouseMove = (e) => {
      const { clientX, clientY } = e;
      const centerX = window.innerWidth / 2;
      const centerY = window.innerHeight / 2;
      
      const moveX = (clientX - centerX) / 30; // More subtle movement
      const moveY = (clientY - centerY) / 30;
      
      if (logoRef.current) {
        logoRef.current.style.transform = `
          translateX(${moveX}px) 
          translateY(${moveY}px) 
          rotateY(${moveX / 3}deg) 
          rotateX(${-moveY / 3}deg)
          rotateZ(${moveX / 8}deg)
        `;
      }
    };

    window.addEventListener('mousemove', handleMouseMove);
    
    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
    };
  }, []);

  const initLogo3D = () => {
    // Animate logo entrance
    if (logoRef.current) {
      setTimeout(() => {
        logoRef.current.classList.add('animate-in');
      }, 1000);
    }
  };

  return (
    <section className="hero-section">
      {/* Background Effects */}
      <div className="bg-orbs">
        <div className="orb orb-1"></div>
        <div className="orb orb-2"></div>
        <div className="orb orb-3"></div>
      </div>
      
      <div className="noise-overlay"></div>
      <div className="radial-gradient"></div>
      
      {/* Main Content Grid */}
      <div className="hero-grid">
        {/* Left Content Section */}
        <div className="hero-content">
          <h1 className="hero-title animate-fadeup-1">
            Aakar<span className="highlight-orange">3D</span>
          </h1>
          
          <h2 className="hero-subtitle animate-fadeup-2">
            Building the future of <span className="highlight-orange">Architecture</span>
          </h2>
          
          <p className="hero-description animate-fadeup-3">
            Unlock smarter design with Aakar3D — where machine learning meets 
            architectural intelligence. Analyze building structures, learn design 
            patterns, and predict the perfect architecture.
          </p>
          
          <div className="hero-buttons animate-fadeup-4">
            <button className="btn btn-documentation">
              Documentation
              <span className="btn-arrow">→</span>
            </button>
            <button className="btn btn-getstarted">
              Get Started
              <span className="btn-arrow">→</span>
            </button>
          </div>
        </div>
        
        {/* Right 3D Logo Section */}
        <div className="logo-3d-container">
          <div className="logo-3d" ref={logoRef}>
            <div className="logo-wrapper">
              <img 
                src="/aakar3d-logo.png" 
                alt="Aakar3D Logo" 
                className="logo-image"
              />
              <div className="logo-glow"></div>
            </div>
          </div>
          
          {/* Floating Geometric Shapes */}
          <div className="floating-shapes">
            <div className="shape cube-1"></div>
            <div className="shape sphere-1"></div>
            <div className="shape cube-2"></div>
            <div className="shape pyramid-1"></div>
          </div>
          
          {/* Particle System */}
          <div className="particles">
            {[...Array(15)].map((_, i) => (
              <div key={i} className={`particle particle-${i}`}></div>
            ))}
          </div>
          
          {/* Perspective Grid */}
          <div className="perspective-grid">
            {[...Array(20)].map((_, i) => (
              <div key={i} className="grid-line"></div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;