"""
Configuration module for Indian House Blender Generator
"""

import os
from dataclasses import dataclass, field
from typing import List

@dataclass
class IndianHouseBlenderConfig:
    """Configuration for Indian house Blender generation"""
    
    device: str = "cuda" if __name__ == "__main__" else "cpu"  # Will be set properly in main
    
    # Text encoder
    text_model: str = "distilbert-base-uncased"
    text_embedding_dim: int = 768
    max_text_length: int = 128
    
    # Architectural styles
    architectural_styles: List[str] = field(default_factory=lambda: [
        'modern', 'traditional', 'colonial', 'contemporary',
        'kerala', 'rajasthani', 'bengali', 'south_indian',
        'gujarati', 'punjabi', 'maharashtrian', 'kashmiri'
    ])
    
    # House types
    house_types: List[str] = field(default_factory=lambda: [
        'bungalow', 'villa', 'duplex', 'row_house',
        'haveli', 'cottage', 'farmhouse', 'apartment'
    ])
    
    # Roof types
    roof_types: List[str] = field(default_factory=lambda: [
        'flat', 'sloped', 'gabled', 'hipped', 'mansard', 'dome'
    ])
    
    # Room types
    room_types: List[str] = field(default_factory=lambda: [
        'bedroom', 'living_room', 'kitchen', 'bathroom',
        'dining_room', 'balcony', 'terrace', 'puja_room',
        'courtyard', 'veranda', 'garage', 'study',
        'guest_room', 'servant_quarter', 'store_room'
    ])
    
    # Features
    feature_types: List[str] = field(default_factory=lambda: [
        'pillars', 'arches', 'dome', 'jali', 'courtyard',
        'fountain', 'garden', 'gate', 'compound_wall',
        'parking', 'swimming_pool', 'terrace_garden'
    ])
    
    # Output settings
    output_dir: str = "./indian_house_blender_output"
    blender_executable: str = "blender"  # or full path
    
    def __post_init__(self):
        """Initialize configuration after creation"""
        try:
            import torch
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        except ImportError:
            self.device = "cpu"
            
        os.makedirs(self.output_dir, exist_ok=True)
        print(f"✓ Configuration initialized")
        print(f"  Device: {self.device}")
        print(f"  Output: {self.output_dir}")