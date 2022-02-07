import os


def fixture(file_name: str) -> str:
    with open(os.path.join(os.path.dirname(__file__), f"fixtures/{file_name}")) as f:
        return f.read()
