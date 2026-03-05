#!/bin/bash

# Цвета для вывода
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE} Запуск полной сборки NovBase на Nitro-ANV15-41...${NC}"

# 1. Проверка окружения
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "Ошибка: Скрипт предназначен только для Linux."
    exit 1
fi

# 2. Обновление и установка системных зависимостей
echo -e "${GREEN}📦 Установка системных пакетов...${NC}"
sudo apt update && sudo apt install -y python3-venv python3-pip git build-essential

# 3. Создание виртуального окружения
echo -e "${GREEN}🐍 Создание venv...${NC}"
python3 -m venv venv
source venv/bin/activate

# 4. Установка Python зависимостей
echo -e "${GREEN} Установка библиотек...${NC}"
pip install --upgrade pip
pip install flask requests python-dotenv aiohttp werkzeug numpy

# 5. Проверка путей и структуры
echo -e "${GREEN}📁 Проверка структуры папок...${NC}"
mkdir -p core/domain/physics core/domain/social core/behavior/modes configs models

# 6. Настройка прав (важно для локальных бэкапов)
echo -e "${GREEN}🔐 Настройка прав доступа...${NC}"
chmod -R 755 /home/obn7/NovBase
mkdir -p /home/obn7/NovBase_backups

# 7. Финальный отчет
echo -e "${BLUE}✅ Сборка завершена успешно!${NC}"
echo -e "Используй: ${GREEN}source venv/bin/activate && python3 bot.py${NC} для запуска."
