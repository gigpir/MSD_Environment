#!/bin/bash
#SBATCH --job-name=build_terms_and_terms_occurrences
#SBATCH --mail-type=ALL
#SBATCH --mail-user=luigi.pirisi@studenti.polito.it
#SBATCH --partition=global
#SBATCH --time=3:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --output=build_terms_and_terms_occurrences.log
#SBATCH --mem-per-cpu=100M

#---- load python3 module
module load singularity/3.2.1

pwd
#mpiexec -n $SLURM_NTASKS

cd /home/crottondi/PIRISI_TESI/MSD_Environment/PYTHON_PROJ/4_TO_PKLS

singularity exec /home/crottondi/PIRISI_TESI/singularity/projEnv_v2.img \
python3 /home/crottondi/PIRISI_TESI/MSD_Environment/PYTHON_PROJ/4_TO_PKLS/build_terms_and_terms_occurrences.py \
--distances /home/crottondi/PIRISI_TESI/MSD_Environment/FULL_PKL/distances_m3_bivariate_hungarian.pkl \
--ground_truth /home/crottondi/PIRISI_TESI/MSD_Environment/FULL_PKL/ground_truth.pkl \
--heatmaps /home/crottondi/PIRISI_TESI/MSD_Environment/FULL_PKL/heatmaps.pkl \
--names /home/crottondi/PIRISI_TESI/MSD_Environment/FULL_PKL/names.pkl \
--ranking /home/crottondi/PIRISI_TESI/MSD_Environment/FULL_PKL/max_length_ranking_m3_bivariate_hungarian.pkl \
--output_folder /home/crottondi/PIRISI_TESI/MSD_Environment/FULL_OUTPUT \
--artists_pkl /home/crottondi/PIRISI_TESI/MSD_Environment/FULL_PKL/artists_m3_hm.pkl
