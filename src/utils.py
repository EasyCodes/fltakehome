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
