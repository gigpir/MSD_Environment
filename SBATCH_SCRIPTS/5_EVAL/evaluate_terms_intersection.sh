vect=(100 200 400 800)

for i in ${vect[*]} 
do 
    sed -e 's/{VAR}/'$i'/g' evaluate_terms_intersection.sbatch > tmp.sbatch
    sbatch tmp.sbatch
done

rm tmp.sbatch