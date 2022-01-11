imports = "train.tasks"
timezone = "UTC"
accept_content = ["json", "msgpack", "yaml"]
task_serializer = "json"
result_serializer = "json"
beat_schedule = {
    "current_speed": {"task": "current_speed", "schedule": 10.0},
    "train_station": {"task": "train_station", "schedule": 20.0},
}
task_routes = {
    "current_speed": {"queue": "speed", "routing_key": "speed"},
    "train_station": {"queue": "station", "routing_key": "station"},
}
