#!/bin/bash
#SBATCH --job-name=build_distances_chunk_{NUMBER}
#SBATCH --mail-type=ALL
#SBATCH --mail-user=luigi.pirisi@studenti.polito.it
#SBATCH --partition=global
#SBATCH --time=15:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=32
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --output=./LOGS/build_distances_chunk_{NUMBER}.log
#SBATCH --mem=300gb

#---- load python3 module
module load singularity/3.2.1

pwd
#mpiexec -n $SLURM_NTASKS

cd /home/crottondi/PIRISI_TESI/MSD_Environment/PYTHON_PROJ/4_TO_PKLS

singularity exec /home/crottondi/PIRISI_TESI/singularity/projEnv_v2.img \
python3 /home/crottondi/PIRISI_TESI/MSD_Environment/PYTHON_PROJ/4_TO_PKLS/1_build_distances_chunk.py \
--input_pkl /home/crottondi/PIRISI_TESI/MSD_Environment/FULL_PKL/artists_m3_hm.pkl \
--metric bipartite_hungarian \
--input_chunk /home/crottondi/PIRISI_TESI/MSD_Environment/FULL_PKL/CHUNKS/chunk_{NUMBER}.pkl \
--output_path /home/crottondi/PIRISI_TESI/MSD_Environment/FULL_OUTPUT/CHUNK_OUT/