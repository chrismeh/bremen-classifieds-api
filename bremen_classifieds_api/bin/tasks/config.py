from environs import Env

env = Env()
env.read_env()

accept_content = ["pickle"]
task_serializer = "pickle"
broker_url = f"redis://{env.str('REDIS_HOST', 'localhost')}"
