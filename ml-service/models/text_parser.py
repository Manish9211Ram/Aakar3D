"""
Enhanced Indian House Text Parser
Comprehensive NLU for Indian house understanding
"""

import re
import math
from typing import Dict, List, Optional
from transformers import DistilBertTokenizer, DistilBertModel

class EnhancedIndianHouseParser:
    """Enhanced NLU for comprehensive Indian house understanding"""
    
    def __init__(self, config):
        self.config = config
        
        print("\n🔍 Loading enhanced text parser...")
        
        # Load models
        self.tokenizer = DistilBertTokenizer.from_pretrained(config.text_model)
        self.text_encoder = DistilBertModel.from_pretrained(config.text_model)
        self.text_encoder.to(config.device)
        self.text_encoder.eval()
        
        print("✓ Enhanced parser initialized")
    
    def parse_text(self, text: str) -> Dict:
        """Parse text with comprehensive attribute extraction"""
        print(f"\n📝 Parsing: {text}")
        
        text_lower = text.lower()
        
        # Extract all attributes
        attributes = {
            'text': text,
            'num_floors': self._extract_floors(text_lower),
            'style': self._extract_style(text_lower),
            'house_type': self._extract_house_type(text_lower),
            'roof_type': self._extract_roof_type(text_lower),
            'rooms': self._extract_rooms(text_lower),
            'dimensions': self._extract_dimensions(text_lower),
            'features': self._extract_features(text_lower),
            'materials': self._extract_materials(text_lower),
            'colors': self._extract_colors(text_lower),
            'budget': self._extract_budget(text_lower),
            'orientation': self._extract_orientation(text_lower)
        }
        
        print(f"  ✓ Style: {attributes['style']}")
        print(f"  ✓ Type: {attributes['house_type']}")
        print(f"  ✓ Floors: {attributes['num_floors']}")
        print(f"  ✓ Rooms: {', '.join(attributes['rooms'][:5])}")
        print(f"  ✓ Features: {', '.join(attributes['features'][:5])}")
        
        return attributes
    
    def _extract_floors(self, text: str) -> int:
        """Extract number of floors"""
        patterns = [
            (r'(\d+)\s*(?:floor|story|storey|level)', lambda m: int(m.group(1))),
            (r'g\+(\d+)', lambda m: int(m.group(1)) + 1),
            (r'ground\s*\+\s*(\d+)', lambda m: int(m.group(1)) + 1),
            (r'single\s*floor', lambda m: 1),
            (r'double\s*floor|duplex', lambda m: 2),
            (r'triple\s*floor', lambda m: 3),
            (r'(\d+)\s*bhk', lambda m: max(1, min(3, int(m.group(1)) // 2)))
        ]
        
        for pattern, extractor in patterns:
            match = re.search(pattern, text)
            if match:
                return max(1, min(extractor(match), 5))
        
        return 2  # Default
    
    def _extract_style(self, text: str) -> str:
        """Extract architectural style"""
        style_keywords = {
            'modern': ['modern', 'contemporary', 'minimalist', 'sleek', 'new age'],
            'traditional': ['traditional', 'classic', 'heritage', 'vintage', 'ethnic'],
            'colonial': ['colonial', 'british', 'european', 'victorian'],
            'kerala': ['kerala', 'nalukettu', 'ettukettu', 'malabar', 'mangalore'],
            'rajasthani': ['rajasthani', 'haveli', 'rajput', 'jaipur', 'jodhpur'],
            'bengali': ['bengali', 'kolkata', 'calcutta', 'bengal'],
            'south_indian': ['south indian', 'tamil', 'chettinad', 'dravidian', 'andhra'],
            'gujarati': ['gujarati', 'gujarat', 'ahmedabad', 'pol'],
            'punjabi': ['punjabi', 'punjab', 'chandigarh'],
            'maharashtrian': ['maharashtrian', 'marathi', 'wada'],
            'kashmiri': ['kashmiri', 'kashmir', 'srinagar'],
            'contemporary': ['contemporary', 'ultra modern', 'futuristic']
        }
        
        for style, keywords in style_keywords.items():
            if any(kw in text for kw in keywords):
                return style
        
        return 'modern'
    
    def _extract_house_type(self, text: str) -> str:
        """Extract house type"""
        type_keywords = {
            'bungalow': ['bungalow', 'single family'],
            'villa': ['villa', 'luxury house'],
            'duplex': ['duplex', 'double floor'],
            'row_house': ['row house', 'townhouse'],
            'haveli': ['haveli', 'mansion'],
            'cottage': ['cottage', 'small house'],
            'farmhouse': ['farmhouse', 'farm house', 'country house'],
            'apartment': ['apartment', 'flat', 'unit']
        }
        
        for house_type, keywords in type_keywords.items():
            if any(kw in text for kw in keywords):
                return house_type
        
        return 'bungalow'
    
    def _extract_roof_type(self, text: str) -> str:
        """Extract roof type"""
        roof_keywords = {
            'flat': ['flat roof', 'terrace'],
            'sloped': ['sloped roof', 'slanting roof', 'pitched roof'],
            'gabled': ['gabled', 'gable roof'],
            'hipped': ['hipped', 'hip roof'],
            'mansard': ['mansard'],
            'dome': ['dome', 'cupola']
        }
        
        for roof_type, keywords in roof_keywords.items():
            if any(kw in text for kw in keywords):
                return roof_type
        
        # Default based on style
        return 'sloped' if 'traditional' in text or 'kerala' in text else 'flat'
    
    def _extract_rooms(self, text: str) -> List[str]:
        """Extract room types"""
        rooms = []
        
        room_patterns = {
            'bedroom': [r'(\d+)\s*(?:bed|bedroom|bhk)', 'bedroom'],
            'living_room': ['living room', 'living', 'hall', 'sitting'],
            'kitchen': ['kitchen', 'cooking'],
            'bathroom': [r'(\d+)\s*bath', 'bathroom', 'toilet'],
            'dining_room': ['dining', 'dining room'],
            'balcony': ['balcony', 'balconies'],
            'terrace': ['terrace', 'rooftop'],
            'puja_room': ['puja room', 'pooja', 'prayer room', 'mandir'],
            'courtyard': ['courtyard', 'central court'],
            'veranda': ['veranda', 'verandah', 'porch'],
            'garage': ['garage', 'parking', 'car porch'],
            'study': ['study', 'office', 'work room'],
            'guest_room': ['guest room', 'guest bedroom'],
            'servant_quarter': ['servant quarter', 'servant room', 'helper room'],
            'store_room': ['store room', 'storage', 'pantry']
        }
        
        for room_type, patterns in room_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    rooms.append(room_type)
                    break
        
        # Ensure minimum rooms
        if not rooms:
            rooms = ['living_room', 'bedroom', 'kitchen', 'bathroom']
        
        return list(set(rooms))
    
    def _extract_dimensions(self, text: str) -> Dict:
        """Extract dimensions"""
        dims = {'width': 10.0, 'length': 12.0, 'height': 3.0}
        
        # Area patterns
        patterns = [
            r'(\d+)\s*x\s*(\d+)\s*(?:feet|ft|meter|m)',
            r'(\d+)\s*(?:sq\.?\s*)?(?:feet|ft)\s*x\s*(\d+)',
            r'(\d+)x(\d+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                w, l = float(match.group(1)), float(match.group(2))
                
                # Convert feet to meters if needed
                if 'feet' in text or 'ft' in text:
                    w *= 0.3048
                    l *= 0.3048
                
                dims['width'] = w
                dims['length'] = l
                break
        
        # Square footage
        sqft_match = re.search(r'(\d+)\s*(?:sq\.?\s*)?(?:feet|ft|sqft)', text)
        if sqft_match and not any(p in text for p in ['x', 'X']):
            sqft = float(sqft_match.group(1))
            sqm = sqft * 0.092903
            side = math.sqrt(sqm)
            dims['width'] = side
            dims['length'] = side * 1.2
        
        return dims
    
    def _extract_features(self, text: str) -> List[str]:
        """Extract architectural features"""
        features = []
        
        feature_keywords = {
            'pillars': ['pillar', 'column'],
            'arches': ['arch', 'archway'],
            'dome': ['dome', 'cupola'],
            'jali': ['jali', 'lattice', 'jaali'],
            'courtyard': ['courtyard', 'central court', 'atrium'],
            'fountain': ['fountain', 'water feature'],
            'garden': ['garden', 'lawn', 'landscaping'],
            'gate': ['gate', 'entrance gate', 'main gate'],
            'compound_wall': ['compound wall', 'boundary wall', 'fence', 'compound'],
            'parking': ['parking', 'garage', 'car porch'],
            'swimming_pool': ['swimming pool', 'pool'],
            'terrace_garden': ['terrace garden', 'roof garden']
        }
        
        for feature, keywords in feature_keywords.items():
            if any(kw in text for kw in keywords):
                features.append(feature)
        
        return features
    
    def _extract_materials(self, text: str) -> List[str]:
        """Extract building materials"""
        materials = []
        
        material_keywords = [
            'brick', 'concrete', 'wood', 'timber', 'stone',
            'marble', 'granite', 'tiles', 'glass', 'steel',
            'mud', 'clay', 'terracotta', 'sandstone', 'limestone',
            'rcc', 'cement', 'plaster'
        ]
        
        for material in material_keywords:
            if material in text:
                materials.append(material)
        
        return materials if materials else ['concrete', 'brick']
    
    def _extract_colors(self, text: str) -> List[str]:
        """Extract colors"""
        colors = []
        
        color_keywords = [
            'white', 'cream', 'beige', 'brown', 'red', 'yellow',
            'orange', 'pink', 'blue', 'green', 'grey', 'gray',
            'black', 'gold', 'silver', 'sandstone', 'terracotta'
        ]
        
        for color in color_keywords:
            if color in text:
                colors.append(color)
        
        return colors if colors else ['white', 'cream']
    
    def _extract_budget(self, text: str) -> Optional[str]:
        """Extract budget if mentioned"""
        budget_patterns = [
            r'(?:rs\.?|₹|inr)\s*(\d+)\s*(?:lakh|lac|l)',
            r'(\d+)\s*(?:lakh|lac)\s*(?:rs\.?|₹|rupees)',
            r'budget\s*(?:of\s*)?(?:rs\.?|₹)?\s*(\d+)'
        ]
        
        for pattern in budget_patterns:
            match = re.search(pattern, text)
            if match:
                return f"{match.group(1)} lakhs"
        
        return None
    
    def _extract_orientation(self, text: str) -> Optional[str]:
        """Extract house orientation/direction"""
        orientations = {
            'north': ['north facing', 'north direction'],
            'south': ['south facing', 'south direction'],
            'east': ['east facing', 'east direction'],
            'west': ['west facing', 'west direction']
        }
        
        for orientation, keywords in orientations.items():
            if any(kw in text for kw in keywords):
                return orientation
        
        return None