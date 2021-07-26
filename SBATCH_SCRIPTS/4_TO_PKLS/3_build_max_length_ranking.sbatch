#!/bin/bash
#SBATCH --job-name=3_build_max_length_ranking_m2_cc_p
#SBATCH --mail-type=ALL
#SBATCH --mail-user=luigi.pirisi@studenti.polito.it
#SBATCH --partition=global
#SBATCH --time=160:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=32
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --output=./LOGS/3_build_max_length_ranking_m2_cc_p.log
#SBATCH --mem=200G

#---- load python3 module
module load singularity/3.2.1

pwd
#mpiexec -n $SLURM_NTASKS

cd /home/crottondi/PIRISI_TESI/MSD_Environment/PYTHON_PROJ/4_TO_PKLS

singularity exec /home/crottondi/PIRISI_TESI/singularity/projEnv_v2.img \
python3 /home/crottondi/PIRISI_TESI/MSD_Environment/PYTHON_PROJ/4_TO_PKLS/3_build_max_length_ranking.py \
--distances /home/crottondi/PIRISI_TESI/MSD_Environment/FULL_PKL/distances_m2_cc_peak_1.csv \
--note m2_cc_peak_1
