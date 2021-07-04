import multiprocessing
import os
import sys
# insert at 1, 0 is the script path (or '' in REPL)
import time
from functools import partial
from tqdm import tqdm

sys.path.insert(1, '/home/crottondi/PIRISI_TESI/MSD_Environment/PYTHON_PROJ')
from primary.utility import map_dict
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
import scipy.stats

terms_per_artist = None

def compute_terms_intersection_slave(ids):
    d = {}

    global terms_per_artist

    # compute terms intersection for my batch
    for outer_id in ids:
        # check if artist has actually terms attached
        if terms_per_artist[outer_id] != []:
            d[outer_id] = {}

            # iterate over other artists
            for inner_id, inner_terms in terms_per_artist.items():
                # check if artist has actually terms attached
                if inner_terms != []:
                    # compute intersection and add it to the dictionary
                    d[outer_id][inner_id] = len(set(terms_per_artist[outer_id]).intersection(inner_terms))

    return d

def merge_dictionaries(result):
    res = {}
    for dictionary in result:
        res.update(dictionary)
    return res

def compute_terms_intersection_master(artists_ids):
    nproc = multiprocessing.cpu_count()

    split = np.array_split(artists_ids, nproc)

    with multiprocessing.Pool(nproc) as p:
        result = p.map(compute_terms_intersection_slave, split)

    d = merge_dictionaries(result)

    df = pd.DataFrame.from_dict(d)

    return df

def main(args):
    # creare matrice triangolare delle intersezioni delle liste dei tag (non normalizzate)

    global terms_per_artist

    terms_per_artist = load_data(filename=args.terms)

    artists_ids = list(terms_per_artist.keys())

    t0 = time.time()
    df = compute_terms_intersection_master(artists_ids)
    print(f'Time taken for computing the matrix: {time.time()-t0}')

    output_folder = args.output_folder

    output_pathname = os.path.join(output_folder, 'artists_terms_intersection.pkl')

    save_data(dict=df, filename=output_pathname)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_folder', '-o', required=False, type=str, default='./OUTPUT',
                        help='output folder')
    parser.add_argument('--terms', '-t', required=False, type=str, default='./terms_per_artist.pkl',
                        help='terms per artist file')
    args = parser.parse_args()

    main(args)
