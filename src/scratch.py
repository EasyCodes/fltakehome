from matplotlib import collections as mc
import pylab as pl

from utils import load_edges, load_events
from pmap_matcher import get_hmm_model, prepare_hmm_data


def inspect_edges():
  edges = load_edges()

  start_nodes = set(edge['start_node_id'] for edge in edges)
  end_nodes = set(edge['end_node_id'] for edge in edges)

  print(f'num of edges {len(edges)}')
  print(f'num of starting nodes {len(start_nodes)}')
  print(f'num of ending nodes {len(start_nodes)}')
  print(f'unique nodes {len(start_nodes & end_nodes)}')


def plot_edgets():
  edges = load_edges()
  lines = [edge['gps']['coordinates'] for edge in edges]

  lc = mc.LineCollection(lines, linewidths=2)
  fig, ax = pl.subplots()
  ax.add_collection(lc)
  ax.autoscale()
  ax.margins(0.1)
  pl.show()
  

def get_journeys(events: list[dict]) -> list[dict]:
  journey_ids = set(event['journey_id'] for event in events)
  journeys = []
  for journey_id in journey_ids:
    data_points = [event for event in events if event['journey_id'] == journey_id]
    
    # could drop journey_key after sorted to save space in lists
    data_points = sorted(data_points, key=lambda d: d['timestamp'])
    journeys.append(data_points)
  
  return journeys
    
def get_trained_model()
  edges = load_edges()
  events = load_events()
  journeys = get_journeys(events)

  emissions, transitions = prepare_hmm_data(events, edges)

  model = get_hmm_model(emissions, transitions)

  prob, likely_path = model.decode(journeys[0], algorithm='viterbi')


if __name__ == "__main__":
  inspect_edges()
