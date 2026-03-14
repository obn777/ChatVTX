class IntentDetector:
    def detect(self, text):
        # Простая проверка на наличие Email
        if re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text):
            return "USER_DATA_SUBMISSION"
        return "GENERAL_CONVERSATION"
