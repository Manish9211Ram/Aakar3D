import React, { useState } from 'react';
import axios from 'axios';
import ThreeJSViewer from './ThreeJSViewer';
import AdvancedForm from './AdvancedForm';
import './Dashboard.css';

const Dashboard = ({ user, onLogout }) => {
  const [textInput, setTextInput] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedModel, setGeneratedModel] = useState(null);
  const [error, setError] = useState('');
  const [generationMode, setGenerationMode] = useState('text'); // 'text' or 'form'

  const handleInputChange = (e) => {
    setTextInput(e.target.value);
    setError('');
  };

  const handleGenerate = async (data, mode = 'text') => {
    setIsGenerating(true);
    setError('');
    
    try {
      let response;
      
      if (mode === 'form') {
        console.log('🏗️ Sending form data to generate house:', data);
        response = await axios.post('http://localhost:5000/api/ml/generate-house-form', data);
      } else {
        console.log('🏠 Sending text to generate house:', data);
        response = await axios.post('http://localhost:5000/api/ml/generate-house', {
          description: data
        });
      }
      
      console.log('✅ Received response:', response.data);
      
      if (response.data.success) {
        const mlData = response.data.data;
        console.log('📊 ML Data received:', mlData);
        
        setGeneratedModel({
          text: mode === 'form' ? `Custom ${data.style} ${data.house_type}` : data,
          attributes: mlData.attributes || {},
          files: mlData.files || [],
          processingTime: mlData.processing_time ? `${mlData.processing_time.toFixed(3)}s` : 'N/A',
          timestamp: new Date().toISOString(),
          modelData: mlData.model_data || null,
          formConfig: mlData.form_config || null
        });
        
        if (mode === 'text') {
          setTextInput('');
        }
        setError('');
      } else {
        setError(response.data.message || 'Failed to generate house model');
      }
      
    } catch (err) {
      console.error('❌ Generation error:', err);
      setError(err.response?.data?.message || 'Failed to generate 3D model. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleTextToModel = () => {
    if (!textInput.trim()) {
      setError('Please enter some text to generate a 3D model');
      return;
    }
    handleGenerate(textInput, 'text');
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
              <div className="generator-header">
                <h3>✨ AI House Generator</h3>
                <div className="mode-switcher">
                  <button 
                    className={`mode-btn ${generationMode === 'text' ? 'active' : ''}`}
                    onClick={() => setGenerationMode('text')}
                  >
                    📝 Text Mode
                  </button>
                  <button 
                    className={`mode-btn ${generationMode === 'form' ? 'active' : ''}`}
                    onClick={() => setGenerationMode('form')}
                  >
                    🔧 Advanced Mode
                  </button>
                </div>
              </div>
              
              {error && (
                <div className="error-message">
                  <span className="error-icon">⚠️</span>
                  {error}
                </div>
              )}

              {generationMode === 'text' ? (
                <div className="input-section">
                  <label htmlFor="textInput">Describe your Indian house:</label>
                  <textarea
                    id="textInput"
                    value={textInput}
                    onChange={handleInputChange}
                    placeholder="e.g., A traditional Indian house with 2 stories, red brick walls, wooden balcony, and a tiled roof..."
                    rows={4}
                    disabled={isGenerating}
                    className="text-input"
                  />
                  
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
                    <button 
                      type="button" 
                      className="example-btn"
                      onClick={() => setTextInput("A small cottage with garden, single floor, and wooden doors")}
                    >
                      Simple Cottage
                    </button>
                  </div>

                  <button 
                    onClick={handleTextToModel}
                    disabled={isGenerating || !textInput.trim()}
                    className="generate-button"
                  >
                    {isGenerating ? (
                      <>
                        <span className="loading-spinner"></span>
                        Generating...
                      </>
                    ) : (
                      'Generate 3D Model'
                    )}
                  </button>
                </div>
              ) : (
                <AdvancedForm 
                  onGenerate={handleGenerate}
                  isGenerating={isGenerating}
                />
              )}
            </div>
          </section>

          {/* Generated Model Display */}
          {generatedModel && (
            <section className="model-display-section">
              <div className="model-card">
                <h3>� Generated Indian House Model</h3>
                
                <div className="model-info">
                  <div className="model-section">
                    <h4>Original Description:</h4>
                    <p className="model-text">"{generatedModel.text}"</p>
                  </div>
                  
                  {generatedModel.attributes && (
                    <div className="model-section">
                      <h4>House Attributes:</h4>
                      <div className="attributes-grid">
                        <div className="attribute">
                          <span className="label">Stories:</span>
                          <span className="value">{generatedModel.attributes.stories || 'N/A'}</span>
                        </div>
                        <div className="attribute">
                          <span className="label">Style:</span>
                          <span className="value">{generatedModel.attributes.style || 'N/A'}</span>
                        </div>
                        <div className="attribute">
                          <span className="label">Colors:</span>
                          <span className="value">{generatedModel.attributes.colors?.join(', ') || 'N/A'}</span>
                        </div>
                        <div className="attribute">
                          <span className="label">Features:</span>
                          <span className="value">{generatedModel.attributes.features?.join(', ') || 'N/A'}</span>
                        </div>
                        <div className="attribute">
                          <span className="label">Materials:</span>
                          <span className="value">{generatedModel.attributes.materials?.join(', ') || 'N/A'}</span>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
                
                {/* 3D Model Viewer */}
                <div className="model-viewer">
                  {generatedModel.modelData ? (
                    <div className="threejs-container">
                      <h4>🎯 Interactive 3D Model</h4>
                      <ThreeJSViewer 
                        modelData={generatedModel.modelData} 
                        width={500} 
                        height={350}
                      />
                      <p className="viewer-info">
                        Use mouse to interact • Auto-rotating view
                      </p>
                    </div>
                  ) : (
                    <div className="model-placeholder">
                      <div className="rotating-cube">
                        <div className="cube-face front">🏠</div>
                        <div className="cube-face back">🏛️</div>
                        <div className="cube-face right">🎨</div>
                        <div className="cube-face left">AI</div>
                        <div className="cube-face top">⭐</div>
                        <div className="cube-face bottom">🚀</div>
                      </div>
                      <p>Indian House Model Preview</p>
                      <small>Processing Time: {generatedModel.processingTime || 'N/A'}</small>
                    </div>
                  )}
                </div>

                <div className="model-actions">
                  {generatedModel.files && generatedModel.files.length > 0 ? (
                    generatedModel.files.map((file, index) => (
                      <button 
                        key={index}
                        className="action-btn download-btn"
                        onClick={() => window.open(`http://localhost:5001${file.url}`, '_blank')}
                      >
                        📥 {file.type}
                      </button>
                    ))
                  ) : (
                    <button className="action-btn download-btn">
                      📥 Download Model
                    </button>
                  )}
                  <button className="action-btn view-btn">
                    👁️ View in Blender
                  </button>
                  <button className="action-btn share-btn">
                    🔗 Share Model
                  </button>
                </div>
                
                <div className="generation-details">
                  <small>Generated: {new Date(generatedModel.timestamp).toLocaleString()}</small>
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