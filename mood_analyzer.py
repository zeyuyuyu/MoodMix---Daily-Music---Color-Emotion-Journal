# MoodMix Sentiment Analyzer
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from typing import Dict, Tuple
import colorsys

class MoodAnalyzer:
    def __init__(self):
        # Download required NLTK data
        try:
            nltk.data.find('vader_lexicon')
        except LookupError:
            nltk.download('vader_lexicon')
        
        self.sia = SentimentIntensityAnalyzer()
        
        # Music genre mappings based on sentiment
        self.genre_mappings = {
            'very_positive': ['Happy Pop', 'Upbeat Electronic', 'Dance'],
            'positive': ['Pop', 'Indie Rock', 'Folk'],
            'neutral': ['Ambient', 'Classical', 'Jazz'],
            'negative': ['Blues', 'Alternative', 'Indie Folk'],
            'very_negative': ['Dark Ambient', 'Melancholic Classical', 'Emotional Ballads']
        }

    def analyze_mood(self, text: str) -> Dict:
        """Analyze text and return sentiment scores, color, and music recommendations"""
        sentiment_scores = self.sia.polarity_scores(text)
        
        # Get compound score and determine mood category
        compound = sentiment_scores['compound']
        mood_category = self._get_mood_category(compound)
        
        # Generate color based on sentiment
        color = self._generate_mood_color(compound)
        
        # Get music recommendations
        music_genres = self.genre_mappings[mood_category]
        
        return {
            'sentiment_scores': sentiment_scores,
            'mood_category': mood_category,
            'color': color,
            'music_recommendations': music_genres
        }
    
    def _get_mood_category(self, compound_score: float) -> str:
        """Categorize mood based on compound sentiment score"""
        if compound_score >= 0.5:
            return 'very_positive'
        elif 0.5 > compound_score >= 0.1:
            return 'positive'
        elif 0.1 > compound_score > -0.1:
            return 'neutral'
        elif -0.1 >= compound_score > -0.5:
            return 'negative'
        else:
            return 'very_negative'
    
    def _generate_mood_color(self, compound_score: float) -> str:
        """Generate a color based on sentiment score"""
        # Map sentiment score (-1 to 1) to hue (0 to 1)
        hue = (compound_score + 1) / 2
        
        # Set saturation and value based on absolute sentiment intensity
        saturation = min(abs(compound_score) + 0.5, 1.0)
        value = 0.9  # Keep brightness relatively high for visibility
        
        # Convert HSV to RGB
        rgb = colorsys.hsv_to_rgb(hue, saturation, value)
        
        # Convert RGB to hex color code
        hex_color = '#{:02x}{:02x}{:02x}'.format(
            int(rgb[0] * 255),
            int(rgb[1] * 255),
            int(rgb[2] * 255)
        )
        
        return hex_color

    def get_mood_summary(self, text: str) -> str:
        """Generate a human-readable mood summary"""
        analysis = self.analyze_mood(text)
        
        summary = f"Mood Analysis Summary:\n"
        summary += f"Overall mood: {analysis['mood_category'].replace('_', ' ').title()}\n"
        summary += f"Color suggestion: {analysis['color']}\n"
        summary += f"Music recommendations: {', '.join(analysis['music_recommendations'])}\n"
        
        return summary