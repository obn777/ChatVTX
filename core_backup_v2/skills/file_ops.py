import os

def save_to_note(text: str, filename: str = "notes.txt"):
    """
    Записывает текст в файл в папке проекта.
    Путь: /home/obn7/NovBase/notes.txt
    """
    # Определяем базовый путь к проекту
    base_path = "/home/obn7/NovBase"
    full_path = os.path.join(base_path, filename)
    
    try:
        # Режим 'a' (append) добавляет запись в конец, не удаляя старое
        with open(full_path, "a", encoding="utf-8") as f:
            f.write(text + "\n" + "-"*20 + "\n")
        return f"успешно записано в {filename}"
    except Exception as e:
        return f"ошибка записи: {str(e)}"

# Если нужно будет прочитать файл в будущем
def read_notes(filename: str = "notes.txt"):
    path = os.path.join("/home/obn7/NovBase", filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return "Файл пока пуст."
