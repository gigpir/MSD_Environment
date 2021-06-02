#!/bin/bash
#SBATCH --job-name=1_IMPORT
#SBATCH --mail-type=ALL
#SBATCH --mail-user=luigi.pirisi@studenti.polito.it
#SBATCH --partition=global
#SBATCH --time=160:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=32
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --output=1_IMPORT.log
#SBATCH --mem-per-cpu=100M

#---- load python3 module
module load singularity/3.2.1

pwd
#mpiexec -n $SLURM_NTASKS

cd /home/crottondi/PIRISI_TESI/MSD_Environment/PYTHON_PROJ/1_IMPORT_DATA

singularity exec /home/crottondi/PIRISI_TESI/singularity/projEnv_v2.img \
python3 /home/crottondi/PIRISI_TESI/MSD_Environment/PYTHON_PROJ/1_IMPORT_DATA/retreive_artists_from_h5.py \
--i_path /home/crottondi/PIRISI_TESI/MSD_FULL/data \
--o_path /home/crottondi/PIRISI_TESI/MSD_Environment/FULL_PKL \
--o_name artists.pkl