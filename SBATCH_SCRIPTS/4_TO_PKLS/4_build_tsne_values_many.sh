for i in {0..3}
do 
    sed -e 's/{NUMBER}/'$i'/g' 4_build_tsne_values.sbatch > tmp.sbatch
    sbatch tmp.sbatch
done

rm tmp.sbatch