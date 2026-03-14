import re

class ServerNavigator:
    """
    Модуль технической поддержки серверов и сетевых настроек.
    Интеграция с Vast AI, Duck DNS и окружением GitHub.
    """
    def __init__(self):
        # База знаний по инфраструктуре Nitro/NovBase
        self.configs = {
            "vast": (
                "Вайст А И — это площадка для аренды ГПУ мощностей. Для подключения используй SSH-порт, "
                "указанный в инстансе. Рекомендуемый образ — PyTorch или NVIDIA CUDA. "
                "Следи за свободным местом на диске, чтобы база NovBase не заблокировалась."
            ),
            "duck_dns": (
                "Дак ДНС используется для привязки динамического IP к домену. "
                "Обновление адреса происходит через HTTP-запрос с твоим токеном. "
                "Проверь наличие задания в cron, чтобы внешний доступ к Nitro не прерывался."
            ),
            "github_copilot": (
                "Гитхаб Копайлот интегрирован в среду разработки. "
                "Используй контекст проекта для генерации логики модулей. "
                "Убедись, что расширение авторизовано в VS Code для доступа к API."
            ),
            "server": (
                "Сервер Nitro работает на Ubuntu. Среда исполнения — Python 3.10. "
                "Логи системы находятся в директории NovBase/logs. "
                "Для применения изменений используй скрипт ./run_nitro.sh."
            )
        }

    def solve(self, expression: str):
        """Анализ запросов по настройке и навигации сервера."""
        ql = expression.lower()
        results = []

        # 1. Vast AI (ГПУ аренда)
        if any(w in ql for w in ["vast", "васт", "видеокарт", "аренда"]):
            results.append(self.configs["vast"])

        # 2. Duck DNS (Домен и IP)
        if any(w in ql for w in ["duck", "дак", "днс", "домен", "ip", "айпи"]):
            results.append(self.configs["duck_dns"])

        # 3. GitHub / Copilot (Разработка)
        if any(w in ql for w in ["github", "гитхаб", "копайлот", "copilot", "код"]):
            results.append(self.configs["github_copilot"])

        # 4. Общие настройки сервера
        if any(w in ql for w in ["сервер", "настройк", "nitro", "нитро", "ubuntu"]):
            # Если специфичные модули не сработали, даем общую инфу
            if not results:
                results.append(self.configs["server"])

        if results:
            # Возвращаем данные как технический контекст
            return "ТЕХНИЧЕСКИЙ УЗЕЛ: " + " ".join(results)

        return None

# Инициализация модуля для LogicProcessor
server_tool = ServerNavigator()

def solve(expression):
    """Точка входа для диспетчера логики."""
    return server_tool.solve(expression)
