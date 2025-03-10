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



if __name__ == "__main__":
    inspect_edges()
