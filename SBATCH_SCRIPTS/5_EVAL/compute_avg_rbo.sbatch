#!/bin/bash
#SBATCH --job-name=evaluate_terms_intersection_{MODE}.py
#SBATCH --mail-type=ALL
#SBATCH --mail-user=luigi.pirisi@studenti.polito.it
#SBATCH --partition=global
#SBATCH --time=24:30:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --output=./LOGS/evaluate_terms_intersection_{MODE}.log
#SBATCH --mem-per-cpu=100M

#---- load python3 module
module load singularity/3.2.1

pwd
#mpiexec -n $SLURM_NTASKS

cd /home/crottondi/PIRISI_TESI/MSD_Environment/PYTHON_PROJ/5_EVAL

singularity exec /home/crottondi/PIRISI_TESI/singularity/projEnv_v2.img \
python3 /home/crottondi/PIRISI_TESI/MSD_Environment/PYTHON_PROJ/5_EVAL/compute_avg_rbo.py \
--ground_truth /home/crottondi/PIRISI_TESI/MSD_Environment/FULL_PKL/ground_truth.pkl \
--ranking /home/crottondi/PIRISI_TESI/MSD_Environment/FULL_PKL/max_length_ranking_{MODE}.pkl \
