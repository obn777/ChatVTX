class SyntacticRestorer:
    def __init__(self):
        self.module_name = "Синтаксический корректор"

    def preprocess_voice_flow(self, text: str) -> str:
        # Если в длинном тексте нет знаков препинания — это 100% голос
        if len(text.split()) > 5 and not any(char in text for char in ".,!?"):
            return f"[VOICE_FLOW_DETECTED]: {text} [/VOICE_FLOW]"
        return text

    def get_instruction(self) -> str:
        return (
            "\n[ВНИМАНИЕ — ГОЛОСОВОЙ ВВОД]: Георгий говорит через микрофон, знаки препинания отсутствуют. "
            "Твоя задача: ПЕРЕД ответом мысленно расставь запятые и точки, чтобы не исказить смысл "
            "(помни про 'казнить нельзя помиловать'). Отвечай так, будто текст был идеально структурирован."
        )
