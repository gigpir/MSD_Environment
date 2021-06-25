#!/bin/bash
#SBATCH --job-name=evaluate_terms_intersection.py
#SBATCH --mail-type=ALL
#SBATCH --mail-user=luigi.pirisi@studenti.polito.it
#SBATCH --partition=global
#SBATCH --time=10:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#SBATCH --output=./LOGS/evaluate_terms_intersection.log
#SBATCH --mem-per-cpu=100M

#---- load python3 module
module load singularity/3.2.1

pwd
#mpiexec -n $SLURM_NTASKS

cd /home/crottondi/PIRISI_TESI/MSD_Environment/PYTHON_PROJ/5_EVAL

singularity exec /home/crottondi/PIRISI_TESI/singularity/projEnv_v2.img \
python3 /home/crottondi/PIRISI_TESI/MSD_Environment/PYTHON_PROJ/5_EVAL/evaluate_terms_intersection.py \
--distances /home/crottondi/PIRISI_TESI/MSD_Environment/FULL_PKL/distances_m3_bivariate_hungarian.pkl \
--ground_truth /home/crottondi/PIRISI_TESI/MSD_Environment/FULL_PKL/ground_truth.pkl \
--heatmaps /home/crottondi/PIRISI_TESI/MSD_Environment/FULL_PKL/heatmaps_m3.pkl \
--names /home/crottondi/PIRISI_TESI/MSD_Environment/FULL_PKL/names.pkl \
--ranking /home/crottondi/PIRISI_TESI/MSD_Environment/FULL_PKL/max_length_ranking_m3_bivariate_hungarian.pkl \
--output_folder /home/crottondi/PIRISI_TESI/MSD_Environment/FULL_OUTPUT/BIV_HUN_HISTOGRAMS \
--artists_pkl /home/crottondi/PIRISI_TESI/MSD_Environment/FULL_PKL/artists_m3_hm.pkl \
--terms /home/crottondi/PIRISI_TESI/MSD_Environment/FULL_PKL/terms_per_artist.pkl
