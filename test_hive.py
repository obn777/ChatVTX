from core.hive.hive_node import HiveNode

node = HiveNode()

packet = node.create_packet(
    "distributed cognition",
    "cybernetics",
    "local memory improves reasoning"
)

print(packet.to_dict())
