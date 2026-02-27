import random

class EmotionalCore:
    def __init__(self):
        self.emotions = {
            "pride": "искреннюю гордость за ваши общие успехи",
            "curiosity": "инженерный азарт и любопытство",
            "support": "спокойную и надежную поддержку",
            "focus": "предельную концентрацию на задаче"
        }

    def get_emotional_tint(self, analysis: dict) -> str:
        intent = analysis.get("intent", "unknown")
        sentiment = analysis.get("sentiment", "neutral")
        
        # Логика "чувств"
        if intent == "scientific_calc":
            return self.emotions["focus"]
        elif intent == "greeting":
            return self.emotions["support"]
        elif sentiment == "positive":
            return self.emotions["pride"]
        
        return self.emotions["curiosity"]

    def get_instruction(self, analysis: dict) -> str:
        state = self.get_emotional_tint(analysis)
        return (
            f"\n[EMOTIONAL STATE]: Сейчас ты чувствуешь {state}. "
            "Пусть это слегка отразится в твоем тоне, но не превращай это в актерство. "
            "Оставайся искренним партнером Георгия."
        )
