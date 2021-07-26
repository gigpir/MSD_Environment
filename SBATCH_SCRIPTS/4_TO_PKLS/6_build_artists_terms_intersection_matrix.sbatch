#!/bin/bash
#SBATCH --job-name=6_build_artists_terms_intersection_matrix
#SBATCH --mail-type=ALL
#SBATCH --mail-user=luigi.pirisi@studenti.polito.it
#SBATCH --partition=global
#SBATCH --time=3:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --output=./LOGS/6_build_artists_terms_intersection_matrix.log
#SBATCH --mem-per-cpu=100M

#---- load python3 module
module load singularity/3.2.1

pwd
#mpiexec -n $SLURM_NTASKS

cd /home/crottondi/PIRISI_TESI/MSD_Environment/PYTHON_PROJ/4_TO_PKLS

singularity exec /home/crottondi/PIRISI_TESI/singularity/projEnv_v2.img \
python3 /home/crottondi/PIRISI_TESI/MSD_Environment/PYTHON_PROJ/4_TO_PKLS/6_build_artists_terms_intersection_matrix.py \
--output_folder /home/crottondi/PIRISI_TESI/MSD_Environment/FULL_PKL \
--terms /home/crottondi/PIRISI_TESI/MSD_Environment/FULL_PKL/terms_per_artist.pkl

