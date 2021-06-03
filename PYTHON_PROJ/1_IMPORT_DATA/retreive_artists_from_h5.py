import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '/home/crottondi/PIRISI_TESI/MSD_Environment/PYTHON_PROJ')

from primary.data_io import retrieve_artist_dict, save_data
import os
import argparse


def main(args):
    input_folder = args.i_path

    output_filename = os.path.join(args.o_path, args.o_name)

    artists = retrieve_artist_dict(basedir=input_folder)

    save_data(dict=artists, filename=output_filename)

    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--i_path', required=True, type=str, help='path to data directory /data of MSD')
    parser.add_argument('--o_path', required=True, type=str, help='path where MSD pkl will be saved')
    parser.add_argument('--o_name', required=True, type=str, help='output filename')
    args = parser.parse_args()

    main(args)
