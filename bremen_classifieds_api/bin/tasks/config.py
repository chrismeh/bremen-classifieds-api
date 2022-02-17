from bremen_classifieds_api.platform.config import parse_config

config = parse_config()

accept_content = ["pickle"]
task_serializer = "pickle"
broker_url = f"redis://{config.redis_host}"
