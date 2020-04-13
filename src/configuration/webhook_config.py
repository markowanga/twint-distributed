import os


def is_webhook_configured() -> bool:
    return 'WEBHOOK_HOST' in os.environ and os.environ['WEBHOOK_HOST'] != 'no_host'


def get_webhook_host() -> str:
    return os.environ['WEBHOOK_HOST']
