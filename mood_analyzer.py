import os
import librosa
import numpy as np
from transformers import pipeline

class MoodAnalyzer:
    def __init__(self, audio_dir):
        self.audio_dir = audio_dir
        self.sentiment_analyzer = pipeline('sentiment-analysis')

    def analyze_mood(self):
        moods = []
        for filename in os.listdir(self.audio_dir):
            if filename.endswith('.wav'):
                audio_path = os.path.join(self.audio_dir, filename)
                mood = self.analyze_audio(audio_path)
                moods.append(mood)
        return moods

    def analyze_audio(self, audio_path):
        audio, sr = librosa.load(audio_path, sr=16000)
        mfcc = librosa.feature.mfcc(y=audio, sr=sr)
        mfcc_mean = np.mean(mfcc, axis=1)
        sentiment = self.sentiment_analyzer(mfcc_mean.tolist())[0]
        return sentiment['label']
