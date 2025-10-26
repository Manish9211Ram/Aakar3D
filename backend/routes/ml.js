/**
 * ML Service Integration for Aakar3D
 * Express.js routes for Indian House Blender Generator
 */

const express = require('express');
const axios = require('axios');
const multer = require('multer');
const path = require('path');
const fs = require('fs');

const router = express.Router();

// ML Service Configuration
const ML_SERVICE_URL = process.env.ML_SERVICE_URL || 'http://localhost:5001';
const UPLOAD_DIR = path.join(__dirname, '../../uploads/ml-generated');

// Ensure upload directory exists
if (!fs.existsSync(UPLOAD_DIR)) {
    fs.mkdirSync(UPLOAD_DIR, { recursive: true });
}

// Configure multer for file uploads
const storage = multer.diskStorage({
    destination: UPLOAD_DIR,
    filename: (req, file, cb) => {
        const timestamp = Date.now();
        cb(null, `${timestamp}-${file.originalname}`);
    }
});

const upload = multer({ storage });

/**
 * @route   GET /api/ml/health
 * @desc    Check ML service health
 * @access  Public
 */
router.get('/health', async (req, res) => {
    try {
        const response = await axios.get(`${ML_SERVICE_URL}/health`, {
            timeout: 5000
        });
        
        res.json({
            success: true,
            message: 'ML service is healthy',
            mlService: response.data
        });
    } catch (error) {
        console.error('ML service health check failed:', error.message);
        res.status(503).json({
            success: false,
            message: 'ML service unavailable',
            error: error.message
        });
    }
});

/**
 * @route   POST /api/ml/generate-house
 * @desc    Generate house from text description
 * @access  Private (requires authentication)
 */
router.post('/generate-house', async (req, res) => {
    try {
        const { description, style, floors, outputName } = req.body;
        
        if (!description) {
            return res.status(400).json({
                success: false,
                message: 'House description is required'
            });
        }
        
        // Call ML service
        const response = await axios.post(`${ML_SERVICE_URL}/generate`, {
            description,
            style,
            floors,
            output_name: outputName
        }, {
            timeout: 300000 // 5 minutes timeout for generation
        });
        
        if (response.data.success) {
            // Store generation record in database (if you have user model)
            // const generationRecord = {
            //     userId: req.user.id,
            //     description,
            //     style,
            //     floors,
            //     files: response.data.data.files,
            //     attributes: response.data.data.attributes,
            //     createdAt: new Date()
            // };
            
            res.json({
                success: true,
                message: 'House generated successfully',
                data: response.data.data
            });
        } else {
            res.status(500).json({
                success: false,
                message: 'House generation failed',
                error: response.data.error
            });
        }
        
    } catch (error) {
        console.error('House generation error:', error.message);
        res.status(500).json({
            success: false,
            message: 'Server error during house generation',
            error: error.message
        });
    }
});

/**
 * @route   GET /api/ml/examples
 * @desc    Get example house descriptions
 * @access  Public
 */
router.get('/examples', async (req, res) => {
    try {
        const response = await axios.get(`${ML_SERVICE_URL}/generate/examples`);
        
        res.json({
            success: true,
            examples: response.data.examples
        });
    } catch (error) {
        console.error('Failed to fetch examples:', error.message);
        res.status(500).json({
            success: false,
            message: 'Failed to fetch examples',
            error: error.message
        });
    }
});

/**
 * @route   POST /api/ml/generate-example/:exampleId
 * @desc    Generate house from predefined example
 * @access  Private (requires authentication)
 */
router.post('/generate-example/:exampleId', async (req, res) => {
    try {
        const { exampleId } = req.params;
        
        const response = await axios.post(`${ML_SERVICE_URL}/generate/example/${exampleId}`, {}, {
            timeout: 300000 // 5 minutes timeout
        });
        
        if (response.data.success) {
            res.json({
                success: true,
                message: `Example '${exampleId}' generated successfully`,
                data: response.data.data
            });
        } else {
            res.status(500).json({
                success: false,
                message: 'Example generation failed',
                error: response.data.error
            });
        }
        
    } catch (error) {
        console.error('Example generation error:', error.message);
        res.status(500).json({
            success: false,
            message: 'Server error during example generation',
            error: error.message
        });
    }
});

