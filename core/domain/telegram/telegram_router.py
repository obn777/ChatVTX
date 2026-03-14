class TelegramRouter:
    def __init__(self, admin_id):
        self.admin_id = admin_id

    def resolve_action(self, user_id, text, state):
        text = text.lower().strip()

        if state == 'WAIT_DATA':
            return "SUBMIT_DATA"
        if text == "заявка на ключ":
            return "START_REGISTRATION"
        if user_id == self.admin_id:
            if text.startswith("одобряю "): return "ADMIN_APPROVE"
            if text.startswith("канал:"): return "ADMIN_BROADCAST"

        return "GENERAL_CHAT"
