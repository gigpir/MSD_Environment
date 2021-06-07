import multiprocessing
import os
import sys
# insert at 1, 0 is the script path (or '' in REPL)
import time
from functools import partial
from tqdm import tqdm

sys.path.insert(1, '/home/crottondi/PIRISI_TESI/MSD_Environment/PYTHON_PROJ')
import numpy as np
import argparse
from primary.data_io import save_data, load_data
from primary.heatmap import compute_heatmap_distance, compute_cross_correlation_distance, \
    compute_cross_correlation_distance_normalized
from operator import itemgetter
import os
import pandas as pd



def main(args):
    input_pkl = args.input_pkl
    output_pathname = args.output_pathname

    n_inliners, n_outliers = 0,0
    artists = load_data(input_pkl)
    df = pd.DataFrame(columns=['artist_id', 'song_id', 'tsne_0', 'tsne_1'])

    for a in artists.values():
        for s in a.song_list.values():
            try:
                new_row = {'artist_id': a.id,
                           'song_id': s.id,
                           'tsne_0': s.tsne[0],
                           'tsne_1': s.tsne[1]
                            }
                df = df.append(new_row, ignore_index=True)
                n_inliners += 1
            except:
                n_outliers += 1

    print('n_inliners ', n_inliners)
    print('n_outliers ', n_outliers)

    save_data(dict=df, filename=output_pathname)





if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--input_pkl', '-i', required=True, type=str,
                        help='path to pkl artists dictionary it has to include tsne coordinates')
    parser.add_argument('--output_pathname', '-o', required=False, type=str, default='.',
                        help='output pathname')

    args = parser.parse_args()
    main(args)
