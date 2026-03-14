import os, requests, subprocess, re

class BotConnector:
    def __init__(self, token, base_dir, site_link_top, site_link_bot, vtx_manager):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{token}/"
        self.base_dir = base_dir
        self.site_top = site_link_top
        self.site_bot = site_link_bot
        self.vtx_manager = vtx_manager
        self.piper_exe = os.path.join(base_dir, "core/tts/piper/piper")
        self.piper_model = os.path.join(base_dir, "core/tts/piper/ru_RU-irina-medium.onnx")

    def vtx_censor(self, text):
        if not text: return ""
        forbidden = ["георгий", "georgiy", "nitro", "anv15", "auth", "login"]
        if any(word in text.lower() for word in forbidden):
            return self.vtx_manager.get_rules()
        return text.replace("Малышка", "VTX").replace("малышка", "vtx")

    def send_msg(self, chat_id, text, use_links=True):
        safe_text = self.vtx_censor(text)
        full_text = f"{self.site_top}\n{safe_text}{self.site_bot}" if use_links else safe_text
        try:
            requests.post(self.base_url + "sendMessage",
                         data={"chat_id": chat_id, "text": full_text, "parse_mode": "HTML"}, timeout=15)
        except: pass

    def speak_and_send(self, chat_id, text):
        # Логика генерации голоса Piper и отправки sendVoice
        voice_out = os.path.join(self.base_dir, "temp_voice.ogg")
        clean_text = re.sub('<[^<]+?>', '', self.vtx_censor(text))
        cmd = f'echo "{clean_text}" | {self.piper_exe} --model {self.piper_model} --output_raw | ffmpeg -y -f s16le -ar 22050 -ac 1 -i - -c:a libopus -b:a 32k {voice_out}'
        try:
            subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            with open(voice_out, 'rb') as v:
                requests.post(self.base_url + "sendVoice", data={'chat_id': chat_id}, files={'voice': v})
            if os.path.exists(voice_out): os.remove(voice_out)
        except: pass
