import multiprocessing
import sys
# insert at 1, 0 is the script path (or '' in REPL)
import time
from functools import partial

from tqdm import tqdm

sys.path.insert(1, '/home/crottondi/PIRISI_TESI/MSD_Environment/PYTHON_PROJ')
import numpy as np
import argparse
from primary.data_io import retrieve_artist_dict, save_data, load_data
from primary.prep import gen_dataset, remove_outlier, normalize
from primary.tsne import prepare_dataset, tsne,attach_tsne_to_art_dict, remove_outliers_lof, get_features_dict
from primary.utility import optimize_artists_dictionary, clean_similar_artists
from primary.heatmap import heatmap
from primary.rbo import RankingSimilarity
import matplotlib.pyplot as plt


gt = None
ranking = None

def compute_rbo_slave(list_ids):
    global ranking
    global gt
    res = []
    for gt_id, gt_list in gt.items():
        if len(gt_list) > 0:
            if gt_id in ranking:
                if len(ranking[gt_id]) > 0:
                    res.append(RankingSimilarity(gt_list, ranking[gt_id][:100]).rbo())
    return res

def merge_result(result):
    final = []
    for r in result:
        final += r
    return final

def compute_rbo_master():
    global ranking
    start = time.time()

    nproc = multiprocessing.cpu_count()
    artists_ids = list(ranking.keys())

    split = np.array_split(artists_ids, nproc)

    with multiprocessing.Pool(nproc) as p:
        result = p.map(compute_rbo_slave, split)

    rbos = merge_result(result=result)

    print(time.time() - start)
    return rbos



def main(args):
    global gt
    global ranking
    gt = load_data(args.ground_truth)
    ranking = load_data(args.ranking)

    rbos = compute_rbo_master()

    #print(rbos)
    print(args.ranking)
    print(f'AVG RBO {np.mean(np.array(rbos))}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--ground_truth', '-gt', required=True, type=str, help='path to ground_truth.pkl file')
    parser.add_argument('--ranking', '-r', required=True, type=str, help='path to max_length_ranking_*.pkl file')

    args = parser.parse_args()

    main(args)

