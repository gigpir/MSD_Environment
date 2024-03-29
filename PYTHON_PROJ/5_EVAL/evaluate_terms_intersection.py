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
ranking = None
ground_truth = None
terms = None
min_terms_occurence = None
terms_occurrences = None
mode = None
first_vals = -1
# TODO
# matrice ungherese cambio del peso del picco (proovare 5 e 10)
# creare matrice triangolare delle intersezioni delle liste dei tag (non normalizzate)
# plottare minimo e massimo anzichè confidenza
# analizzare i tag (tag comuni) (singolare plurale)

def mean_confidence_interval(data, confidence=0.95):
    '''
        generate mean and confidence value of a population
    '''
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, h

def filter_list_with_min_occurences(list):
    global min_terms_occurence
    global terms_occurrences

    new_list = []
    for term in list:
        # for each term in the list check if it occurs a minimum number of times
        if terms_occurrences[term] >= min_terms_occurence:
            new_list.append(term)
    return new_list

def apply_filter_to_terms():
    global terms

    terms = map_dict(lambda x: filter_list_with_min_occurences(x), terms)


def compute_intersection_vs_position_slave(positions):
    d = dict()
    global ranking
    global terms
    global mode
    # for each position
    zero_terms_artists = 0
    for pos in positions:
        intersection = []
        # for each artist
        for _id, _ranking in ranking.items():
            try:
                # compute the intersection between the terms of artist _id and the terms of artist at position p
                if mode == 'NORM_STD':
                    tmp = len(set(terms[_id]).intersection(terms[_ranking[pos]])) / len(terms[_id])
                elif mode == 'NORM_OTHER':
                    tmp = len(set(terms[_id]).intersection(terms[_ranking[pos]])) / len(terms[_ranking[pos]])
                elif mode == 'NOT_NORM':
                    tmp = len(set(terms[_id]).intersection(terms[_ranking[pos]]))

                intersection.append(tmp)
            except Exception as e:
                #print(e)
                zero_terms_artists += 1
        if len(intersection) != 0:
            # compute the mean intersection with confidence of terms of artists at position p
            val, conf = mean_confidence_interval(intersection)
            # create a new entry in the dictionary
            if mode == 'NOT_NORM':
                d[pos] = val, conf
            else:
                d[pos] = val*100, conf*100


        else:
            print(f"No artists at position {pos}!!!")

        print(f'THREAD[{os.getpid()}] -> {positions[-1] - pos} positions remaining',end='\r')
    print(f'THREAD[{os.getpid()}] -> found {zero_terms_artists} times artists with no terms')
    return d

def merge_dictionaries(result):
    res = {}
    for dictionary in result:
        res.update(dictionary)
    return res


def compute_intersection_vs_position_master():
    nproc = multiprocessing.cpu_count()

    global ranking
    global ground_truth
    global terms
    global first_vals
    # pick the first not null element in my ranking dictionary
    size = 0
    while size == 0:
        values_view = ranking.values()
        value_iterator = iter(values_view)
        size = len(next(value_iterator))


    if first_vals > 0:
        positions_list = list(range(0, first_vals))
    else:
        positions_list = list(range(0, size))

    split = np.array_split(positions_list, nproc)

    with multiprocessing.Pool(nproc) as p:
        result = p.map(compute_intersection_vs_position_slave, split)

    d = merge_dictionaries(result)

    return d

def print_histogram(d, output_folder):
    global min_terms_occurence
    global mode
    global first_vals
    if first_vals > 0:
        filename = 'intersection_vs_position_min_term_occ' + str(min_terms_occurence) + '_' + mode + '_FIRST_'+str(first_vals)+'.png'
    else:
        filename = 'intersection_vs_position_min_term_occ'+str(min_terms_occurence)+'_'+mode+'.png'
    pathname = os.path.join(output_folder, filename)

    fig, ax = plt.subplots()
    x = []
    y = []
    ci = []
    for k, v in d.items():
        x.append(k)
        y.append(v[0])
        ci.append(v[1])
    x = np.array(x)
    y = np.array(y)
    ci = np.array(ci)

    ax.plot(x, y)
    ax.fill_between(x, (y - ci), (y + ci), color='b', alpha=.1)

    if mode == 'NORM_STD':
        ax.set(xlabel='position in ranking',
               ylabel='mean( terms intersection / reference artist terms list length) (%)',
               title='mean terms intersection vs position')
    elif mode == 'NORM_OTHER':
        ax.set(xlabel='position in ranking',
               ylabel='mean( terms intersection / extern artist terms list length) (%)',
               title='mean terms intersection vs position')
    elif mode == 'NOT_NORM':
        ax.set(xlabel='position in ranking',
               ylabel='mean( terms intersection ) ',
               title='mean terms intersection vs position')

    ax.grid()
    fig.savefig(pathname)


def main(args):
    global ranking
    global ground_truth
    global terms
    global min_terms_occurence
    global terms_occurrences
    global mode
    global first_vals

    first_vals = args.first_vals
    min_terms_occurence = args.min_terms_occurrence

    mode = args.mode
    output_folder = args.output_folder
    ground_truth = load_data(filename=args.ground_truth)
    ranking = load_data(filename=args.ranking)
    terms = load_data(filename=args.terms)
    terms_occurrences = load_data(filename=args.terms_occurrences)

    t0 = time.time()

    if min_terms_occurence > 0:
        print(f'Apply filter to terms, threshold set to {min_terms_occurence}')
        apply_filter_to_terms()

    d = compute_intersection_vs_position_master()
    print(f'Time taken: {time.time()-t0} s')
    print_histogram(d, output_folder)

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
    parser.add_argument('--terms', '-t', required=False, type=str, default='./terms_per_artist.pkl',
                        help='terms per artist file')
    parser.add_argument('--terms_occurrences', '-T', required=False, type=str, default='./terms_occurrences.pkl',
                        help='file that contains occurrence per each term present in the dataset')
    parser.add_argument('--min_terms_occurrence', '-thr', required=False, type=int, default=0,
                        help='set a minimum threshold of occurence under which tags are not considered')
    parser.add_argument('--mode', '-m', required=False, type=str, default='NORM_STD', choices=['NORM_STD','NORM_OTHER','NOT_NORM'],
                        help='set the criteria to compute the intersection')
    parser.add_argument('--first_vals', '-f', required=False, type=int, default=-1,
                        help='if you want to stop the plot at a specific position')
    args = parser.parse_args()

    main(args)
