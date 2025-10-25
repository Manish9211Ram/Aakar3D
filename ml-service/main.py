# ============================================================================
# INDIAN HOUSE TEXT-TO-BLENDER GENERATOR - ML AAKAR3D
# Complete AI/ML Pipeline with .blend file output
# Date: 2025-10-25 18:45:07 UTC
# User: micmoodz
# ============================================================================

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader

import numpy as np
import cv2
from PIL import Image
import trimesh
import open3d as o3d

import os
import sys
import json
import time
import re
import warnings
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Union
from datetime import datetime
from dataclasses import dataclass, field
import tempfile
import shutil
from collections import defaultdict

from transformers import (
    DistilBertTokenizer,
    DistilBertModel,
)
from sentence_transformers import SentenceTransformer
from skimage import measure

# Import our custom modules
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.text_parser import EnhancedIndianHouseParser
from models.blender_generator import BlenderScriptGenerator
from utils.config import IndianHouseBlenderConfig
from api.pipeline import IndianHouseBlenderPipeline

warnings.filterwarnings('ignore')

# Set seeds for reproducibility
torch.manual_seed(42)
np.random.seed(42)

print("="*90)
print(" "*20 + "INDIAN HOUSE TEXT-TO-BLENDER GENERATOR")
print(" "*32 + "ML AAKAR3D v3.0")
print("="*90)
print("\n🚀 Dependencies loaded...")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function"""
    print("\n" + "🏛 "*40)
    print("INDIAN HOUSE BLENDER GENERATOR")
    print("Generate complete .blend files from text descriptions")
    print("🏛 "*40 + "\n")
    
    config = IndianHouseBlenderConfig()
    pipeline = IndianHouseBlenderPipeline(config)
    
    print("\n📋 Supported Features:")
    print("  ✓ All Indian architectural styles")
    print("  ✓ Multiple house types (bungalow, villa, duplex, haveli, etc.)")
    print("  ✓ Comprehensive room types")
    print("  ✓ Traditional features (jali, courtyard, veranda, etc.)")
    print("  ✓ Complete Blender scene with lighting and materials")
    print("\n" + "="*90 + "\n")
    
    return pipeline

# ============================================================================
# QUICK FUNCTIONS FOR API INTEGRATION
# ============================================================================

def quick_generate(text: str = None, output_dir: str = None):
    """Quick generation for API calls"""
    if not text:
        return {"success": False, "error": "No text description provided"}
    
    config = IndianHouseBlenderConfig()
    if output_dir:
        config.output_dir = output_dir
        
    pipeline = IndianHouseBlenderPipeline(config)
    result = pipeline.generate_blender_file(text)
    
    return result

def generate_house_api(
    description: str,
    style: str = None,
    floors: int = None,
    output_dir: str = "./output"
) -> Dict:
    """
    API function for generating houses
    
    Args:
        description: Text description of the house
        style: Optional architectural style override
        floors: Optional number of floors override
        output_dir: Output directory for files
    
    Returns:
        Dict with generation results
    """
    try:
        # Enhanced description with overrides
        enhanced_desc = description
        if style:
            enhanced_desc += f" in {style} style"
        if floors:
            enhanced_desc += f" with {floors} floors"
        
        result = quick_generate(enhanced_desc, output_dir)
        
        if result['success']:
            return {
                "success": True,
                "message": "House generated successfully",
                "files": {
                    "blend_file": result['blend_file'],
                    "script_file": result['script_file'],
                    "metadata_file": result['metadata_file']
                },
                "attributes": result['attributes'],
                "processing_time": result['processing_time']
            }
        else:
            return {
                "success": False,
                "error": result.get('error', 'Unknown error'),
                "message": "Failed to generate house"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Exception occurred during generation"
        }

# Example generators for testing
def example_kerala():
    return quick_generate("traditional Kerala nalukettu house with courtyard, sloped roof, veranda, 2 floors, 4 bedrooms, wooden pillars, red tiles")

def example_rajasthani():
    return quick_generate("Rajasthani haveli with jali work, courtyard, fountain, 3 floors, 6 bedrooms, dome, sandstone, terrace")

def example_modern():
    return quick_generate("modern 3 floor villa with glass facade, 5 bedrooms, terrace garden, swimming pool, parking, white and grey, 50x60 feet")

def example_colonial():
    return quick_generate("colonial bungalow with pillars, veranda, 2 floors, 6 bedrooms, compound wall, garden, white with brown trim")

if __name__ == "__main__":
    print("\n" + "="*90)
    print("INDIAN HOUSE BLENDER GENERATOR - READY!")
    print("="*90)
    print("\n📝 Quick Commands:")
    print("   main()                                     # Initialize pipeline")
    print("   quick_generate('your description')         # Quick generate")
    print("   generate_house_api('description')          # API function")
    print("   example_kerala()                           # Kerala nalukettu")
    print("   example_rajasthani()                       # Rajasthani haveli")
    print("   example_modern()                           # Modern villa")
    print("   example_colonial()                         # Colonial bungalow")
    print("\n💡 Example Usage:")
    print('   quick_generate("modern 2 floor house with 4 bedrooms, balcony, parking")')
    print('   generate_house_api("traditional Kerala house with courtyard and sloped roof")')
    print("\n📦 Output: Complete .blend files with:")
    print("   ✓ Full 3D house model")
    print("   ✓ Materials and textures")
    print("   ✓ Lighting setup")
    print("   ✓ Camera positioning")
    print("   ✓ Landscaping elements")
    print("\n" + "="*90 + "\n")
    
    # Initialize the main pipeline
    pipeline = main()