/**
 * @route   GET /api/ml/styles
 * @desc    Get available architectural styles and options
 * @access  Public
 */
router.get('/styles', async (req, res) => {
    try {
        const response = await axios.get(`${ML_SERVICE_URL}/styles`);
        
        res.json({
            success: true,
            styles: response.data.styles,
            houseTypes: response.data.house_types,
            roofTypes: response.data.roof_types,
            roomTypes: response.data.room_types,
            features: response.data.features
        });
    } catch (error) {
        console.error('Failed to fetch styles:', error.message);
        res.status(500).json({
            success: false,
            message: 'Failed to fetch architectural styles',
            error: error.message
        });
    }
});

/**
 * @route   GET /api/ml/download/:filename
 * @desc    Download generated files
 * @access  Private (requires authentication)
 */
router.get('/download/:filename', async (req, res) => {
    try {
        const { filename } = req.params;
        
        const response = await axios.get(`${ML_SERVICE_URL}/download/${filename}`, {
            responseType: 'stream'
        });
        
        // Set appropriate headers
        res.set({
            'Content-Type': response.headers['content-type'],
            'Content-Disposition': response.headers['content-disposition'] || `attachment; filename="${filename}"`
        });
        
        // Pipe the file stream to response
        response.data.pipe(res);
        
    } catch (error) {
        console.error('File download error:', error.message);
        res.status(404).json({
            success: false,
            message: 'File not found or download failed',
            error: error.message
        });
    }
});

/**
 * @route   GET /api/ml/status
 * @desc    Get ML service status and configuration
 * @access  Public
 */
router.get('/status', async (req, res) => {
    try {
        const response = await axios.get(`${ML_SERVICE_URL}/status`);
        
        res.json({
            success: true,
            mlService: response.data.status,
            integration: {
                version: '1.0.0',
                serviceUrl: ML_SERVICE_URL,
                uploadDir: UPLOAD_DIR
            }
        });
    } catch (error) {
        console.error('ML status check failed:', error.message);
        res.status(503).json({
            success: false,
            message: 'ML service status unavailable',
            error: error.message
        });
    }
});

/**
 * @route   POST /api/ml/bulk-generate
 * @desc    Generate multiple houses from batch descriptions
 * @access  Private (requires authentication)
 */
router.post('/bulk-generate', upload.single('descriptionsFile'), async (req, res) => {
    try {
        let descriptions = [];
        
        if (req.file) {
            // Read descriptions from uploaded file
            const fileContent = fs.readFileSync(req.file.path, 'utf8');
            descriptions = fileContent.split('\n').filter(line => line.trim());
        } else if (req.body.descriptions) {
            // Get descriptions from request body
            descriptions = Array.isArray(req.body.descriptions) 
                ? req.body.descriptions 
                : [req.body.descriptions];
        } else {
            return res.status(400).json({
                success: false,
                message: 'No descriptions provided'
            });
        }
        
        const results = [];
        const errors = [];
        
        // Process each description
        for (let i = 0; i < descriptions.length; i++) {
            try {
                const description = descriptions[i].trim();
                if (!description) continue;
                
                const response = await axios.post(`${ML_SERVICE_URL}/generate`, {
                    description,
                    output_name: `batch_${i + 1}_${Date.now()}`
                }, {
                    timeout: 300000 // 5 minutes per generation
                });
                
                if (response.data.success) {
                    results.push({
                        index: i + 1,
                        description,
                        ...response.data.data
                    });
                } else {
                    errors.push({
                        index: i + 1,
                        description,
                        error: response.data.error
                    });
                }
                
            } catch (error) {
                errors.push({
                    index: i + 1,
                    description: descriptions[i],
                    error: error.message
                });
            }
        }
        
        // Clean up uploaded file
        if (req.file) {
            fs.unlinkSync(req.file.path);
        }
        
        res.json({
            success: true,
            message: `Batch generation completed. ${results.length} successful, ${errors.length} failed.`,
            results,
            errors,
            summary: {
                total: descriptions.length,
                successful: results.length,
                failed: errors.length
            }
        });
        
    } catch (error) {
        console.error('Bulk generation error:', error.message);
        res.status(500).json({
            success: false,
            message: 'Bulk generation failed',
            error: error.message
        });
    }
});

module.exports = router;