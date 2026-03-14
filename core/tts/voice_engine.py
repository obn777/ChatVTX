import subprocess
import os

class VoiceEngine:
    """
    Голосовой движок системы NovBase. 
    Гарантированное выключение через pkill -9, как в терминале.
    """
    def __init__(self):
        self.base_path = "/home/obn7/NovBase/core/tts/piper"
        self.piper_exe = os.path.join(self.base_path, "piper")
        
        self.voice_models = {
            "female": os.path.join(self.base_path, "ru_RU-irina-medium.onnx"),
            "male": os.path.join(self.base_path, "ru_RU-denis-medium.onnx")
        }
        
        self.current_mode = "female"
        self.length_scale = "0.9" 
        self.noise_scale = "0.667"

    def stop(self):
        """Метод 'Стоп-кран': убивает все звуковые процессы мгновенно."""
        try:
            # Выполняем те самые команды, которые сработали у тебя вручную
            subprocess.run("pkill -9 aplay", shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            subprocess.run("pkill -9 piper", shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            # Зачистка роботов на всякий случай
            subprocess.run("pkill -9 espeak", shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            subprocess.run("pkill -9 espeak-ng", shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        except Exception:
            pass

    def _detect_voice_trigger(self, text: str):
        """Смена личности голоса по триггерам в тексте."""
        low_text = text.lower()
        if "мужской голос" in low_text or "говори как мужчина" in low_text:
            self.current_mode = "male"
            return True
        if "женский голос" in low_text or "верни женский" in low_text:
            self.current_mode = "female"
            return True
        return False

    def speak(self, text: str):
        """Запуск озвучки с предварительной очисткой памяти."""
        if not os.path.exists(self.piper_exe):
            return

        # ПЕРЕД каждой новой фразой вызываем жесткий стоп
        self.stop()

        if not text or len(text.strip()) == 0:
            return

        self._detect_voice_trigger(text)
        model_path = self.voice_models.get(self.current_mode)
        
        if not os.path.exists(model_path):
            model_path = self.voice_models["female"]

        # Очистка текста от символов, которые могут мешать shell-команде
        clean_text = text.replace('"', '').replace("'", "").replace('*', '')
        clean_text = clean_text.replace('#', '').replace('_', '').replace('`', '').replace(';', '')
        
        # Конвейер: Текст -> Piper -> Динамики
        cmd = (
            f'echo "{clean_text}" | '
            f'{self.piper_exe} --model {model_path} '
            f'--length_scale {self.length_scale} '
            f'--noise_scale {self.noise_scale} '
            f'--output_raw | '
            f'aplay -r 22050 -f S16_LE'
        )

        try:
            # Запуск в фоновом режиме через независимую группу процессов
            subprocess.Popen(
                cmd, 
                shell=True, 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL,
                preexec_fn=os.setsid 
            )
        except Exception:
            pass

# Глобальный объект для импорта в app.py
voice = VoiceEngine()
