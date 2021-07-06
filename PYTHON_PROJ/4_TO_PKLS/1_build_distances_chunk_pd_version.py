import multiprocessing
import os
import sys
# insert at 1, 0 is the script path (or '' in REPL)
import time
from functools import partial

import pandas as pd

sys.path.insert(1, '/home/crottondi/PIRISI_TESI/MSD_Environment/PYTHON_PROJ')
import numpy as np
import argparse
from primary.data_io import save_data, load_data
from primary.heatmap import compute_heatmap_distance, compute_cross_correlation_distance, \
    compute_cross_correlation_distance_normalized, \
    compute_distance_bipartite_graph_hungarian


artists = None
metric = None
df = None
def build_matrix_slave(metric,artists_ids):
    global artists
    df = pd.DataFrame(columns=list(artists.keys()), index=artists_ids)
    for i, a_outer_id in enumerate(artists_ids):
        for a_inner_id, a_inner in artists.items():
            if a_inner_id != a_outer_id:
                try:
                    if artists[a_outer_id].tsne_heatmap is not None and a_inner.tsne_heatmap is not None:
                        if metric == 'cc_peak_1':
                            df.at[a_outer_id, a_inner_id] = compute_cross_correlation_distance(h1=artists[a_outer_id].tsne_heatmap,
                                                                                           h2=a_inner.tsne_heatmap)
                        elif metric == 'cc_peak_2':
                            df.at[a_outer_id, a_inner_id] = compute_cross_correlation_distance_normalized(
                                h1=artists[a_outer_id].tsne_heatmap,
                                h2=a_inner.tsne_heatmap)
                        elif metric == 'bipartite_hungarian':
                            df.at[a_outer_id, a_inner_id] = compute_distance_bipartite_graph_hungarian(
                                h1=artists[a_outer_id].tsne_heatmap,
                                h2=a_inner.tsne_heatmap)
                except Exception as e:
                    print(e)
        print(i, ' / ', len(artists_ids))
    return df

def build_matrix_master(chunk):
    global artists
    start = time.time()
    func = partial(build_matrix_slave, metric)

    #nproc = multiprocessing.cpu_count()
    nproc = 4
    artists_ids = list(chunk)

    # initialize dataframe

    split = np.array_split(artists_ids, nproc)

    with multiprocessing.Pool(nproc) as p:
        result = p.map(func, split)
    del artists
    df = pd.concat(result)
    #DEBUG
    #result = func(artists_ids)
    print(time.time() - start)
    return df


def main(args):
    input_path = args.input_pkl
    output_path = args.output_path
    global metric
    metric = args.metric
    global artists
    artists = load_data(input_path)

    chunk_pathname = args.input_chunk
    print('LOADING CHUNKS...')
    chunk = load_data(filename=chunk_pathname)
    print('DONE')

    df = build_matrix_master(chunk=chunk)

    chunk_basename = os.path.basename(chunk_pathname)
    os.path.splitext(chunk_basename)
    chunk_name = os.path.splitext(chunk_basename)[0]
    chunk_name = chunk_name + '_OUT' + '.pkl'
    output_pathname = os.path.join(output_path, chunk_name)

    save_data(filename=output_pathname, dict=df)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--input_chunk', '-ic', required=True, type=str,
                        help='path to pkl chunk of artists')

    parser.add_argument('--input_pkl', '-i', required=True, type=str,
                        help='path to pkl artists dictionary it has to include heatmaps attached')
    parser.add_argument('--output_path', '-o', required=False, type=str, default='',
                        help='path where output data will be saved')
    parser.add_argument('--metric', '-m', required=False, type=str, default='cc_peak_1',
                        choices=['cc_peak_1', 'cc_peak_2', 'bipartite_hungarian'], help='metric type:\n'
                                                                 'cc_peak_1 con peak_thresh=1\n'
                                                                 'cc_peak_2 calcolare la distanza da shift_0 e normalizzare (dividere) la distanza per il valore del picco\n'
                                                                    'bipartite_hungarian calcolare la distanza utilizzando associazioni tra grafi bipartiti + metodo ungherese')

    args = parser.parse_args()
    main(args)


