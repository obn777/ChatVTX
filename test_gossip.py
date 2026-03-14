from core.hive.hive_node import HiveNode
from core.hive.gossip_protocol import GossipProtocol

node1 = HiveNode()
node2 = HiveNode()
node3 = HiveNode()

node1.peers = [node2, node3]

gossip = GossipProtocol(node1)

packet = node1.create_packet(
    "distributed cognition",
    "cybernetics",
    "nodes share knowledge"
)

gossip.spread_packet(packet)
