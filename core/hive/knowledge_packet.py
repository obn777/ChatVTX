import time
import hashlib
import json


class KnowledgePacket:
    """
    Пакет передачи знаний между узлами Hive.
    """

    def __init__(self, source, topic, domain, insight, confidence=0.5):

        self.source = source
        self.topic = topic
        self.domain = domain
        self.insight = insight
        self.confidence = confidence
        self.timestamp = time.time()

        self.packet_id = self._generate_id()

    def _generate_id(self):
        """
        Генерация уникального идентификатора пакета.
        """

        raw = f"{self.source}{self.topic}{self.timestamp}"

        return hashlib.sha256(raw.encode()).hexdigest()

    def to_dict(self):
        """
        Преобразование пакета в словарь.
        """

        return {
            "packet_id": self.packet_id,
            "source": self.source,
            "topic": self.topic,
            "domain": self.domain,
            "insight": self.insight,
            "confidence": self.confidence,
            "timestamp": self.timestamp
        }

    def to_json(self):
        """
        Сериализация пакета в JSON.
        """

        return json.dumps(self.to_dict(), ensure_ascii=False)

    @staticmethod
    def from_dict(data):
        """
        Восстановление пакета из словаря.
        """

        packet = KnowledgePacket(
            source=data["source"],
            topic=data["topic"],
            domain=data["domain"],
            insight=data["insight"],
            confidence=data.get("confidence", 0.5)
        )

        packet.packet_id = data["packet_id"]
        packet.timestamp = data["timestamp"]

        return packet
