"""
Enhanced Text Parser with Deep Learning Features
Uses NLP and ML for better understanding of house descriptions
"""

import re
import json
import numpy as np
from typing import Dict, List, Tuple, Any
import nltk
from collections import defaultdict
import spacy

# Download required NLTK data (run once)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class IntelligentTextParser:
    """Advanced text parser with NLP capabilities"""
    
    def __init__(self):
        # Load spacy model (install with: python -m spacy download en_core_web_sm)
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Installing spacy model...")
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")
        
        # Enhanced architectural knowledge base
        self.styles_keywords = {
            'traditional': {
                'keywords': ['traditional', 'classic', 'heritage', 'old', 'vintage', 'ancestral', 'joint family'],
                'features': ['courtyard', 'thick walls', 'wooden pillars', 'traditional roof'],
                'materials': ['brick', 'stone', 'wood', 'mud'],
                'colors': ['earth tones', 'terracotta', 'ochre']
            },
            'modern': {
                'keywords': ['modern', 'contemporary', 'sleek', 'minimalist', 'urban', 'new'],
                'features': ['large windows', 'open plan', 'flat roof', 'glass walls'],
                'materials': ['glass', 'steel', 'concrete'],
                'colors': ['white', 'grey', 'black']
            },
            'kerala': {
                'keywords': ['kerala', 'malayali', 'backwater', 'coconut', 'monsoon', 'tropical'],
                'features': ['sloped roof', 'wooden balcony', 'carved pillars', 'open courtyard'],
                'materials': ['wood', 'tile', 'bamboo'],
                'colors': ['brown', 'green', 'cream']
            },
            'rajasthani': {
                'keywords': ['rajasthani', 'desert', 'palace', 'haveli', 'jharokha', 'royal'],
                'features': ['carved windows', 'dome', 'courtyard', 'jharokha'],
                'materials': ['sandstone', 'marble', 'stone'],
                'colors': ['yellow', 'red', 'pink', 'white']
            },
            'bengali': {
                'keywords': ['bengali', 'kolkata', 'cultural', 'artistic', 'poet'],
                'features': ['curved roof', 'artistic designs', 'cultural elements'],
                'materials': ['brick', 'terracotta', 'wood'],
                'colors': ['red', 'yellow', 'white']
            },
            'punjabi': {
                'keywords': ['punjabi', 'farmhouse', 'agricultural', 'sikh', 'rural'],
                'features': ['farmhouse style', 'large doors', 'simple design'],
                'materials': ['brick', 'concrete'],
                'colors': ['white', 'cream', 'blue']
            },
            'south_indian': {
                'keywords': ['south indian', 'tamil', 'temple', 'dravidian', 'chennai'],
                'features': ['temple style', 'pillars', 'carved details'],
                'materials': ['stone', 'granite', 'wood'],
                'colors': ['grey', 'brown', 'white']
            },
            'colonial': {
                'keywords': ['colonial', 'british', 'european', 'vintage', 'bungalow'],
                'features': ['high ceiling', 'large windows', 'verandah'],
                'materials': ['brick', 'wood'],
                'colors': ['white', 'cream', 'brown']
            }
        }
        
        self.house_types = {
            'villa': {
                'keywords': ['villa', 'luxury', 'premium', 'grand', 'mansion'],
                'typical_floors': [2, 3, 4],
                'typical_rooms': ['master bedroom', 'guest room', 'study', 'gym', 'library'],
                'features': ['swimming pool', 'garden', 'garage', 'balcony']
            },
            'bungalow': {
                'keywords': ['bungalow', 'single floor', 'ground floor', 'one story'],
                'typical_floors': [1],
                'typical_rooms': ['bedroom', 'living room', 'kitchen'],
                'features': ['garden', 'porch']
            },
            'apartment': {
                'keywords': ['apartment', 'flat', 'unit', 'condo'],
                'typical_floors': [1, 2],
                'typical_rooms': ['bedroom', 'living room', 'kitchen'],
                'features': ['balcony', 'parking']
            },
            'cottage': {
                'keywords': ['cottage', 'small', 'cozy', 'simple', 'tiny'],
                'typical_floors': [1, 2],
                'typical_rooms': ['bedroom', 'kitchen', 'living room'],
                'features': ['garden', 'chimney']
            },
            'farmhouse': {
                'keywords': ['farmhouse', 'rural', 'countryside', 'agricultural'],
                'typical_floors': [1, 2],
                'typical_rooms': ['bedroom', 'kitchen', 'storage'],
                'features': ['large yard', 'barn', 'garden']
            },
            'townhouse': {
                'keywords': ['townhouse', 'row house', 'terrace'],
                'typical_floors': [2, 3],
                'typical_rooms': ['bedroom', 'living room', 'kitchen'],
                'features': ['small garden', 'garage']
            },
            'mansion': {
                'keywords': ['mansion', 'palace', 'huge', 'massive', 'royal'],
                'typical_floors': [3, 4, 5],
                'typical_rooms': ['multiple bedrooms', 'ballroom', 'library', 'study'],
                'features': ['swimming pool', 'large garden', 'multiple garages']
            },
            'duplex': {
                'keywords': ['duplex', 'two family', 'double'],
                'typical_floors': [2],
                'typical_rooms': ['multiple bedrooms', 'two kitchens'],
                'features': ['separate entrances', 'balcony']
            },
            'penthouse': {
                'keywords': ['penthouse', 'top floor', 'luxury apartment'],
                'typical_floors': [1, 2],
                'typical_rooms': ['master suite', 'entertainment room'],
                'features': ['terrace', 'city view', 'premium finishes']
            }
        }
        
        # Room detection with context
        self.rooms = {
            'bedroom': ['bedroom', 'master bedroom', 'guest room', 'bed room', 'sleeping room'],
            'kitchen': ['kitchen', 'cooking area', 'pantry', 'kitchenette'],
            'living_room': ['living room', 'hall', 'sitting room', 'lounge', 'drawing room'],
            'bathroom': ['bathroom', 'toilet', 'washroom', 'bath', 'powder room'],
            'dining_room': ['dining room', 'dining area', 'eating area'],
            'study': ['study', 'office', 'home office', 'work room', 'library'],
            'garage': ['garage', 'parking', 'car park'],
            'storage': ['storage', 'store room', 'utility room', 'pantry'],
            'balcony': ['balcony', 'terrace', 'deck', 'veranda'],
            'garden': ['garden', 'yard', 'lawn', 'landscape'],
            'gym': ['gym', 'fitness room', 'exercise room'],
            'guest_room': ['guest room', 'guest bedroom', 'visitor room'],
            'kids_room': ['kids room', 'children room', 'nursery', 'child bedroom'],
            'entertainment': ['entertainment room', 'media room', 'game room', 'recreation room']
        }
        
        # Feature detection
        self.features = {
            'swimming_pool': ['swimming pool', 'pool', 'swimming', 'water feature'],
            'garden': ['garden', 'lawn', 'landscaping', 'greenery', 'plants'],
            'balcony': ['balcony', 'terrace', 'deck', 'veranda'],
            'garage': ['garage', 'parking', 'car port'],
            'fireplace': ['fireplace', 'chimney', 'hearth'],
            'security': ['security', 'gated', 'protected', 'safe'],
            'solar_panels': ['solar', 'renewable energy', 'green energy'],
            'elevator': ['elevator', 'lift'],
            'basement': ['basement', 'cellar', 'underground'],
            'attic': ['attic', 'loft', 'top floor storage']
        }
        
        # Color detection with variations
        self.colors = {
            'red': ['red', 'crimson', 'scarlet', 'brick red', 'maroon'],
            'blue': ['blue', 'navy', 'azure', 'sky blue', 'royal blue'],
            'green': ['green', 'emerald', 'forest green', 'olive'],
            'yellow': ['yellow', 'golden', 'amber', 'cream'],
            'white': ['white', 'ivory', 'pearl', 'off-white'],
            'brown': ['brown', 'chocolate', 'coffee', 'mahogany', 'wooden'],
            'orange': ['orange', 'tangerine', 'peach', 'coral'],
            'pink': ['pink', 'rose', 'blush', 'salmon'],
            'purple': ['purple', 'violet', 'lavender', 'plum'],
            'grey': ['grey', 'gray', 'silver', 'charcoal'],
            'black': ['black', 'ebony', 'jet black'],
            'beige': ['beige', 'tan', 'sand', 'neutral']
        }
        
        # Material detection
        self.materials = {
            'brick': ['brick', 'bricks', 'brick work'],
            'wood': ['wood', 'wooden', 'timber', 'lumber'],
            'concrete': ['concrete', 'cement', 'reinforced'],
            'stone': ['stone', 'natural stone', 'rock'],
            'glass': ['glass', 'glazed', 'transparent'],
            'metal': ['metal', 'steel', 'iron', 'aluminum'],
            'marble': ['marble', 'polished stone'],
            'granite': ['granite', 'hard stone'],
            'bamboo': ['bamboo', 'eco-friendly'],
            'tile': ['tile', 'tiled', 'ceramic']
        }
        
        # Number extraction patterns
        self.number_patterns = {
            'floors': [
                r'(\d+)\s*(?:floor|story|storey|level)',
                r'(?:floor|story|storey|level)\s*(\d+)',
                r'(\d+)\s*(?:floor|story|storey|level)s?'
            ],
            'rooms': [
                r'(\d+)\s*(?:room|bedroom|bed room)',
                r'(\d+)\s*(?:bhk|BHK)',
                r'(\d+)(?:bed|bedroom)'
            ],
            'bathrooms': [
                r'(\d+)\s*(?:bathroom|bath|toilet)',
                r'(\d+)\s*bath'
            ]
        }
    
    def extract_numbers_with_context(self, text: str) -> Dict[str, int]:
        """Extract numbers with context using NLP"""
        doc = self.nlp(text.lower())
        numbers = {}
        
        # Extract floors
        for pattern in self.number_patterns['floors']:
            matches = re.findall(pattern, text.lower())
            if matches:
                numbers['floors'] = int(matches[0])
                break
        
        # Extract rooms
        for pattern in self.number_patterns['rooms']:
            matches = re.findall(pattern, text.lower())
            if matches:
                numbers['bedrooms'] = int(matches[0])
                break
        
        # Extract bathrooms
        for pattern in self.number_patterns['bathrooms']:
            matches = re.findall(pattern, text.lower())
            if matches:
                numbers['bathrooms'] = int(matches[0])
                break
        
        # Use spacy to find numbers and their context
        for token in doc:
            if token.like_num:
                # Look at surrounding words for context
                context_window = 3
                start = max(0, token.i - context_window)
                end = min(len(doc), token.i + context_window + 1)
                context = doc[start:end].text.lower()
                
                if any(word in context for word in ['floor', 'story', 'storey', 'level']):
                    numbers['floors'] = int(token.text)
                elif any(word in context for word in ['room', 'bedroom', 'bhk']):
                    numbers['rooms'] = int(token.text)
                elif any(word in context for word in ['bathroom', 'bath', 'toilet']):
                    numbers['bathrooms'] = int(token.text)
        
        return numbers
    
    def detect_architectural_style(self, text: str) -> Tuple[str, float]:
        """Detect architectural style with confidence score"""
        text_lower = text.lower()
        doc = self.nlp(text_lower)
        
        style_scores = defaultdict(float)
        
        for style, data in self.styles_keywords.items():
            score = 0
            
            # Direct keyword matching
            for keyword in data['keywords']:
                if keyword in text_lower:
                    score += 2.0
            
            # Feature matching
            for feature in data['features']:
                if feature in text_lower:
                    score += 1.5
            
            # Material matching
            for material in data['materials']:
                if material in text_lower:
                    score += 1.0
            
            # Color matching
            for color in data['colors']:
                if color in text_lower:
                    score += 0.5
            
            # Semantic similarity using spacy
            for keyword in data['keywords']:
                keyword_doc = self.nlp(keyword)
                similarity = doc.similarity(keyword_doc)
                score += similarity * 1.0
            
            style_scores[style] = score
        
        if not style_scores:
            return 'modern', 0.5  # default
        
        best_style = max(style_scores.items(), key=lambda x: x[1])
        
        # Normalize confidence
        max_possible_score = len(self.styles_keywords[best_style[0]]['keywords']) * 2.0
        confidence = min(1.0, best_style[1] / max_possible_score)
        
        return best_style[0], confidence
    
    def detect_house_type(self, text: str) -> Tuple[str, float]:
        """Detect house type with confidence"""
        text_lower = text.lower()
        doc = self.nlp(text_lower)
        
        type_scores = defaultdict(float)
        
        for house_type, data in self.house_types.items():
            score = 0
            
            # Direct keyword matching
            for keyword in data['keywords']:
                if keyword in text_lower:
                    score += 3.0
            
            # Room matching
            for room in data['typical_rooms']:
                if room in text_lower:
                    score += 1.0
            
            # Feature matching
            for feature in data['features']:
                if feature in text_lower:
                    score += 1.5
            
            # Semantic similarity
            for keyword in data['keywords']:
                keyword_doc = self.nlp(keyword)
                similarity = doc.similarity(keyword_doc)
                score += similarity * 2.0
            
            type_scores[house_type] = score
        
        if not type_scores:
            return 'house', 0.5  # default
        
        best_type = max(type_scores.items(), key=lambda x: x[1])
        
        # Normalize confidence
        max_possible_score = len(self.house_types[best_type[0]]['keywords']) * 3.0
        confidence = min(1.0, best_type[1] / max_possible_score)
        
        return best_type[0], confidence
    
    def extract_detailed_attributes(self, text: str) -> Dict[str, Any]:
        """Extract comprehensive attributes from text using advanced NLP"""
        
        # Basic processing
        doc = self.nlp(text.lower())
        attributes = {}
        
        # Detect style and type
        style, style_confidence = self.detect_architectural_style(text)
        house_type, type_confidence = self.detect_house_type(text)
        
        attributes['style'] = style
        attributes['house_type'] = house_type
        attributes['confidence_scores'] = {
            'style': style_confidence,
            'type': type_confidence
        }
        
        # Extract numbers with context
        numbers = self.extract_numbers_with_context(text)
        attributes.update(numbers)
        
        # Set defaults based on house type
        if house_type in self.house_types:
            type_data = self.house_types[house_type]
            if 'floors' not in attributes:
                attributes['floors'] = type_data['typical_floors'][0]
        
        # Extract rooms
        detected_rooms = []
        for room_type, keywords in self.rooms.items():
            for keyword in keywords:
                if keyword in text.lower():
                    detected_rooms.append(room_type)
                    break
        
        # Add typical rooms if none detected
        if not detected_rooms and house_type in self.house_types:
            detected_rooms = self.house_types[house_type]['typical_rooms'][:3]
        
        attributes['rooms'] = list(set(detected_rooms))
        
        # Extract features
        detected_features = []
        for feature_type, keywords in self.features.items():
            for keyword in keywords:
                if keyword in text.lower():
                    detected_features.append(feature_type)
                    break
        
        attributes['features'] = detected_features
        
        # Extract colors
        detected_colors = []
        for color_name, keywords in self.colors.items():
            for keyword in keywords:
                if keyword in text.lower():
                    detected_colors.append(color_name)
                    break
        
        if not detected_colors:
            # Default based on style
            style_data = self.styles_keywords.get(style, {})
            default_colors = style_data.get('colors', ['white'])
            detected_colors = [default_colors[0]]
        
        attributes['colors'] = detected_colors
        
        # Extract materials
        detected_materials = []
        for material_name, keywords in self.materials.items():
            for keyword in keywords:
                if keyword in text.lower():
                    detected_materials.append(material_name)
                    break
        
        if not detected_materials:
            # Default based on style
            style_data = self.styles_keywords.get(style, {})
            default_materials = style_data.get('materials', ['brick'])
            detected_materials = [default_materials[0]]
        
        attributes['materials'] = detected_materials
        
        # Estimate dimensions based on type and floors
        base_dimensions = {
            'villa': {'width': 15, 'depth': 12, 'height': 12},
            'mansion': {'width': 20, 'depth': 18, 'height': 15},
            'bungalow': {'width': 12, 'depth': 10, 'height': 4},
            'cottage': {'width': 8, 'depth': 8, 'height': 6},
            'apartment': {'width': 10, 'depth': 8, 'height': 8},
            'farmhouse': {'width': 14, 'depth': 12, 'height': 8},
            'townhouse': {'width': 8, 'depth': 12, 'height': 8},
            'duplex': {'width': 12, 'depth': 10, 'height': 8},
            'penthouse': {'width': 12, 'depth': 12, 'height': 6}
        }
        
        dims = base_dimensions.get(house_type, {'width': 10, 'depth': 8, 'height': 8})
        floors = attributes.get('floors', 1)
        dims['height'] = dims['height'] * floors / 2  # Adjust height for floors
        
        attributes['dimensions'] = dims
        
        # Add sentiment analysis for quality indicators
        sentiment_keywords = {
            'luxury': ['luxury', 'premium', 'high-end', 'expensive', 'grand'],
            'simple': ['simple', 'basic', 'modest', 'small', 'tiny'],
            'modern': ['modern', 'contemporary', 'new', 'advanced'],
            'traditional': ['traditional', 'classic', 'old', 'heritage']
        }
        
        attributes['quality_indicators'] = []
        for indicator, keywords in sentiment_keywords.items():
            if any(keyword in text.lower() for keyword in keywords):
                attributes['quality_indicators'].append(indicator)
        
        return attributes