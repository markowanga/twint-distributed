import pika

import configuration.rabbit_config as rabbit_config
import utils.docker_logs as docker_logs

logger = docker_logs.get_logger('rabbit_send')


def send_to_rabbit(queue: str, body: str):
    logger.info('send_to_rabbit ' + queue + ' ' + body)
    connection = pika.BlockingConnection(rabbit_config.get_rabbit_connection_config())
    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=True)
    channel.basic_publish(exchange='', routing_key=queue, body=body, properties=pika.BasicProperties(delivery_mode=2))
    connection.close()
    return
