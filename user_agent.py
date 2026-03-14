from pyrogram import Client, filters
import time

# Данные из my.telegram.org
api_id = 1234567 # ТВОЙ ID
api_hash = "abcdef123456..." # ТВОЙ HASH

app = Client("malyshka_user", api_id=api_id, api_hash=api_hash)

# Список ключевых слов, на которые Малышка будет агриться в чатах
KEYWORDS = ["ии", "ai", "нейросеть", "gpt", "llm", "прогноз"]

@app.on_message(filters.group & ~filters.me)
def chat_monitor(client, message):
    text = message.text.lower() if message.text else ""
    
    # Если кто-то упомянул ключевое слово
    if any(word in text for word in KEYWORDS):
        print(f"🔍 Нашла обсуждение в чате {message.chat.title}")
        
        # Берем логику из нашего LogicProcessor (или ai_expert)
        from core.domain.ai.ai_expert import solve
        reply = solve(text)
        
        if reply:
            # Делаем паузу, чтобы выглядело как будто человек пишет
            time.sleep(random.randint(5, 15))
            message.reply_text(f"Интересная мысль! {reply}\nКстати, я анализирую это на своем узле.")

app.run()
