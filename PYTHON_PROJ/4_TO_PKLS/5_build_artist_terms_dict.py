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
import matplotlib.pyplot as plt
from tqdm import tqdm



def main(args):
    output_folder = args.output_folder
    artists_filename = args.artists_pkl

    artists = load_data(artists_filename)

    terms_dict = dict()

    for _id, _artist in tqdm(artists.items()):
        try:
             terms_dict[_id] = _artist.terms
        except Exception as e:
            print(f'{_id} {e}')

    output_pathname = os.path.join(output_folder, 'terms_per_artist.pkl')

    save_data(terms_dict, output_pathname)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--distances', '-d', required=False, type=str, default='./distances_cc_peak_1.pkl',
                        help='path to pkl distances file')
    parser.add_argument('--ground_truth', '-g', required=False, type=str, default='./ground_truth.pkl',
                        help='path to pkl ground truth file')
    parser.add_argument('--heatmaps', '-hm', required=False, type=str, default='./heatmaps.pkl',
                        help='path to pkl heatmap file')
    parser.add_argument('--names', '-n', required=False, type=str, default='./names.pkl',
                        help='path to pkl name file')
    parser.add_argument('--ranking', '-r', required=False, type=str, default='./.pkl',
                        help='path to ranking file')
    parser.add_argument('--output_folder', '-o', required=False, type=str, default='./OUTPUT',
                        help='output folder')
    parser.add_argument('--artists_pkl', '-a', required=False, type=str, default='./artists_hm.pkl',
                        help='artists dictionary pathname')
    args = parser.parse_args()

    main(args)