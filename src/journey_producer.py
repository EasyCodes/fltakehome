import json
import logging

from hooks.pulsar_hooks import get_client, get_producer
from utils import get_journeys, load_events


log = logging.getLogger(__name__)


def package_message(journey):
    return json.dumps(journey).encode('utf-8')


def produce_journeys():
    events = load_events()
    journeys = get_journeys(events)

    log.error(f'Total "jouneys" to send: {len(journeys)}')

    client = get_client()
    producer =  get_producer(client)
    for journey in journeys:
        producer.send(package_message(journey))

    log.error('Producer finished. Shutting down...')
    producer.close()
    client.close()

if __name__ == "__main__":
    produce_journeys()
