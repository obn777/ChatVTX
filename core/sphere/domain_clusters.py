from collections import defaultdict

class DomainClusters:
    """
    Управление и анализ кластеров доменов по темам.
    Позволяет объединять смежные домены и отслеживать их активность.
    """

    def __init__(self):
        # Структура: {тема: {домен: set(related_domains)}}
        self.clusters = defaultdict(lambda: defaultdict(set))

    def add_relation(self, topic, domain, related_domain):
        """
        Добавить связь между доменами в рамках одной темы.

        :param topic: тема
        :param domain: основной домен
        :param related_domain: связанный домен
        """
        self.clusters[topic][domain].add(related_domain)
        self.clusters[topic][related_domain].add(domain)  # симметрично

    def get_related_domains(self, topic, domain):
        """
        Получить все связанные домены для конкретной темы.

        :param topic: тема
        :param domain: домен
        :return: множество связанных доменов
        """
        return self.clusters.get(topic, {}).get(domain, set())

    def get_clusters_for_topic(self, topic):
        """
        Получить все доменные кластеры для темы.

        :param topic: тема
        :return: словарь {домен: set(related_domains)}
        """
        return self.clusters.get(topic, {})

    def merge_clusters(self, topic, domain_a, domain_b):
        """
        Объединить два доменных кластера в один для темы.

        :param topic: тема
        :param domain_a: первый домен
        :param domain_b: второй домен
        """
        related_a = self.clusters[topic].get(domain_a, set())
        related_b = self.clusters[topic].get(domain_b, set())
        merged = related_a.union(related_b, {domain_a, domain_b})
        for d in merged:
            self.clusters[topic][d] = merged
