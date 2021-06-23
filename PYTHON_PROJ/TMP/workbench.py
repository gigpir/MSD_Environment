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
def distance_vs_gt_position(ground_truth, distances):
    gt_distances = np.zeros((len(ground_truth), 100))
    gt_distances.fill(np.nan)
    n = 0
    for i, (id_outer, l) in enumerate(ground_truth.items()):
        for j, id_inner in enumerate(l):
            try:
                gt_distances[i, j] = distances[id_outer][id_inner]
            except:
                n += 1

    print(n)
    return gt_distances


def print_histograms(gt_distances, folder):
    path = folder
    if not os.path.exists(path):
        os.makedirs(path)

    for position in range(100):
        try:
            _ = plt.hist(gt_distances[:, position], bins=30)
            plt.xlabel('distance value')
            plt.ylabel('occurrences', fontsize=16)
            title = 'ground truth distances distribution @ position ' + str(position)
            plt.title(title)
            filename = str(position) + '.png'
            path_name = os.path.join(path, filename)
            plt.savefig(path_name, dpi=300)
            plt.close('all')
        except:
            print('Could not print histogram for position '+ str(position))


def compute_minimum_size_to_total_intersection(ground_truth, my_ranking, output_folder):

    d = dict()

    for _id, gt_list in tqdm(ground_truth.items()):
        if (_id in my_ranking.keys()) and (len(gt_list)>0) :
            for i in range(len(my_ranking[_id])):
                size = len(set(my_ranking[_id][:i]).intersection(gt_list))
                if size >= len(gt_list):
                    break
            d[_id] = i+1
        #else:
            #print(_id ,(_id in my_ranking.keys()), (len(gt_list) > 0))
    filename = os.path.join(output_folder, 'minimum_size_to_total_intesection.png')

    plt.hist(d.values(), bins='auto')
    plt.savefig(filename)


def compute_intersection_percentage_vs_considered_ranking_size(ground_truth, my_ranking, output_folder):

    d = dict()

    #pick the first not null element in my ranking dictionary
    size = 0
    while size == 0:
        values_view = my_ranking.values()
        value_iterator = iter(values_view)
        size = len(next(value_iterator))

    for i in tqdm(range(size)):
        percentages = []
        for _id, gt_list in ground_truth.items():
            if (_id in my_ranking.keys()) and (len(gt_list)>0) :
                size = len(set(my_ranking[_id][:i]).intersection(gt_list)) / len(gt_list)
                percentages.append(size)
            # else:
            #     print(_id ,(_id in my_ranking.keys()), (len(gt_list) > 0))
        d[i] = np.mean(percentages)*100
    filename = os.path.join(output_folder, 'intersection_vs_considered_ranking_size.png')

    fig, ax = plt.subplots()
    ax.plot(list(d.keys()), list(d.values()))

    #compute the mean lenght of the ground truth
    lenghts = map(lambda x: len(x), list(ground_truth.values()))
    print(f'Ground truth mean size: {np.mean(list(lenghts))}')

    ax.set(xlabel='portion of predicted ranking', ylabel='intersection size / ground truth size (%)',
           title='intersection vs considered ranking_size')
    ax.grid()
    fig.savefig(filename)


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

    #names = load_data(filename=args.names)
    #heatmaps = load_data(filename=args.heatmaps)
    ground_truth = load_data(filename=args.ground_truth)
    #distances = load_data(filename=args.distances)
    ranking = load_data(filename=args.ranking)
    #artists = load_data(filename=args.artists_pkl)
    output_folder =args.output_folder
    #compute_minimum_size_to_total_intersection(ground_truth=ground_truth, my_ranking=ranking, output_folder=output_folder)
    compute_intersection_percentage_vs_considered_ranking_size(ground_truth=ground_truth, my_ranking=ranking, output_folder=output_folder)
    # for i, a in enumerate(artists.values()):
    #     for s in a.song_list.values():
    #         try:
    #             print(s.id, s.tsne[0], s.tsne[1])
    #         except:
    #             print(s.id, 'NO tsne')
    #     if i > 100:
    #         exit(0)
    #output_folder = args.output_folder
    #print_histograms(gt_distances=distance_vs_gt_position(ground_truth=ground_truth, distances=distances), folder=output_folder)
