import os

import pulsar
from pulsar import Consumer, Producer, Client


PULSAR_BROKER = os.getenv('PULSAR_BROKER_URL', 'pulsar://localhost:6650')
TOPIC_NAME = os.getenv('PULSAR_TOPIC', 'journeys')


def get_client() -> Client:
    return pulsar.Client(PULSAR_BROKER)


def get_consumer(client) -> Consumer:
    return client.subscribe(TOPIC_NAME, subscription_name="map_matcher", consumer_type=pulsar.ConsumerType.Shared)


def get_producer(client) -> Producer:
    return client.create_producer(TOPIC_NAME)
