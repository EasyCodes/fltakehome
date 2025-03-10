import json


def load_edges():
    return load_from_json('edges')


def load_events():
    return load_from_json('events')


def load_from_json(filename):
    data = []
    with open(f'input_data/{filename}.json') as file:
        data = json.load(file)
    return data


def get_journeys(events: list[dict]) -> list[dict]:
    if not events:
        return

    journey_ids = set(event['journey_id'] for event in events)
    journeys = []
    for journey_id in journey_ids:
        data_points = [event for event in events if event['journey_id'] == journey_id]

        # could drop journey_key after sorted to save space in lists
        data_points = sorted(data_points, key=lambda d: d['timestamp'])
        journeys.append(data_points)

    return journeys
