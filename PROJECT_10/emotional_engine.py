import json
from typing import Dict, Any
import asyncio

class EmotionalEngine:
    def __init__(self):
        self.current_emotion = "neutral"
        self.emotion_intensity = 0.5
        self.emotion_history = []

    async def update(self, input_text: str, output_text: str):
        # Simple keyword-based emotion detection
        emotions = {
            "joy": ["happy", "excited", "delighted"],
            "sadness": ["sad", "depressed", "unhappy"],
            "anger": ["angry", "furious", "irritated"],
            "fear": ["scared", "afraid", "terrified"],
            "surprise        }

        detected_emotions = []
        for emotion, keywords in emotions.items():
            if any(keyword in input_text.lower() or keyword in output_text.lower() for keyword in keywords):
                detected_emotions.append(emotion)

        if detected_emotions:
            self.current_emotion = detected_emotions[0]  # Just use the first detected emotion for simplicity
            self.emotion_intensity = 0.8
        else:
            self.current_emotion = "neutral"
            self.emotion_intensity = 0.5

        self.emotion_history.append({
            "emotion": self.current            "intensity": self.emotion_intensity,
            "input": input_text,
            "output": output_text
        })

    async def get_emotional        return {
            "current_emotion": self.current_emotion,
            "intensity": self.emotion_intensity
        }

    async def save_emotional_state(self):
        with open("brain_settings/emotional_state.json", "w") as f:
            json.dump({                "current_emotion": self.current_emotion,
                "intensity": self.emotion_intensity,
                "history": self.emotion_history[-10:]  # Save last 10 emotional states
            }, f)

    async def load_emotional_state(self):
        try:
            with open("brain_settings/emotional_state.json", "r") as f:
                data = json.load(f)
                self.current_emotion = data["current_emotion"]
                self.emotion_intensity = data["intensity"]
                self.emotion_history = data["history"]
        except FileNotFoundError:
            pass  # No previous emotional state found,