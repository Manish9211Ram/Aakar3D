"""
Main Pipeline for Indian House Blender Generation
Complete pipeline for generating Blender files from text descriptions
"""

import os
import time
import subprocess
from datetime import datetime
from typing import Dict
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.text_parser import EnhancedIndianHouseParser
from models.blender_generator import BlenderScriptGenerator

class IndianHouseBlenderPipeline:
    """Complete pipeline for generating Blender files"""
    
    def __init__(self, config = None):
        if config is None:
            from utils.config import IndianHouseBlenderConfig
            config = IndianHouseBlenderConfig()
        
        self.config = config
        
        print("\n" + "="*90)
        print(" "*20 + "INDIAN HOUSE BLENDER PIPELINE INITIALIZED")
        print("="*90)
        
        self.parser = EnhancedIndianHouseParser(self.config)
        self.blender_generator = BlenderScriptGenerator()
        
        print("\n✓ Pipeline ready")
        print("="*90 + "\n")
    
    def generate_blender_file(
        self,
        text: str,
        output_name: str = None
    ) -> Dict:
        """
        Generate .blend file from text description
        
        Args:
            text: House description
            output_name: Output filename
        
        Returns:
            Result dictionary
        """
        print("\n" + "="*90)
        print("🏗  INDIAN HOUSE BLENDER GENERATION")
        print("="*90)
        print(f"Input: {text}")
        print("="*90 + "\n")
        
        start_time = time.time()
        
        try:
            # Parse text
            attributes = self.parser.parse_text(text)
            
            # Generate output name
            if output_name is None:
                output_name = self._text_to_filename(text)
            
            # Paths
            blend_path = os.path.join(self.config.output_dir, f"{output_name}.blend")
            script_path = os.path.join(self.config.output_dir, f"{output_name}_script.py")
            
            # Generate Blender script
            print("\n📝 Generating Blender script...")
            script = self.blender_generator.generate_blender_script(
                mesh_data={},
                attributes=attributes,
                output_blend_path=blend_path
            )
            
            # Save script
            self.blender_generator.save_script(script, script_path)
            
            # Execute Blender script
            print("\n🎨 Executing Blender...")
            self._execute_blender_script(script_path)
            
            # Create metadata
            metadata = self._create_metadata(attributes, output_name)
            
            processing_time = time.time() - start_time
            
            print("\n" + "="*90)
            print("✓ BLENDER FILE GENERATED!")
            print("="*90)
            print(f"⏱  Time: {processing_time:.2f}s")
            print(f"📁 Output: {blend_path}")
            print(f"📄 Script: {script_path}")
            print(f"📋 Metadata: {metadata['path']}")
            print("="*90 + "\n")
            
            return {
                'success': True,
                'text': text,
                'attributes': attributes,
                'blend_file': blend_path,
                'script_file': script_path,
                'metadata_file': metadata['path'],
                'processing_time': processing_time
            }
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'error': str(e)
            }
    
    def _execute_blender_script(self, script_path: str):
        """Execute Blender script"""
        try:
            # Try running Blender
            cmd = [
                self.config.blender_executable,
                '--background',
                '--python', script_path
            ]
            
            print(f"  Running: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                print("  ✓ Blender execution successful")
            else:
                print(f"  ⚠  Blender warnings: {result.stderr}")
                
        except FileNotFoundError:
            print("  ⚠  Blender not found in PATH")
            print("  ℹ  Script saved - run manually with:")
            print(f"     blender --background --python {script_path}")
        except Exception as e:
            print(f"  ⚠  Execution error: {e}")
            print(f"  ℹ  Run manually: blender --background --python {script_path}")
    
    def _text_to_filename(self, text: str) -> str:
        """Convert text to filename"""
        words = text.lower().split()[:6]
        filename = "_".join(w for w in words if w.isalnum())
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"indian_house_{filename}_{timestamp}"
    
    def _create_metadata(self, attributes: Dict, output_name: str) -> Dict:
        """Create metadata file"""
        import json
        
        metadata = {
            'text_description': attributes['text'],
            'generation_date': datetime.now().isoformat(),
            'user': 'aakar3d_user',
            'attributes': {
                'num_floors': attributes['num_floors'],
                'style': attributes['style'],
                'house_type': attributes['house_type'],
                'roof_type': attributes['roof_type'],
                'rooms': attributes['rooms'],
                'dimensions': attributes['dimensions'],
                'features': attributes['features'],
                'materials': attributes['materials'],
                'colors': attributes['colors']
            },
            'files': {
                'blend_file': f"{output_name}.blend",
                'script_file': f"{output_name}_script.py"
            }
        }
        
        metadata_path = os.path.join(self.config.output_dir, f"{output_name}_metadata.json")
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"  ✓ Metadata: {metadata_path}")
        
        return {'path': metadata_path, 'data': metadata}