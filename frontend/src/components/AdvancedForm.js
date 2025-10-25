import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './AdvancedForm.css';

const AdvancedForm = ({ onGenerate, isGenerating }) => {
  const [formData, setFormData] = useState({
    style: 'modern',
    house_type: 'bungalow',
    floors: 2,
    bedrooms: 3,
    bathrooms: 2,
    rooms: [],
    features: [],
    colors: ['white'],
    materials: ['brick'],
    windows: { style: 'standard', size: 'medium' },
    doors: { main_door: 'wooden' },
    budget: 'standard',
    area: { width: 12, length: 15 }
  });

  const [configOptions, setConfigOptions] = useState({});
  const [showAdvanced, setShowAdvanced] = useState(false);

  useEffect(() => {
    // Fetch configuration options
    axios.get('http://localhost:5000/api/ml/config-options')
      .then(response => {
        if (response.data.success) {
          setConfigOptions(response.data.data);
        }
      })
      .catch(error => console.error('Failed to load config options:', error));
  }, []);

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleNestedChange = (parent, field, value) => {
    setFormData(prev => ({
      ...prev,
      [parent]: {
        ...prev[parent],
        [field]: value
      }
    }));
  };

  const handleArrayChange = (field, value, checked) => {
    setFormData(prev => ({
      ...prev,
      [field]: checked 
        ? [...prev[field], value]
        : prev[field].filter(item => item !== value)
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onGenerate(formData, 'form');
  };

  return (
    <div className="advanced-form-container">
      <div className="form-header">
        <h3>🏗️ Advanced House Designer</h3>
        <button 
          type="button"
          className="toggle-advanced"
          onClick={() => setShowAdvanced(!showAdvanced)}
        >
          {showAdvanced ? '📝 Simple Mode' : '⚙️ Advanced Mode'}
        </button>
      </div>

      <form onSubmit={handleSubmit} className="house-form">
        {/* Basic Configuration */}
        <div className="form-section">
          <h4>🏠 Basic Configuration</h4>
          
          <div className="form-row">
            <div className="form-group">
              <label>Style</label>
              <select 
                value={formData.style}
                onChange={(e) => handleInputChange('style', e.target.value)}
              >
                {configOptions.styles?.map(style => (
                  <option key={style} value={style}>
                    {style.charAt(0).toUpperCase() + style.slice(1)}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>House Type</label>
              <select
                value={formData.house_type}
                onChange={(e) => handleInputChange('house_type', e.target.value)}
              >
                {configOptions.house_types?.map(type => (
                  <option key={type} value={type}>
                    {type.charAt(0).toUpperCase() + type.slice(1)}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Floors</label>
              <input
                type="number"
                min="1"
                max="5"
                value={formData.floors}
                onChange={(e) => handleInputChange('floors', parseInt(e.target.value))}
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Bedrooms</label>
              <input
                type="number"
                min="1"
                max="10"
                value={formData.bedrooms}
                onChange={(e) => handleInputChange('bedrooms', parseInt(e.target.value))}
              />
            </div>

            <div className="form-group">
              <label>Bathrooms</label>
              <input
                type="number"
                min="1"
                max="8"
                value={formData.bathrooms}
                onChange={(e) => handleInputChange('bathrooms', parseInt(e.target.value))}
              />
            </div>

            <div className="form-group">
              <label>Budget Tier</label>
              <select
                value={formData.budget}
                onChange={(e) => handleInputChange('budget', e.target.value)}
              >
                {configOptions.budget_tiers?.map(tier => (
                  <option key={tier} value={tier}>
                    {tier.charAt(0).toUpperCase() + tier.slice(1)}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Advanced Configuration */}
        {showAdvanced && (
          <>
            {/* Room Selection */}
            <div className="form-section">
              <h4>🚪 Room Selection</h4>
              <div className="checkbox-grid">
                {configOptions.room_types?.map(room => (
                  <label key={room} className="checkbox-item">
                    <input
                      type="checkbox"
                      checked={formData.rooms.includes(room)}
                      onChange={(e) => handleArrayChange('rooms', room, e.target.checked)}
                    />
                    <span>{room.replace('_', ' ').toUpperCase()}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* Features */}
            <div className="form-section">
              <h4>✨ Features</h4>
              <div className="checkbox-grid">
                {configOptions.features?.map(feature => (
                  <label key={feature} className="checkbox-item">
                    <input
                      type="checkbox"
                      checked={formData.features.includes(feature)}
                      onChange={(e) => handleArrayChange('features', feature, e.target.checked)}
                    />
                    <span>{feature.replace('_', ' ').toUpperCase()}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* Colors & Materials */}
            <div className="form-section">
              <h4>🎨 Colors & Materials</h4>
              
              <div className="subsection">
                <label>Colors</label>
                <div className="checkbox-grid">
                  {configOptions.colors?.map(color => (
                    <label key={color} className="checkbox-item color-item">
                      <input
                        type="checkbox"
                        checked={formData.colors.includes(color)}
                        onChange={(e) => handleArrayChange('colors', color, e.target.checked)}
                      />
                      <span className={`color-swatch color-${color}`}></span>
                      <span>{color.toUpperCase()}</span>
                    </label>
                  ))}
                </div>
              </div>

              <div className="subsection">
                <label>Materials</label>
                <div className="checkbox-grid">
                  {configOptions.materials?.map(material => (
                    <label key={material} className="checkbox-item">
                      <input
                        type="checkbox"
                        checked={formData.materials.includes(material)}
                        onChange={(e) => handleArrayChange('materials', material, e.target.checked)}
                      />
                      <span>{material.toUpperCase()}</span>
                    </label>
                  ))}
                </div>
              </div>
            </div>

            {/* Dimensions */}
            <div className="form-section">
              <h4>📐 Dimensions</h4>
              <div className="form-row">
                <div className="form-group">
                  <label>Width (meters)</label>
                  <input
                    type="number"
                    min="5"
                    max="50"
                    value={formData.area.width}
                    onChange={(e) => handleNestedChange('area', 'width', parseInt(e.target.value))}
                  />
                </div>
                <div className="form-group">
                  <label>Length (meters)</label>
                  <input
                    type="number"
                    min="5"
                    max="50"
                    value={formData.area.length}
                    onChange={(e) => handleNestedChange('area', 'length', parseInt(e.target.value))}
                  />
                </div>
              </div>
            </div>

            {/* Windows & Doors */}
            <div className="form-section">
              <h4>🪟 Windows & Doors</h4>
              <div className="form-row">
                <div className="form-group">
                  <label>Window Style</label>
                  <select
                    value={formData.windows.style}
                    onChange={(e) => handleNestedChange('windows', 'style', e.target.value)}
                  >
                    {configOptions.window_styles?.map(style => (
                      <option key={style} value={style}>
                        {style.charAt(0).toUpperCase() + style.slice(1)}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="form-group">
                  <label>Door Type</label>
                  <select
                    value={formData.doors.main_door}
                    onChange={(e) => handleNestedChange('doors', 'main_door', e.target.value)}
                  >
                    {configOptions.door_types?.map(type => (
                      <option key={type} value={type}>
                        {type.charAt(0).toUpperCase() + type.slice(1)}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            </div>
          </>
        )}

        {/* Submit */}
        <div className="form-section">
          <button 
            type="submit" 
            className="generate-btn"
            disabled={isGenerating}
          >
            {isGenerating ? '🔄 Generating...' : '🏗️ Generate House'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default AdvancedForm;