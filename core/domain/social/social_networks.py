import re
from typing import Optional, List


class SocialAnalyzer:
    """
    Модуль анализа лимитов, форматов и технических ограничений
    популярных социальных платформ.

    Адаптирован для чистого произношения (Piper) и понимания разговорной речи.
    """

    def __init__(self):
        # Технические спецификации (вокализованы для Ирины)
        self.platforms = {
            "telegram": {
                "aliases": ["телеграм", "telegram", "tg", "телега", "телеги", "телегу", "телеге"],
                "info": (
                    "Телеграм. Лимит текста — 4096 символов. "
                    "Максимальный размер файла для бота — до двух гигабайт. "
                    "Для обычных пользователей — до двух гигабайт, с подпиской Премиум — до четырех гигабайт. "
                    "Видеосообщения в форме кружочков — до 60 секунд."
                )
            },
            "tiktok": {
                "aliases": ["тик ток", "тикток", "tiktok", "тик тока", "тик токе"],
                "info": (
                    "Тик Ток. Оптимальное соотношение сторон — 9 на 16. "
                    "Максимальная длительность видео — до 10 минут. "
                    "Рекомендуемый формат — Эм Пэ 4 с кодеком Эйч 264."
                )
            },
            "youtube": {
                "aliases": ["ютуб", "youtube", "ютуба", "ютубе"],
                "info": (
                    "Ютуб. Шортс — вертикальные видео до 60 секунд. "
                    "Длинные видео — до 12 часов при подтвержденном аккаунте. "
                    "Лимит названия — 100 символов."
                )
            },
            "instagram": {
                "aliases": ["инстаграм", "instagram", "инста", "инсты", "инсту", "инсте"],
                "info": (
                    "Инстаграм. Подпись к посту — до 2200 символов. "
                    "Рилс — до 90 секунд. "
                    "Карусель — до 10 фотографий или видео."
                )
            }
        }

        # Ключевые слова для общих вопросов
        self.limit_keywords = [
            "лимит", "ограничение", "размер", "длина", "максимальный", "формат"
        ]

    # -------------------------

    def _detect_platforms(self, text: str) -> List[str]:
        """Определяет упомянутые платформы, игнорируя окончания."""
        found = []

        for platform_data in self.platforms.values():
            for alias in platform_data["aliases"]:
                # Поиск по границам слов (\b), чтобы не путать короткие алиасы
                if re.search(rf"\b{re.escape(alias)}\b", text):
                    found.append(platform_data["info"])
                    break

        return found

    # -------------------------

    def solve(self, expression: str) -> Optional[str]:
        """
        Основная точка входа.
        """
        if not expression:
            return None

        text = expression.lower().strip()

        # 1. Поиск конкретных платформ (теперь понимает "в инсте", "телегу" и т.д.)
        platform_results = self._detect_platforms(text)
        if platform_results:
            return "АНАЛИЗ СОЦИАЛЬНЫХ СЕТЕЙ.\n\n" + "\n\n".join(platform_results)

        # 2. Общий вопрос о лимитах без указания платформы
        if any(keyword in text for keyword in self.limit_keywords):
            return (
                "Уточните платформу. Я знаю параметры Телеграм, Тик Ток, Ютуб и Инстаграм, "
                "чтобы предоставить точные технические ограничения."
            )

        return None


# Экземпляр для интеграции
social_tool = SocialAnalyzer()


def solve(expression: str) -> Optional[str]:
    """
    Унифицированная точка входа для LogicProcessor.
    """
    return social_tool.solve(expression)
