import hashlib

def sha256_hash(data: str) -> str:
    """
    Возвращает SHA-256 хэш строки.

    :param data: входная строка
    :return: hex-представление хэша
    """
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def hash_packet(packet) -> str:
    """
    Хэширует пакет знаний по ключевым атрибутам.

    :param packet: объект с атрибутами topic, domain, insight
    :return: hex-представление хэша
    """
    content = f"{packet.topic}|{packet.domain}|{packet.insight}"
    return sha256_hash(content)
