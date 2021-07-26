#!/bin/bash
#SBATCH --job-name=workbench_cc
#SBATCH --mail-type=ALL
#SBATCH --mail-user=luigi.pirisi@studenti.polito.it
#SBATCH --partition=global
#SBATCH --time=48:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --output=workbench.log
#SBATCH --mem-per-cpu=100M

#---- load python3 module
module load singularity/3.2.1

pwd
#mpiexec -n $SLURM_NTASKS

cd /home/crottondi/PIRISI_TESI/MSD_Environment/PYTHON_PROJ/TMP

singularity exec /home/crottondi/PIRISI_TESI/singularity/projEnv_v2.img \
python3 /home/crottondi/PIRISI_TESI/MSD_Environment/PYTHON_PROJ/TMP/workbench.py \
--distances /home/crottondi/PIRISI_TESI/MSD_Environment/FULL_PKL/distances_m2_bivariate_hungarian.csv \
--ground_truth /home/crottondi/PIRISI_TESI/MSD_Environment/FULL_PKL/ground_truth.pkl \
--heatmaps /home/crottondi/PIRISI_TESI/MSD_Environment/FULL_PKL/heatmaps_m2.pkl \
--names /home/crottondi/PIRISI_TESI/MSD_Environment/FULL_PKL/names.pkl \
--ranking /home/crottondi/PIRISI_TESI/MSD_Environment/FULL_PKL/max_length_ranking_m2_bivariate_hungarian.pkl \
--output_folder /home/crottondi/PIRISI_TESI/MSD_Environment/FULL_OUTPUT/M2/BIV_HUN \
--artists_pkl /home/crottondi/PIRISI_TESI/MSD_Environment/FULL_PKL/artists_m2_hm.pkl
