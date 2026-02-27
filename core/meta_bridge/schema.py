# Схемы данных Meta Bridge
ADAPTATION_EVENT_SCHEMA = {
    "event_id": "uuid",
    "timestamp": "str",
    "type": "adaptation_event",
    "context": {},
    "metrics": {},
    "payload": {},
    "status": "new"
}

RECOMMENDATION_SCHEMA = {
    "recommendation_id": "uuid",
    "timestamp": "str",
    "target_event_id": "uuid",
    "action": "adjust_parameter",
    "details": {},
    "priority": "low",
    "status": "proposed"
}
