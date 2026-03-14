import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_vtx_key(target_email, user_name, generated_key, attachment_path=None):
    """
    Отправляет Email через системный ящик VTX (vtxm777@gmail.com).
    Поддерживает передачу ключей доступа и вложений (цифровых клонов).
    """
    # Параметры подключения к серверу Google
    smtp_server = "smtp.gmail.com"
    port = 587

    # СИСТЕМНЫЕ ДАННЫЕ (Авторизация узла)
    sender_email = "vtxm777@gmail.com"
    # Твой новый 16-значный пароль приложения
    password = "qfynicegsaamjruy"

    # ЗАГОЛОВОК ОТПРАВИТЕЛЯ
    display_name = "VTX System Core"
    subject = "🔑 Твой ключ доступа к VTX ULTRA CORE"

    # ТЕКСТ ПИСЬМА
    body = f"""
    Приветствуем, {user_name}.

    Твоя заявка на доступ к терминалу VTX была обработана автоматически.
    Твой персональный ключ: {generated_key}

    Вход в терминал: https://chatvtx.xyz

    Инструкция:
    1. Перейди по ссылке выше.
    2. В поле ввода ключа вставь: {generated_key}
    3. Нажми 'Вход в систему'.

    Внимание: Не передавай этот ключ третьим лицам.
    Данное сообщение сформировано автоматически нейронным ядром VTX.
    ---
    Система: VTX Core (Nitro Node)
    Статус: Авторизовано
    """

    msg = MIMEMultipart()
    msg['From'] = f"{display_name} <{sender_email}>"
    msg['To'] = target_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    # Логика работы с вложениями (Digital Clones / Backups)
    if attachment_path and os.path.exists(attachment_path):
        try:
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            encoders.encode_base64(part)
            filename = os.path.basename(attachment_path)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename}",
            )
            msg.attach(part)
        except Exception as e:
            print(f"⚠️ [MAILER] Ошибка прикрепления файла: {e}")

    # Процесс отправки через TLS
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.set_debuglevel(0)
        server.starttls()  # Шифрование сессии
        server.login(sender_email, password)
        server.send_message(msg)
        server.quit()

        print(f"✅ [MAILER] Успешная отправка на {target_email} (через vtxm777)")
        return True

    except Exception as e:
        print(f"❌ [MAILER] Ошибка отправки: {e}")
        return False
