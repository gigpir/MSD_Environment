import sys
# insert at 1, 0 is the script path (or '' in REPL)

sys.path.insert(1, '/home/crottondi/PIRISI_TESI/MSD_Environment/PYTHON_PROJ')
import argparse
from primary.data_io import save_data, load_data
import gc
import pandas as pd
def getCurrentMemoryUsage():
    ''' Memory usage in kB '''

    with open('/proc/self/status') as f:
        memusage = f.read().split('VmRSS:')[1].split('\n')[0][:-3]

    return int(memusage.strip())


def main(args):
    n_chunks = args.n_chunks
    chunk_folder = args.chunk_folder
    if chunk_folder[-1] != '/':
        chunk_folder += '/'

    #group all chunk level ranking in a single ranking file
    frames = []
    for i in range(n_chunks):
        chunk_filename = 'chunk_' + str(i) + '_OUT.pkl'
        chunk_pathname = chunk_folder+chunk_filename
        chunk_out = load_data(filename=chunk_pathname)
        chunk_out.dropna(axis=1, how="all", inplace=True)
        print(chunk_out.size)
        print(chunk_out.head())
        frames.append(chunk_out)

    df = pd.concat(frames)
    print(df.size)
    print(df.head())
        #print('chunk ', str(i), 'Memory (GB) : ', getCurrentMemoryUsage()/(2**20))
    final_pathname = chunk_folder+'merged_OUT.csv'
    #print('before gc Memory (GB) : ', getCurrentMemoryUsage() / (2 ** 20))
    gc.collect()
    #print('after gc Memory (GB) : ', getCurrentMemoryUsage() / (2 ** 20))
    # drop all entirely nan columns
    df.dropna(axis=1, how="all", inplace=True)

    df.to_csv(final_pathname)
    #print('chunk ', str(i), 'Memory (GB) : ', getCurrentMemoryUsage() / (2 ** 20))

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--n_chunks', '-n', required=False, type=int, default=1,
                        help='number of chunk lists to create')
    parser.add_argument('--chunk_folder', '-c', required=False, type=str, default=1,
                        help='folder where _OUT chunks are')

    args = parser.parse_args()
    main(args)