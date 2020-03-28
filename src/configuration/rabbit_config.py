import os

import pika

_rabbit_host = os.environ['RABBIT_HOST']
_rabbit_username = os.environ['RABBIT_USERNAME']
_rabbit_password = os.environ['RABBIT_PASSWORD']


def get_rabbit_connection_config() -> pika.ConnectionParameters:
    return pika.ConnectionParameters(
        host=_rabbit_host,
        credentials=pika.credentials.PlainCredentials(
            username=_rabbit_username,
            password=_rabbit_password
        ),
        heartbeat=0
    )
