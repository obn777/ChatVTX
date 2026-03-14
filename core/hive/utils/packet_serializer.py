import json
from ..knowledge_packet import KnowledgePacket

def serialize_packet(packet: KnowledgePacket) -> str:
    """
    Преобразует пакет знаний в JSON-строку.
    """
    data = {
        "topic": packet.topic,
        "domain": packet.domain,
        "insight": packet.insight,
        "source": getattr(packet, "source", None)
    }
    return json.dumps(data)

def deserialize_packet(data: str) -> KnowledgePacket:
    """
    Восстанавливает объект KnowledgePacket из JSON-строки.
    """
    obj = json.loads(data)
    packet = KnowledgePacket(
        topic=obj["topic"],
        domain=obj["domain"],
        insight=obj["insight"],
        source=obj.get("source")
    )
    return packet
