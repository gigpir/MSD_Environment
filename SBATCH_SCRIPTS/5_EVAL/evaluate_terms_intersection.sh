mto=(100 200 400 800 1600)
md=( "NORM_STD" "NORM_OTHER" "NOT_NORM" )
vls=( "-1" "500")

for i in ${mto[*]} 
do  
    for j in ${md[*]} 
    do    
        for k in ${vls[*]} 
        do 
        rm tmp.sbatch tmp1.sbatch tmp2.sbatch 
        sed -e 's/{MTO}/'$i'/g' evaluate_terms_intersection_cc_peak_1.sbatch > tmp.sbatch
        
        sed -e 's/{MD}/'$j'/g' tmp.sbatch > tmp1.sbatch
        
        sed -e 's/{VLS}/'$k'/g' tmp1.sbatch > tmp2.sbatch
        
        sbatch tmp2.sbatch

        done
    
    done
    
    
done

rm tmp.sbatch tmp1.sbatch tmp2.sbatch 