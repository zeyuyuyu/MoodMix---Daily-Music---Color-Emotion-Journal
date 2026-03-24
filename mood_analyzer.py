from textblob import TextBlob
import colorsys

class MoodAnalyzer:
    def __init__(self):
        self.mood_colors = {
            'joy': '#FFD700',      # Gold
            'sadness': '#4682B4',  # Steel Blue
            'anger': '#DC143C',    # Crimson
            'fear': '#800080',     # Purple
            'neutral': '#A9A9A9',  # Dark Gray
            'excitement': '#FF4500' # Orange Red
        }

    def analyze_mood(self, text):
        """Analyze text and return mood classification with confidence score"""
        analysis = TextBlob(text)
        
        # Get polarity (-1 to 1) and subjectivity (0 to 1)
        polarity = analysis.sentiment.polarity
        subjectivity = analysis.sentiment.subjectivity
        
        # Determine base mood
        if polarity > 0.5:
            mood = 'joy' if subjectivity < 0.5 else 'excitement'
        elif polarity < -0.5:
            mood = 'sadness' if subjectivity < 0.5 else 'anger'
        elif polarity < -0.2:
            mood = 'fear'
        else:
            mood = 'neutral'
            
        return {
            'mood': mood,
            'color': self.mood_colors[mood],
            'confidence': abs(polarity) * 100,
            'intensity': subjectivity * 100
        }

    def generate_color_gradient(self, mood1, mood2, steps=5):
        """Generate a gradient between two mood colors"""
        color1 = self.mood_colors[mood1].lstrip('#')
        color2 = self.mood_colors[mood2].lstrip('#')
        
        # Convert hex to RGB
        rgb1 = tuple(int(color1[i:i+2], 16) for i in (0, 2, 4))
        rgb2 = tuple(int(color2[i:i+2], 16) for i in (0, 2, 4))
        
        # Convert RGB to HSV
        hsv1 = colorsys.rgb_to_hsv(*[x/255.0 for x in rgb1])
        hsv2 = colorsys.rgb_to_hsv(*[x/255.0 for x in rgb2])
        
        # Generate gradient
        gradient = []
        for i in range(steps):
            ratio = i / float(steps-1)
            hsv = tuple(h1 + ratio * (h2 - h1) for h1, h2 in zip(hsv1, hsv2))
            rgb = colorsys.hsv_to_rgb(*hsv)
            hex_color = '#{:02x}{:02x}{:02x}'.format(
                int(rgb[0] * 255),
                int(rgb[1] * 255),
                int(rgb[2] * 255)
            )
            gradient.append(hex_color)
            
        return gradient

    def get_musical_suggestion(self, mood):
        """Suggest musical characteristics based on mood"""
        suggestions = {
            'joy': {
                'tempo': 'upbeat (120-140 BPM)',
                'key': 'major',
                'genres': ['Pop', 'Dance', 'Happy Folk']
            },
            'sadness': {
                'tempo': 'slow (60-80 BPM)',
                'key': 'minor',
                'genres': ['Blues', 'Slow Jazz', 'Classical']
            },
            'anger': {
                'tempo': 'fast (140+ BPM)',
                'key': 'minor',
                'genres': ['Rock', 'Metal', 'Intense Electronic']
            },
            'fear': {
                'tempo': 'varied',
                'key': 'diminished/atonal',
                'genres': ['Ambient', 'Dark Electronic', 'Experimental']
            },
            'neutral': {
                'tempo': 'moderate (90-120 BPM)',
                'key': 'mixed',
                'genres': ['Indie', 'Alternative', 'Instrumental']
            },
            'excitement': {
                'tempo': 'energetic (130+ BPM)',
                'key': 'major',
                'genres': ['EDM', 'House', 'Uplifting Rock']
            }
        }
        return suggestions.get(mood, suggestions['neutral'])
