import json
import logging

import numpy as np
from hmmlearn import hmm

from hooks.postgres_hooks import record_results
from hooks.pulsar_hooks import get_consumer
from utils import get_journeys, load_edges, load_events


log = logging.getLogger(__name__)


def calculate_emissions(gps_points, candidates, N, M, sigma_d, sigma_theta):
    # Emission Probabilities
    emissions = np.zeros((N, M))
    for i, (lat, lon, speed, heading) in enumerate(gps_points):
        probs = []
        for j, seg in enumerate(candidates[i]):
            d = perpendicular_distance((lat, lon), seg)
            theta_diff = min(abs(heading - seg.heading), 360 - abs(heading - seg.heading))
            prob = np.exp(-d**2 / (2 * sigma_d**2)) * np.exp(-theta_diff**2 / (2 * sigma_theta**2))
            probs.append(prob)
        emissions[i, :len(probs)] = np.array(probs) / sum(probs)  # Normalize
    return emissions


def calculate_transitions(gps_points, candidates, edges, N, M, sigma_v):
    # Transition Probabilities
    transitions = np.zeros((M, M))
    for j, seg1 in enumerate(candidates[0]):
        for k, seg2 in enumerate(candidates[1]):
            d_path = shortest_path_distance(seg1, seg2, edges)
            expected_distance = speed * (gps_points[1][3] - gps_points[0][3])
            transitions[j, k] = np.exp(-((d_path - expected_distance) ** 2) / (2 * sigma_v**2))
    transitions /= transitions.sum(axis=1, keepdims=True)  # Normalize
    return transitions


def find_candidate_edges(events, edges):
    # k nearest neighbors
    candidates = []
    for event in events:
        edge_dist = sorted([[dist(event, edge), edge] for edge in edges], key=lambda d: d[0])
        candidates.append([event, edge_dist[0:4]])
    return candidates


def prepare_hmm_data(gps_points, edges, sigma_d=5.0, sigma_theta=10.0, sigma_v=5.0): 
    candidates = find_candidate_edges(gps_points, edges)

    M = max(len(c) for c in candidates)  # Max candidates per point
    N = len(gps_points)  # Number of GPS points

    emissions = calculate_emissions(gps_points, candidates, N, M, sigma_d, sigma_theta)

    transitions = calculate_transitions(gps_points, candidates, edges, N, M, sigma_v)

    return emissions, transitions


def get_hmm_model(emissions, transitions):
    N, M = emissions.shape
    model = hmm.MultinomialHMM(n_components=M)
    model.startprob_ = np.full(M, 1 / M)  # Uniform start probability
    model.transmat_ = transitions  # Use computed transition matrix
    model.emissionprob_ = emissions  # Use computed emission probabilities

    return model


def get_tuned_model():
    # TODO replace dummy untuned model
    return hmm.MultinomialHMM()

    edges = load_edges()
    events = load_events()

    emissions, transitions = prepare_hmm_data(events, edges)

    return get_hmm_model(emissions, transitions)


def initialize_service():
    model = get_tuned_model()
    if not model:
        raise 'MAP_MATCHER Initialization Failed: no model found'

    consumer = get_consumer()  
    if not consumer:
        raise 'MAP_MATCHER Initialization Failed: no Pulsar client found'

    return [model, consumer]


def run():
    batch = []
    model, consumer = initialize_service()

    while True:
        msg = consumer.receive()

        try:
            payload = json.loads(msg.data().decode("utf-8"))

            if not payload:
                log.error('Payload is empty')

            journeys = get_journeys(payload)
            if not journeys:
                log.error('Could not find Journeys in payload provided')

            for journey in journeys: 
                mapping = model.decode(journey, algorithm='viterbi')
                batch.append([journey, mapping])

            if not batch:
                log.error('Payload consumed with no mapping generated')

            record_results(batch)
            consumer.acknowledge(msg)

        except Exception as e:
            log.error(f"Error processing message: {e}")
            consumer.negative_acknowledge(msg)


if __name__ == "__main__":
    run()
