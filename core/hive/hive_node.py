import uuid

from core.hive.knowledge_packet import KnowledgePacket
from core.hive.node_rank import NodeRank


class HiveNode:

    def __init__(self, node_id=None):

        self.node_id = node_id or str(uuid.uuid4())
        self.rank = NodeRank()
        self.peers = []

    def create_packet(self, topic, domain, insight):

        packet = KnowledgePacket(
            source=self.node_id,
            topic=topic,
            domain=domain,
            insight=insight
        )

        return packet

    def receive_packet(self, packet):

        print(f"[Hive] Packet received from {packet.source}")
