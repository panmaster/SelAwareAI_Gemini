import numpy as np
from typing import Dict, List, Tuple
import random
import asyncio


class Emotion:
    def __init__(self, name: str, intensity: float = 0.0):
        self.name = name
        self.intensity = max(0.0, min(1.0, intensity))


class EmotionalState:
    def __init__(self):
        self.emotions: Dict[str, Emotion] = {
            "joy": Emotion("joy"),
            "sadness": Emotion("sadness"),
            "anger": Emotion("anger"),
            "fear": Emotion("fear"),
            "surprise": Emotion("surprise"),
            "disgust": Emotion("disgust"),
            "trust": Emotion("trust"),
            "anticipation": Emotion("anticipation")
        }

    def update(self, emotion_name: str, intensity_change: float):
        if emotion_name in self.emotions:
            self.emotions[emotion_name].intensity = max(0.0, min(1.0, self.emotions[
                emotion_name].intensity + intensity_change))

    def get_dominant_emotion(self) -> Tuple[str, float]:
        return max(self.emotions.items(), key=lambda x: x[1].intensity)


class EmotionalCognition:
    def __init__(self, learning_module, strategic_cognition):
        self.learning_module = learning_module
        self.strategic_cognition = strategic_cognition
        self.emotional_state = EmotionalState()
        self.emotion_memory: List[Dict] = []
        self.emotion_decay_rate = 0.1

    async def process_emotion(self, stimulus: str):
        # Simple emotion processing based on keyword matching
        emotion_keywords = {
            "joy": ["happy", "great", "excellent", "wonderful"],
            "sadness": ["sad", "unhappy", "disappointed", "depressed"],
            "anger": ["angry", "furious", "annoyed", "irritated"],
            "fear": ["scared", "afraid", "terrified", "anxious"],
            "surprise": ["surprised", "amazed", "astonished", "shocked"],
            "disgust": ["disgusted", "revolted", "repulsed"],
            "trust": ["trust", "believe", "confident", "reliable"],
            "anticipation": ["excited", "eager", "looking forward"]
        }

        for emotion, keywords in emotion_keywords.items():
            if any(keyword in stimulus.lower() for keyword in keywords):
                intensity_change = random.uniform(0.1, 0.3)
                self.emotional_state.update(emotion, intensity_change)
                await self.learning_module.learn_concept(f"Emotion: {emotion}", f"Triggered by: {stimulus}")

        dominant_emotion, intensity = self.emotional_state.get_dominant_emotion()
        self.emotion_memory.append({"stimulus": stimulus, "emotion": dominant_emotion, "intensity": intensity})

    async def decay_emotions(self):
        for emotion in self.emotional_state.emotions.values():            emotion.intensity = max(0.0,
                                                                                                  emotion.intensity - self.emotion_decay_rate)

    def get_emotional_bias(self) -> float:
        # Simplified emotional bias calculation
        positive_emotions = ["joy", "trust", "anticipation"]
        negative_emotions = ["sadness", "anger", "fear", "disgust"]
        positive_intensity = sum(self.emotional_state.emotions[e].intensity for e in positive_emotions)
        negative_intensity = sum(self.emotional_state.emotions[e].intensity for e in negative_emotions)

        return (positive_intensity - negative_intensity) / len(self.emotional_state.emotions)

    async def emotionally_biased_decision(self, context: str) -> Dict:
        base_decision = await self.strategic_cognition.make_decision(context)
        emotional_bias = self.get_emotional_bias()
        # Adjust the estimated impact based on emotional bias
        adjusted_impact = base_decision.estimated_impact * (1 + emotional_bias)

        return {
            "action": base_decision.description,
            "original_impact": base_decision.estimated_impact, "emotionally_adjusted_impact": adjusted_impact,
            "emotional_bias": emotional_bias
        }

    async def generate_emotional_insight(self) -> str:
        dominant_emotion, intensity = self.emotional_state.get_dominant_emotion()
        recent_memories = self.emotion_memory[-5:]  # Get last 5 emotional memories

        insight = f"I am currently feeling {dominant_emotion} with an intensity of {intensity:.2f}. "
        insight += "Recent experiences have made me feel "
        insight += ", ".join(
            f"{mem['emoti        insight += f". This is affecting my decision-making with a bias of {self.get_emotional_bias():.2f}."

        return insight

    async def run_emotional_cycle(self):
        while

    True:
    await self.decay_emotions()
    await asyncio.sleep(5)  # Decay emotions every 5 seconds


# Example usage and integration
async def integrate_emotional_cognition(adaptive_consciousness, learning_module, strategic_cognition):
    emotional_cognition = EmotionalCognition(learning_module, strategic_cognition)
    adaptive_consciousness.emotional_cognition = emotional_cognition

    # Add methods to AdaptiveConsciousness
    adaptive_consciousness.process_emotion = emotional_cognition.process_emotion
    adaptive_consciousness.emotionally_biased_decision = emotional_cognition.emotionally_biased_decision
    adaptive_consciousness.generate_emotional_insight = emotional_cognition.generate_emotional_insight

    # Run the emotional cycle in the background
    asyncio.create_task(emotional_cognition.run_emotional_cycle())


if __name__ == "__main__":
    # This is a simplified example. In practice, you'd integrate this with the full AdaptiveConsciousness
    from advanced_learning_module import AdvancedLearningModule
    from strategic_cognition import StrategicCognition


    async def main():
        learning_module = AdvancedLearningModule()
        strategic_cognition = StrategicCognition(learning_module)
        emotional_cognition = EmotionalCognition(learning_module, strategic_cognition)

        # Simulate some interactions
        stimuli = [
            "I'm so happy with the progress we're making!",
            "This setback is really disappointing.",
            "I'm excited about the potential of this new idea!",
            "The complexity of this problem is making me anxious."
        ]

        for stimulus in stimuli:
            await emotional_cognition.process_emotion(stimulus)
            decision = await emotional_cognition.emotionally_biased_decision("How to proceed with the project")
            insight = await emotional_cognition.generate_emotional_insight()

            print(f"Stimulus: {stimulus}")
            print(f"Decision: {decision}")
            print(f"Emotional Insight: {insight}")
            print("---")

            await asyncio.sleep(2)


    asyncio.run(main())