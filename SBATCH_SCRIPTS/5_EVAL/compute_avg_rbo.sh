
mode=( "m3_bivariate_hungarian" "m3_cc_peak_1" "m2_bivariate_hungarian" "m2_cc_peak_1" )

for i in ${mode[*]} 
do  
    sed -e 's/{MODE}/'$i'/g' compute_avg_rbo.sbatch > tmp.sbatch
    sbatch tmp.sbatch
    
done

rm tmp.sbatch 