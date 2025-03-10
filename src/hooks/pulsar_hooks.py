import os

import pulsar


PULSAR_BROKER = os.getenv('PULSAR_BROKER_URL', 'pulsar://localhost:6650')
TOPIC_NAME = os.getenv('PULSAR_TOPIC', 'journeys')


def get_consumer():
    # Pulsar Consumer
    client = pulsar.Client(PULSAR_BROKER)
    return client.subscribe(TOPIC_NAME, subscription_name="map_matcher", consumer_type=pulsar.ConsumerType.Shared)
