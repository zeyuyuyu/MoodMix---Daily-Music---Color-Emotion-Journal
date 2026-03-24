import numpy as np
from textblob import TextBlob
import colorsys

class MoodAnalyzer:
    def __init__(self):
        self.mood_colors = {
            'joy': '#FFD700',      # Gold
            'sadness': '#4682B4',  # Steel Blue  
            'anger': '#DC143C',    # Crimson
            'fear': '#800080',     # Purple
            'neutral': '#808080',  # Gray
            'excitement': '#FF4500' # Orange Red
        }
        
        self.mood_weights = {
            'joy': [0.8, 0.7, 0.1],
            'sadness': [0.2, 0.3, 0.7], 
            'anger': [0.9, 0.2, 0.2],
            'fear': [0.5, 0.2, 0.5],
            'neutral': [0.5, 0.5, 0.5],
            'excitement': [0.9, 0.4, 0.1]
        }

    def analyze_mood(self, text):
        """Analyze text and return mood classification with confidence scores"""
        analysis = TextBlob(text)
        
        # Get polarity (-1 to 1) and subjectivity (0 to 1)
        polarity = analysis.sentiment.polarity
        subjectivity = analysis.sentiment.subjectivity
        
        # Determine base mood
        if polarity > 0.3:
            if subjectivity > 0.7:
                mood = 'excitement'
            else:
                mood = 'joy'
        elif polarity < -0.3:
            if subjectivity > 0.7:
                mood = 'anger'
            else:
                mood = 'sadness'
        elif -0.3 <= polarity <= 0.3:
            if subjectivity > 0.7:
                mood = 'fear'
            else:
                mood = 'neutral'
                
        return {
            'mood': mood,
            'polarity': polarity,
            'subjectivity': subjectivity
        }

    def get_mood_color(self, mood_result):
        """Generate color based on mood analysis"""
        base_color = self.mood_colors[mood_result['mood']]
        weights = self.mood_weights[mood_result['mood']]
        
        # Adjust color based on polarity and subjectivity
        rgb = self._hex_to_rgb(base_color)
        hsv = colorsys.rgb_to_hsv(rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0)
        
        # Modify HSV values based on sentiment
        h = hsv[0] + (mood_result['polarity'] * 0.1)  # Shift hue slightly
        s = min(1.0, hsv[1] + (mood_result['subjectivity'] * 0.2))  # Increase saturation with subjectivity
        v = min(1.0, hsv[2] * (1.0 + mood_result['polarity'] * 0.3))  # Adjust brightness with polarity
        
        # Convert back to RGB
        rgb_modified = colorsys.hsv_to_rgb(h, s, v)
        return self._rgb_to_hex(
            int(rgb_modified[0] * 255),
            int(rgb_modified[1] * 255),
            int(rgb_modified[2] * 255)
        )

    def _hex_to_rgb(self, hex_color):
        """Convert hex color to RGB values"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def _rgb_to_hex(self, r, g, b):
        """Convert RGB values to hex color"""
        return '#{:02x}{:02x}{:02x}'.format(r, g, b)

    def generate_color_palette(self, mood_result, num_colors=5):
        """Generate a harmonious color palette based on mood"""
        base_color = self.get_mood_color(mood_result)
        base_rgb = self._hex_to_rgb(base_color)
        base_hsv = colorsys.rgb_to_hsv(base_rgb[0]/255.0, base_rgb[1]/255.0, base_rgb[2]/255.0)
        
        palette = [base_color]
        golden_ratio = 0.618033988749895
        
        for i in range(num_colors - 1):
            h = (base_hsv[0] + golden_ratio * (i + 1)) % 1.0
            s = base_hsv[1]
            v = base_hsv[2]
            
            rgb = colorsys.hsv_to_rgb(h, s, v)
            color = self._rgb_to_hex(
                int(rgb[0] * 255),
                int(rgb[1] * 255),
                int(rgb[2] * 255)
            )
            palette.append(color)
            
        return palette