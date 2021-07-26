for i in {0..29}
do 
    sed -e 's/{NUMBER}/'$i'/g' 1_build_distances_chunk_pd_version.sbatch > tmp.sbatch
    sbatch tmp.sbatch
done

rm tmp.sbatch
