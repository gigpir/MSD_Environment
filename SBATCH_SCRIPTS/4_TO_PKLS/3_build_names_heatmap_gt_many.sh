for i in {0..3}
do 
    sed -e 's/{NUMBER}/'$i'/g' 3_build_names_heatmap_gt.sbatch > tmp.sbatch
    sbatch tmp.sbatch
done

rm tmp.sbatch