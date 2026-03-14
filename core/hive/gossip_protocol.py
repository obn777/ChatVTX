import random


class GossipProtocol:
    """
    Простейшая реализация gossip-распространения пакетов знаний между узлами.
    """

    def __init__(self, node):
        self.node = node

    def spread_packet(self, packet):
        """
        Отправка пакета случайному соседнему узлу.
        """

        if not self.node.peers:
            print("[Gossip] Нет подключённых узлов")
            return

        peer = random.choice(self.node.peers)

        print(f"[Gossip] {self.node.node_id[:8]} -> {peer.node_id[:8]}")

        peer.receive_packet(packet)

    def broadcast(self, packet):
        """
        Рассылка пакета всем соседним узлам.
        """

        if not self.node.peers:
            print("[Gossip] Нет подключённых узлов")
            return

        for peer in self.node.peers:
            print(f"[Gossip] broadcast -> {peer.node_id[:8]}")
            peer.receive_packet(packet)
