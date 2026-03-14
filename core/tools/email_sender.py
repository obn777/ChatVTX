import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_vtx_key(target_email, generated_key):
    # Данные твоего почтового сервера (лучше вынести в .env)
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = "vtx.system.core@gmail.com" 
    password = "твой_пароль_приложения" # Специальный пароль для сторонних приложений

    subject = "🔑 Твой ключ доступа к VTX ULTRA CORE"
    body = f"""
    Приветствуем, пользователь.
    
    Твоя заявка на доступ к терминалу VTX была обработана автоматически.
    Твой персональный ключ: {generated_key}
    
    Вход в терминал: https://chatvtx.xyz
    
    Внимание: Не передавай этот ключ третьим лицам.
    ---
    Система: VTX Core (Nitro Node)
    """

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = target_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls() # Шифрование
        server.login(sender_email, password)
        server.sendmail(sender_email, target_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"❌ Ошибка отправки почты: {e}")
        return False
