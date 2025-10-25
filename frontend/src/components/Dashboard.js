import React, { useState } from 'react';
import './Dashboard.css';

const Dashboard = ({ user, onLogout }) => {
  const [textInput, setTextInput] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedModel, setGeneratedModel] = useState(null);
  const [error, setError] = useState('');

  const handleTextToModel = async () => {
    if (!textInput.trim()) {
      setError('Please enter some text to generate a 3D model');
      return;
    }

    setIsGenerating(true);
    setError('');
    
    try {
      // Simulate API call for text to 3D model generation
      // In real implementation, this would call your AI service
      await new Promise(resolve => setTimeout(resolve, 3000));
      
      setGeneratedModel({
        text: textInput,
        modelUrl: '/path/to/generated/model.obj', // This would be the actual model URL
        timestamp: new Date().toISOString()
      });
      
      setTextInput('');
    } catch (err) {
      setError('Failed to generate 3D model. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleInputChange = (e) => {
    setTextInput(e.target.value);
    if (error) setError('');
  };

  return (
    <div className="dashboard">
      {/* Header */}
      <header className="dashboard-header">
        <div className="header-content">
          <div className="logo-section">
            <h1 className="dashboard-title">Aakar3D Dashboard</h1>
            <p className="dashboard-subtitle">Transform your ideas into 3D reality</p>
          </div>
          <div className="user-section">
            <span className="welcome-text">Welcome, {user?.fullName || user?.username}!</span>
            <button onClick={onLogout} className="logout-btn">
              Logout
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="dashboard-main">
        <div className="dashboard-container">
          
          {/* Welcome Section */}
          <section className="welcome-section">
            <div className="welcome-card">
              <h2>🎉 Welcome to Aakar3D!</h2>
              <p>
                Ready to bring your imagination to life? Use our advanced AI to convert any text 
                description into stunning 3D models. Simply describe what you want to create, 
                and watch the magic happen!
              </p>
            </div>
          </section>

          {/* Text to 3D Section */}
          <section className="text-to-3d-section">
            <div className="generator-card">
              <h3>✨ Text to 3D Model Generator</h3>
              
              {error && (
                <div className="error-message">
                  <span className="error-icon">⚠️</span>
                  {error}
                </div>
              )}

              <div className="input-section">
                <label htmlFor="textInput">Describe your 3D model:</label>
                <textarea
                  id="textInput"
                  value={textInput}
                  onChange={handleInputChange}
                  placeholder="e.g., A futuristic spaceship with glowing blue engines, sleek metallic surface, and angular wings..."
                  rows={4}
                  disabled={isGenerating}
                  className="text-input"
                />
                
                <button 
                  onClick={handleTextToModel}
                  disabled={isGenerating || !textInput.trim()}
                  className="generate-btn"
                >
                  {isGenerating ? (
                    <>
                      <span className="loading-spinner"></span>
                      Generating 3D Model...
                    </>
                  ) : (
                    <>
                      🚀 Generate 3D Model
                    </>
                  )}
                </button>
              </div>
            </div>
          </section>

          {/* Generated Model Display */}
          {generatedModel && (
            <section className="model-display-section">
              <div className="model-card">
                <h3>🎯 Generated Model</h3>
                <div className="model-info">
                  <p><strong>Description:</strong> {generatedModel.text}</p>
                  <p><strong>Generated:</strong> {new Date(generatedModel.timestamp).toLocaleString()}</p>
                </div>
                
                {/* 3D Model Viewer Placeholder */}
                <div className="model-viewer">
                  <div className="model-placeholder">
                    <div className="rotating-cube">
                      <div className="cube-face front">🎨</div>
                      <div className="cube-face back">3D</div>
                      <div className="cube-face right">🔥</div>
                      <div className="cube-face left">AI</div>
                      <div className="cube-face top">⭐</div>
                      <div className="cube-face bottom">🚀</div>
                    </div>
                    <p>3D Model Preview</p>
                    <small>In production, this would show the actual generated 3D model</small>
                  </div>
                </div>

                <div className="model-actions">
                  <button className="action-btn download-btn">
                    📥 Download Model
                  </button>
                  <button className="action-btn view-btn">
                    👁️ View in 3D
                  </button>
                  <button className="action-btn share-btn">
                    🔗 Share Model
                  </button>
                </div>
              </div>
            </section>
          )}

          {/* Quick Stats */}
          <section className="stats-section">
            <div className="stats-grid">
              <div className="stat-card">
                <h4>Models Created</h4>
                <span className="stat-number">12</span>
              </div>
              <div className="stat-card">
                <h4>Total Generations</h4>
                <span className="stat-number">47</span>
              </div>
              <div className="stat-card">
                <h4>Success Rate</h4>
                <span className="stat-number">98%</span>
              </div>
              <div className="stat-card">
                <h4>Time Saved</h4>
                <span className="stat-number">24h</span>
              </div>
            </div>
          </section>

        </div>
      </main>
    </div>
  );
};

export default Dashboard;