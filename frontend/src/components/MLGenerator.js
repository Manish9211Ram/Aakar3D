import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './MLGenerator.css';

const MLGenerator = () => {
    const [description, setDescription] = useState('');
    const [selectedStyle, setSelectedStyle] = useState('');
    const [numFloors, setNumFloors] = useState(2);
    const [isGenerating, setIsGenerating] = useState(false);
    const [result, setResult] = useState(null);
    const [examples, setExamples] = useState([]);
    const [styles, setStyles] = useState([]);
    const [error, setError] = useState('');
    const [activeTab, setActiveTab] = useState('generate');

    useEffect(() => {
        fetchExamples();
        fetchStyles();
        checkMLServiceHealth();
    }, []);

    const checkMLServiceHealth = async () => {
        try {
            await axios.get('/api/ml/health');
            console.log('ML service is healthy');
        } catch (error) {
            setError('ML service is currently unavailable. Please try again later.');
        }
    };

    const fetchExamples = async () => {
        try {
            const response = await axios.get('/api/ml/examples');
            setExamples(response.data.examples);
        } catch (error) {
            console.error('Failed to fetch examples:', error);
        }
    };

    const fetchStyles = async () => {
        try {
            const response = await axios.get('/api/ml/styles');
            setStyles(response.data.styles);
        } catch (error) {
            console.error('Failed to fetch styles:', error);
        }
    };

    const generateHouse = async () => {
        if (!description.trim()) {
            setError('Please provide a house description');
            return;
        }

        setIsGenerating(true);
        setError('');
        setResult(null);

        try {
            const response = await axios.post('/api/ml/generate-house', {
                description,
                style: selectedStyle || undefined,
                floors: numFloors,
                outputName: `house_${Date.now()}`
            });

            if (response.data.success) {
                setResult(response.data.data);
                setError('');
            } else {
                setError(response.data.message || 'Generation failed');
            }
        } catch (error) {
            setError(error.response?.data?.message || 'An error occurred during generation');
        } finally {
            setIsGenerating(false);
        }
    };

    const generateExample = async (exampleId) => {
        setIsGenerating(true);
        setError('');
        setResult(null);

        try {
            const response = await axios.post(`/api/ml/generate-example/${exampleId}`);

            if (response.data.success) {
                setResult(response.data.data);
                setError('');
            } else {
                setError(response.data.message || 'Example generation failed');
            }
        } catch (error) {
            setError(error.response?.data?.message || 'An error occurred during example generation');
        } finally {
            setIsGenerating(false);
        }
    };

    const downloadFile = async (filename) => {
        try {
            const response = await axios.get(`/api/ml/download/${filename}`, {
                responseType: 'blob'
            });

            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', filename);
            document.body.appendChild(link);
            link.click();
            link.remove();
            window.URL.revokeObjectURL(url);
        } catch (error) {
            setError('Failed to download file');
        }
    };

    return (
        <div className="ml-generator">
            <div className="ml-header">
                <h2>🏛️ AI House Generator</h2>
                <p>Generate stunning 3D Indian house models from text descriptions</p>
            </div>

            <div className="ml-tabs">
                <button
                    className={`tab ${activeTab === 'generate' ? 'active' : ''}`}
                    onClick={() => setActiveTab('generate')}
                >
                    Generate Custom
                </button>
                <button
                    className={`tab ${activeTab === 'examples' ? 'active' : ''}`}
                    onClick={() => setActiveTab('examples')}
                >
                    Use Examples
                </button>
            </div>

            {error && (
                <div className="error-message">
                    <span>⚠️ {error}</span>
                    <button onClick={() => setError('')}>×</button>
                </div>
            )}

            {activeTab === 'generate' && (
                <div className="generate-tab">
                    <div className="input-section">
                        <div className="form-group">
                            <label>House Description</label>
                            <textarea
                                value={description}
                                onChange={(e) => setDescription(e.target.value)}
                                placeholder="Describe your dream house... e.g., 'modern 2 floor villa with 4 bedrooms, balcony, swimming pool, white and glass facade, 40x50 feet'"
                                rows={4}
                                disabled={isGenerating}
                            />
                        </div>

                        <div className="form-row">
                            <div className="form-group">
                                <label>Architectural Style (Optional)</label>
                                <select
                                    value={selectedStyle}
                                    onChange={(e) => setSelectedStyle(e.target.value)}
                                    disabled={isGenerating}
                                >
                                    <option value="">Auto-detect from description</option>
                                    {styles.map(style => (
                                        <option key={style} value={style}>
                                            {style.charAt(0).toUpperCase() + style.slice(1).replace('_', ' ')}
                                        </option>
                                    ))}
                                </select>
                            </div>

                            <div className="form-group">
                                <label>Number of Floors</label>
                                <select
                                    value={numFloors}
                                    onChange={(e) => setNumFloors(parseInt(e.target.value))}
                                    disabled={isGenerating}
                                >
                                    <option value={1}>1 Floor</option>
                                    <option value={2}>2 Floors</option>
                                    <option value={3}>3 Floors</option>
                                    <option value={4}>4 Floors</option>
                                    <option value={5}>5 Floors</option>
                                </select>
                            </div>
                        </div>

                        <button
                            className="generate-btn"
                            onClick={generateHouse}
                            disabled={isGenerating || !description.trim()}
                        >
                            {isGenerating ? (
                                <>
                                    <span className="spinner"></span>
                                    Generating House...
                                </>
                            ) : (
                                '🏗️ Generate House'
                            )}
                        </button>
                    </div>
                </div>
            )}

            {activeTab === 'examples' && (
                <div className="examples-tab">
                    <div className="examples-grid">
                        {examples.map(example => (
                            <div key={example.id} className="example-card">
                                <div className="example-image">
                                    <img
                                        src={example.image || '/placeholder-house.jpg'}
                                        alt={example.name}
                                        onError={(e) => {
                                            e.target.src = '/placeholder-house.jpg';
                                        }}
                                    />
                                </div>
                                <div className="example-content">
                                    <h4>{example.name}</h4>
                                    <p>{example.description}</p>
                                    <div className="example-style">
                                        Style: {example.style.charAt(0).toUpperCase() + example.style.slice(1)}
                                    </div>
                                    <button
                                        className="example-btn"
                                        onClick={() => generateExample(example.id)}
                                        disabled={isGenerating}
                                    >
                                        {isGenerating ? 'Generating...' : 'Generate This Design'}
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {isGenerating && (
                <div className="generation-progress">
                    <div className="progress-content">
                        <div className="spinner-large"></div>
                        <h3>🏗️ Generating Your House</h3>
                        <p>This may take a few minutes. Please wait...</p>
                        <div className="progress-steps">
                            <div className="step active">📝 Parsing description</div>
                            <div className="step active">🎨 Creating 3D model</div>
                            <div className="step active">🏠 Building structure</div>
                            <div className="step">💾 Saving files</div>
                        </div>
                    </div>
                </div>
            )}

            {result && (
                <div className="result-section">
                    <h3>✅ House Generated Successfully!</h3>
                    
                    <div className="result-info">
                        <div className="result-stats">
                            <div className="stat">
                                <span className="label">Processing Time:</span>
                                <span className="value">{result.processing_time?.toFixed(2)}s</span>
                            </div>
                            <div className="stat">
                                <span className="label">Style:</span>
                                <span className="value">{result.attributes?.style}</span>
                            </div>
                            <div className="stat">
                                <span className="label">Floors:</span>
                                <span className="value">{result.attributes?.num_floors}</span>
                            </div>
                            <div className="stat">
                                <span className="label">Type:</span>
                                <span className="value">{result.attributes?.house_type}</span>
                            </div>
                        </div>

                        <div className="result-attributes">
                            <h4>House Features:</h4>
                            <div className="features-list">
                                {result.attributes?.rooms?.map(room => (
                                    <span key={room} className="feature-tag">
                                        {room.replace('_', ' ')}
                                    </span>
                                ))}
                                {result.attributes?.features?.map(feature => (
                                    <span key={feature} className="feature-tag feature-special">
                                        {feature.replace('_', ' ')}
                                    </span>
                                ))}
                            </div>
                        </div>
                    </div>

                    <div className="download-section">
                        <h4>📁 Download Files:</h4>
                        <div className="download-buttons">
                            {result.files?.blend_file && (
                                <button
                                    className="download-btn blend"
                                    onClick={() => downloadFile(result.files.blend_file.split('/').pop())}
                                >
                                    📦 Download .blend File
                                </button>
                            )}
                            {result.files?.script_file && (
                                <button
                                    className="download-btn script"
                                    onClick={() => downloadFile(result.files.script_file.split('/').pop())}
                                >
                                    📄 Download Script
                                </button>
                            )}
                            {result.files?.metadata_file && (
                                <button
                                    className="download-btn metadata"
                                    onClick={() => downloadFile(result.files.metadata_file.split('/').pop())}
                                >
                                    📋 Download Metadata
                                </button>
                            )}
                        </div>
                    </div>

                    <div className="next-steps">
                        <h4>🎯 Next Steps:</h4>
                        <ul>
                            <li>Open the .blend file in Blender to view your 3D model</li>
                            <li>Customize materials, lighting, and camera angles</li>
                            <li>Render high-quality images or animations</li>
                            <li>Export to other 3D formats if needed</li>
                        </ul>
                    </div>
                </div>
            )}
        </div>
    );
};

export default MLGenerator;