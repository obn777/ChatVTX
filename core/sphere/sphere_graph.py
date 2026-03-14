from collections import defaultdict
from .trend_analyzer import TrendAnalyzer
from .domain_clusters import DomainClusters

class SphereGraph:
    """
    Глобальная карта знаний сети Hive.
    Вершины — темы/домены.
    Рёбра — взаимосвязь знаний.
    """

    def __init__(self):
        # структура: {topic: {domain: weight}}
        self.graph = defaultdict(lambda: defaultdict(float))
        # история пакетов для анализа
        self.packet_history = []

        # дополнительные модули
        self.trends = TrendAnalyzer(self)
        self.clusters = DomainClusters()

    # ===== Работа с пакетами знаний =====
    def add_packet(self, packet):
        """
        Добавляет пакет знаний в граф.
        packet должен иметь атрибуты:
          - topic
          - domain
          - insight
        """
        topic = packet.topic
        domain = packet.domain

        # увеличение веса узла
        self.graph[topic][domain] += 1.0

        # сохранить пакет для анализа трендов
        self.packet_history.append(packet)

        # обновить тренды
        self.trends.add_packet(packet)

        # обновить кластеры
        self.clusters.add_cluster(topic, domain, domain)

    # ===== Работа с графом =====
    def get_topics(self):
        """Возвращает список всех тем"""
        return list(self.graph.keys())

    def get_domains(self, topic):
        """Возвращает домены для темы"""
        return list(self.graph[topic].keys())

    def get_weight(self, topic, domain):
        """Возвращает текущий вес связи"""
        return self.graph[topic][domain]

    def merge(self, other_graph):
        """
        Объединяет текущий граф с другим SphereGraph.
        """
        for topic, domains in other_graph.graph.items():
            for domain, weight in domains.items():
                self.graph[topic][domain] += weight

        # объединяем историю пакетов
        self.packet_history.extend(other_graph.packet_history)

        # объединяем тренды и кластеры
        for topic in getattr(other_graph.trends, "top_topics", []):
            self.trends.add_insights(topic, other_graph.trends.top_topics())

        for topic, domains in getattr(other_graph.clusters, "clusters", {}).items():
            for domain, cluster_set in domains.items():
                for d in cluster_set:
                    self.clusters.add_cluster(topic, domain, d)

    # ===== Обёртки для трендов и кластеров =====
    def analyze_trends(self, topic, insights):
        """Добавляет новые инсайты в тренды"""
        self.trends.add_insights(topic, insights)

    def top_insights(self, topic, top_n=5):
        """Возвращает текущие инсайты по теме"""
        return self.trends.top_insights(topic, top_n)

    def cluster_domains(self, topic, domain_pairs):
        """Создаёт кластеры доменов"""
        for a, b in domain_pairs:
            self.clusters.add_cluster(topic, a, b)

    def get_cluster(self, topic, domain):
        """Возвращает список доменов в кластере"""
        return self.clusters.get_cluster(topic, domain)
