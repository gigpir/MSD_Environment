#!/bin/bash
#SBATCH --job-name=3_build_names_heatmap_gt{NUMBER}
#SBATCH --mail-type=ALL
#SBATCH --mail-user=luigi.pirisi@studenti.polito.it
#SBATCH --partition=global
#SBATCH --time=160:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=32
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --output=./LOGS/3_build_names_heatmap_gt{NUMBER}.log
#SBATCH --mem-per-cpu=100M

#---- load python3 module
module load singularity/3.2.1

pwd
#mpiexec -n $SLURM_NTASKS

cd /home/crottondi/PIRISI_TESI/MSD_Environment/PYTHON_PROJ/4_TO_PKLS

singularity exec /home/crottondi/PIRISI_TESI/singularity/projEnv_v2.img \
python3 /home/crottondi/PIRISI_TESI/MSD_Environment/PYTHON_PROJ/4_TO_PKLS/3_build_names_heatmap_gt.py \
--input_pkl /home/crottondi/PIRISI_TESI/MSD_Environment/FULL_PKL/artists_m{NUMBER}_hm.pkl \
--output_path /home/crottondi/PIRISI_TESI/MSD_Environment/FULL_PKL \
--note _{NUMBER}
