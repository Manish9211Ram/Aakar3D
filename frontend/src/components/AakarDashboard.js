import React, { useState } from 'react';
import axios from 'axios';
import ThreeJSViewer from './ThreeJSViewer';
import './Dashboard.css';

const AakarDashboard = ({ user, onLogout }) => {
  const [activeSection, setActiveSection] = useState('text');
  const [textInput, setTextInput] = useState('');
  const [imageFile, setImageFile] = useState(null);
  const [videoFile, setVideoFile] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedModel, setGeneratedModel] = useState(null);
  const [error, setError] = useState('');
  const [progress, setProgress] = useState(0);

  const handleTextSubmit = async (e) => {
    e.preventDefault();
    if (!textInput.trim()) return;
    
    setIsGenerating(true);
    setError('');
    setProgress(0);
    
    // Simulate progress for demo
    const progressInterval = setInterval(() => {
      setProgress(prev => prev < 90 ? prev + 10 : prev);
    }, 200);
    
    try {
      console.log('🏠 Generating house from text:', textInput);
      const response = await axios.post('http://localhost:5000/api/ml/generate-house', {
        description: textInput
      });
      
      if (response.data.success) {
        setGeneratedModel({
          text: textInput,
          attributes: response.data.data.attributes || {},
          modelData: response.data.data.model_data || null,
          timestamp: new Date().toISOString()
        });
        setProgress(100);
      } else {
        setError('Failed to generate 3D model');
      }
    } catch (err) {
      const errorMessage = err.response?.data?.error || err.message || 'Network error. Please try again.';
      setError(`Error: ${errorMessage}`);
      console.error('Generation error:', err.response?.data || err.message);
    } finally {
      clearInterval(progressInterval);
      setIsGenerating(false);
      setTimeout(() => setProgress(0), 1000);
    }
  };

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImageFile(file);
      console.log('Image uploaded:', file.name);
    }
  };

  const handleVideoUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setVideoFile(file);
      console.log('Video uploaded:', file.name);
    }
  };

  const handleImageSubmit = async () => {
    if (!imageFile) return;
    
    setIsGenerating(true);
    setError('');
    
    try {
      console.log('🖼️ Converting image to 3D:', imageFile.name);
      // Add actual image processing API call here
      
      setGeneratedModel({
        text: `Generated from image: ${imageFile.name}`,
        attributes: { type: 'image_generated' },
        timestamp: new Date().toISOString()
      });
    } catch (err) {
      setError('Failed to process image');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleVideoSubmit = async () => {
    if (!videoFile) return;
    
    setIsGenerating(true);
    setError('');
    
    try {
      console.log('🎥 Converting video to 3D:', videoFile.name);
      // Add actual video processing API call here
      
      setGeneratedModel({
        text: `Generated from video: ${videoFile.name}`,
        attributes: { type: 'video_generated' },
        timestamp: new Date().toISOString()
      });
    } catch (err) {
      setError('Failed to process video');
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="dashboard">
      {/* Header */}
      <header className="dashboard-header">
        <div className="header-content">
          <div className="logo-section">
            <h1 className="dashboard-title">Aakar 3D</h1>
            <p className="dashboard-subtitle">AI-Powered 3D Generation Platform</p>
          </div>
          <div className="user-section">
            <span className="welcome-text">Welcome, {user?.fullName || user?.username}</span>
            <button onClick={onLogout} className="logout-btn">Logout</button>
          </div>
        </div>
      </header>

      <main className="dashboard-main">
        <div className="dashboard-container">
          
          {/* Hero Section */}
          <section className="hero-banner">
            <div className="hero-content">
              <h2 className="hero-title">Transform Ideas into Reality</h2>
              <p className="hero-description">
                Generate stunning 3D house models from text, images, or videos using cutting-edge AI technology
              </p>
            </div>
            <div className="hero-stats">
              <div className="stat-item">
                <span className="stat-number">50K+</span>
                <span className="stat-label">Models Generated</span>
              </div>
              <div className="stat-item">
                <span className="stat-number">99.9%</span>
                <span className="stat-label">Accuracy</span>
              </div>
              <div className="stat-item">
                <span className="stat-number">&lt; 5s</span>
                <span className="stat-label">Generation Time</span>
              </div>
            </div>
          </section>

          {/* Generation Modes */}
          <section className="generation-modes">
            <h3 className="section-title">Choose Your Generation Mode</h3>
            
            <div className="mode-selector">
              <button 
                className={`mode-btn ${activeSection === 'text' ? 'active' : ''}`}
                onClick={() => setActiveSection('text')}
              >
                <div className="mode-icon">📝</div>
                <span>Text to 3D</span>
              </button>
              <button 
                className={`mode-btn ${activeSection === 'image' ? 'active' : ''}`}
                onClick={() => setActiveSection('image')}
              >
                <div className="mode-icon">🖼️</div>
                <span>Image to 3D</span>
              </button>
              <button 
                className={`mode-btn ${activeSection === 'video' ? 'active' : ''}`}
                onClick={() => setActiveSection('video')}
              >
                <div className="mode-icon">🎥</div>
                <span>Video to 3D</span>
              </button>
            </div>
          </section>

          {/* Generation Interface */}
          <section className="generation-interface">
            <div className="interface-grid">
              
              {/* Input Section */}
              <div className="input-section">
                {activeSection === 'text' && (
                  <div className="text-input-card">
                    <h4 className="card-title">Describe Your Dream House</h4>
                    <form onSubmit={handleTextSubmit}>
                      <textarea
                        value={textInput}
                        onChange={(e) => setTextInput(e.target.value)}
                        placeholder="e.g., A modern 2-story villa with large windows, minimalist design, white walls, and a swimming pool"
                        className="text-input"
                        rows="4"
                        disabled={isGenerating}
                      />
                      
                      {/* Quick Examples */}
                      <div className="example-buttons">
                        <button 
                          type="button" 
                          className="example-btn"
                          onClick={() => setTextInput("A traditional Kerala house with 2 floors, wooden balcony, and red tile roof")}
                        >
                          Kerala Style
                        </button>
                        <button 
                          type="button" 
                          className="example-btn"
                          onClick={() => setTextInput("A modern glass villa with 3 floors, swimming pool, and garden")}
                        >
                          Modern Villa
                        </button>
                        <button 
                          type="button" 
                          className="example-btn"
                          onClick={() => setTextInput("A royal Rajasthani haveli with courtyard, domes, and sandstone walls")}
                        >
                          Rajasthani Haveli
                        </button>
                      </div>
                      
                      <button 
                        type="submit" 
                        className="generate-btn"
                        disabled={isGenerating || !textInput.trim()}
                      >
                        {isGenerating ? (
                          <>
                            <span className="spinner"></span>
                            Generating...
                          </>
                        ) : (
                          <>
                            <span className="btn-icon">🏗️</span>
                            Generate 3D Model
                          </>
                        )}
                      </button>
                    </form>
                  </div>
                )}

                {activeSection === 'image' && (
                  <div className="image-input-card">
                    <h4 className="card-title">Upload House Image</h4>
                    <div className="upload-area">
                      <input
                        type="file"
                        accept="image/*"
                        onChange={handleImageUpload}
                        className="file-input"
                        id="image-upload"
                        disabled={isGenerating}
                      />
                      <label htmlFor="image-upload" className="upload-label">
                        {imageFile ? (
                          <div className="file-preview">
                            <img 
                              src={URL.createObjectURL(imageFile)} 
                              alt="Preview" 
                              className="preview-image"
                            />
                            <span className="file-name">{imageFile.name}</span>
                          </div>
                        ) : (
                          <div className="upload-placeholder">
                            <span className="upload-icon">📸</span>
                            <span>Click to upload or drag & drop</span>
                            <small>PNG, JPG up to 10MB</small>
                          </div>
                        )}
                      </label>
                    </div>
                    {imageFile && (
                      <button 
                        onClick={handleImageSubmit}
                        className="generate-btn"
                        disabled={isGenerating}
                      >
                        {isGenerating ? (
                          <>
                            <span className="spinner"></span>
                            Processing...
                          </>
                        ) : (
                          <>
                            <span className="btn-icon">🎨</span>
                            Convert to 3D
                          </>
                        )}
                      </button>
                    )}
                  </div>
                )}

                {activeSection === 'video' && (
                  <div className="video-input-card">
                    <h4 className="card-title">Upload House Video</h4>
                    <div className="upload-area">
                      <input
                        type="file"
                        accept="video/*"
                        onChange={handleVideoUpload}
                        className="file-input"
                        id="video-upload"
                        disabled={isGenerating}
                      />
                      <label htmlFor="video-upload" className="upload-label">
                        {videoFile ? (
                          <div className="file-preview">
                            <video 
                              src={URL.createObjectURL(videoFile)} 
                              className="preview-video"
                              controls
                            />
                            <span className="file-name">{videoFile.name}</span>
                          </div>
                        ) : (
                          <div className="upload-placeholder">
                            <span className="upload-icon">🎬</span>
                            <span>Click to upload or drag & drop</span>
                            <small>MP4, MOV up to 100MB</small>
                          </div>
                        )}
                      </label>
                    </div>
                    {videoFile && (
                      <button 
                        onClick={handleVideoSubmit}
                        className="generate-btn"
                        disabled={isGenerating}
                      >
                        {isGenerating ? (
                          <>
                            <span className="spinner"></span>
                            Processing...
                          </>
                        ) : (
                          <>
                            <span className="btn-icon">🎞️</span>
                            Convert to 3D
                          </>
                        )}
                      </button>
                    )}
                  </div>
                )}

                {/* Progress Bar */}
                {isGenerating && progress > 0 && (
                  <div className="progress-section">
                    <div className="progress-bar">
                      <div 
                        className="progress-fill" 
                        style={{ width: `${progress}%` }}
                      ></div>
                    </div>
                    <span className="progress-text">{progress}% Complete</span>
                  </div>
                )}

                {/* Error Display */}
                {error && (
                  <div className="error-message">
                    <span className="error-icon">⚠️</span>
                    {error}
                  </div>
                )}
              </div>

              {/* 3D Viewer Section */}
              <div className="viewer-section">
                <div className="viewer-card">
                  <h4 className="card-title">3D Model Preview</h4>
                  {generatedModel ? (
                    <div className="model-display">
                      <ThreeJSViewer modelData={generatedModel} />
                      <div className="model-info">
                        <p className="model-description">{generatedModel.text}</p>
                        <div className="model-stats">
                          <span className="stat">⏱️ Generated: {new Date(generatedModel.timestamp).toLocaleTimeString()}</span>
                        </div>
                        <div className="model-actions">
                          <button className="action-btn download-btn">
                            📥 Download Model
                          </button>
                          <button className="action-btn view-btn">
                            👁️ View Details
                          </button>
                          <button className="action-btn share-btn">
                            🔗 Share Model
                          </button>
                        </div>
                      </div>
                    </div>
                  ) : (
                    <div className="viewer-placeholder">
                      <div className="placeholder-content">
                        <span className="placeholder-icon">🏠</span>
                        <h5>Your 3D Model Will Appear Here</h5>
                        <p>Select a generation mode and input your data to create amazing 3D house models</p>
                      </div>
                    </div>
                  )}
                </div>
              </div>

            </div>
          </section>

          {/* Features Section */}
          <section className="features-section">
            <h3 className="section-title">Why Choose Aakar 3D?</h3>
            <div className="features-grid">
              <div className="feature-card">
                <div className="feature-icon">⚡</div>
                <h4>Lightning Fast</h4>
                <p>Generate 3D models in under 5 seconds with our optimized AI engine</p>
              </div>
              <div className="feature-card">
                <div className="feature-icon">🎯</div>
                <h4>High Accuracy</h4>
                <p>99.9% accurate architectural interpretations with realistic proportions</p>
              </div>
              <div className="feature-card">
                <div className="feature-icon">🎨</div>
                <h4>Multiple Inputs</h4>
                <p>Support for text descriptions, images, and video inputs</p>
              </div>
              <div className="feature-card">
                <div className="feature-icon">💎</div>
                <h4>Premium Quality</h4>
                <p>Professional-grade 3D models ready for rendering and printing</p>
              </div>
            </div>
          </section>

        </div>
      </main>
    </div>
  );
};

export default AakarDashboard;