from collections import Counter
from datetime import datetime, timedelta

class TrendAnalyzer:
    """
    Анализирует историю пакетов знаний SphereGraph
    и выявляет текущие тренды по темам и доменам.
    """

    def __init__(self, sphere_graph):
        """
        Инициализация анализатора.

        :param sphere_graph: объект SphereGraph, содержащий packet_history
        """
        self.sphere_graph = sphere_graph

    def add_packet(self, packet):
        """
        Добавляет пакет в историю трендов.
        """
        # Устанавливаем временную метку, если её нет
        if not hasattr(packet, "timestamp"):
            packet.timestamp = datetime.utcnow()
        # Сохраняем в history SphereGraph
        self.sphere_graph.packet_history.append(packet)

    def top_topics(self, n=5):
        """
        Возвращает топ-N самых активных тем по количеству пакетов.

        :param n: количество топовых тем
        :return: список кортежей (тема, количество)
        """
        topic_counter = Counter()
        for packet in getattr(self.sphere_graph, "packet_history", []):
            topic_counter[packet.topic] += 1
        return topic_counter.most_common(n)

    def top_domains(self, topic, n=5):
        """
        Возвращает топ-N доменов для заданной темы.

        :param topic: тема для анализа
        :param n: количество топовых доменов
        :return: список кортежей (домен, количество)
        """
        domain_counter = Counter()
        for packet in getattr(self.sphere_graph, "packet_history", []):
            if packet.topic == topic:
                domain_counter[packet.domain] += 1
        return domain_counter.most_common(n)

    def recent_trends(self, hours=24):
        """
        Тренды за последние N часов.

        :param hours: число часов для анализа
        :return: список кортежей (тема, количество)
        """
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        recent_counter = Counter()
        for packet in getattr(self.sphere_graph, "packet_history", []):
            if hasattr(packet, "timestamp") and packet.timestamp >= cutoff:
                recent_counter[packet.topic] += 1
        return recent_counter.most_common()

    def top_insights(self, topic, top_n=5):
        """
        Возвращает топ инсайтов по теме.

        :param topic: тема
        :param top_n: количество инсайтов
        :return: список инсайтов
        """
        insights = []
        for packet in getattr(self.sphere_graph, "packet_history", []):
            if packet.topic == topic:
                insights.append(packet.insight)
        counter = Counter(insights)
        return [insight for insight, _ in counter.most_common(top_n)]
