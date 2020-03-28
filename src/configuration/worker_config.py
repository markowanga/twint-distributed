import os


def get_queue_name() -> str:
    return os.environ['QUEUE_NAME']
