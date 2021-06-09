# MSD_Environment

link repo: https://github.com/gigpir/MSD_Environment.git

## Elenco delle cartelle e descrizione

- ### FULL_OUTPUT 
  
  Destinata all'output relativo al lavoro sul dataset completo.
  
- ### SUBSET_OUTPUT
  
  Destinata all'output relativo al lavoro sul subset 1% reperibile all'indirizzo
  https://labrosa.ee.columbia.edu/~dpwe/tmp/millionsongsubset.tar.gz.
  
- ### FULL_PKL 
  
  Cartella atta a contenere i file `.pkl` relativi al dataset completo.
- ### SUBSET_PKL 
  
  Cartella atta a contenere i file `.pkl` relativi al dataset completo.
- ### PYTHON_PROJ 
  
  Cartella contente il progetto python.
- ### SBATCH_SCRIPTS 
  
  Cartella contente gli script `.sbatch` per sottomettere gli script del progetto
  python sul cluster HPC. La struttura di questa cartella ricalca quella della cartella 
  PYTHON_PROJ.

## Descrizione del progetto situato in PYTHON_PROJ

- ### 1_IMPORT_DATA
  
  Cartella contenente gli script atti ad importare il dataset tralasciando i campi non necessari, organizzarli in un dizionario
  di oggetti e serializzare il dizionario in un file `.pkl` (`artists.pkl`). 
  
- ### 2_PREPROCESSING

  Cartella contenente gli script atti a fare preprocessing, calcolare le coordinate t-SNE, calcolare le heatmap, 
  serializzare il dizionario aggiornato in un file `.pkl` (`artists_m{i}_hm.pkl`). In questa configurazione tutto il lavoro
  è svolto dall'unico script presente in questa cartella.

  - #### artist_m{i}_hm.pkl
    **TIPO:** Dizionario di oggetti `Artist` _(fare riferimento alla classe descritta nel file `primary/data_class.py`)_.
    Ad ogni oggetto della classe `Artist` è _opzionalmente_ associata una heatmap 20x20 accessibile tramite la proprietà `.tsne_heatmap`.
    Ad ogni oggetto della classe `Artist` è associato un dizionario di oggetti `Song` la cui chiave è l'id del brano.
    Ad ogni oggetto della classe `Song` è _opzionalmente_ associata una tupla contenente le coordinate tsne accessibile tramite la proprietà `.tsne[0]` o `.tsne[1]`
    Al variare della modalità m varia il modo in qui è stato calcolato t-SNE
    
    - `m0` media
    - `m1` media + varianza
    - `m2` media + varianza + derivate prime
    - `m3` media + varianza + derivate prime + derivate seconde  

- ### 3_GEN_CHUNKS
  
  Lo script presente in questa cartella suddivide la **lista** degli **id** del dataset in input 
  in _n_ chunk e li salva come `chunk_{i}.pkl` in un path specificato da linea di comando.
  
- ### 4_TO_PKLS
  
  Cartella contenente gli script per generare file `.pkl` derivati da `artist_m{i}_hm.pkl`.
  I file sono i seguenti:
  
  - #### distances_m{i}_cc_peak_1.pkl 
    **TIPO:** Pandas DataFrame.
    Contiene le distanze calcolate con il criterio
    che fa uso della cross correlazione considerando un solo picco.
    La funzione implementa la metrica è `compute_cross_correlation_distance`
    Per accedere alla distanza tra l'artista 'a' e l'artista 'b' digitare l'istruzione: `df['a']['b']` dopo aver caricato il file. 
  
  - #### distances_m{i}_cc_peak_2.pkl 
    **TIPO:** Pandas DataFrame.
    Contiene le distanze calcolate con il criterio
    che fa uso della cross correlazione considerando un solo picco e dividendo poi il valore dello shift per il picco stesso.
    La funzione implementa la metrica è `compute_cross_correlation_distance_normalized`
    Per accedere alla distanza tra l'artista 'a' e l'artista 'b' digitare l'istruzione: `df['a']['b']` dopo aver caricato il file.
  
  - #### max_length_ranking_m{i}\_cc_peak_1.pkl e max_length_ranking_m{i}_cc_peak_2.pkl
    **TIPO:** dizionario di ranking.
    **Chiave**: id artista.
    **Valore**: ranking, una lista ordinata di id artista 
    
  - #### ground_truth.pkl 
    **TIPO:** dizionario di ranking.
    **Chiave**: id artista.
    **Valore**: ranking, una lista ordinata di id artista 
  
  - #### heatmaps_m{i}.pkl
    **TIPO:** dizionario di tuple.
    **Chiave**: id artista.
    **Valore**: tupla contenente una matrice numpy 20x20 in posizione `0` e una lista in posizione `1`. 
    
    Ogni elemento della lista contiene a sua volta una lista formattata in questo modo: 
    
    `[<x_value> , <y_value>, <n_of_songs_in_that_cell>]`. 
    
     laddove la heatmap non sia presente per l'artista la tupla conterra due valori None.  
    
    ​	Esempio d'uso del dizionario: 
    
    ​	
    
    ```python
    tupla = heatmaps['artist_id']
    heatmap = tupla[0]
    list_heatmap_not_normalized = tupla[1]
    # oppure
    heatmap, list_heatmap_not_normalized  = tupla
    ```
    
  - #### names.pkl
    
    **TIPO:** dizionario di stringhe.
    **Chiave**: id artista.
    **Valore**: stringa corrispondente al nome dell'artista
    
  - #### tsne_values_m{i}.pkl
  
    **Descrizione**: contiene le coordinate t-SNE dei brani presenti nel dataset
  
    **TIPO:** dataframe Pandas.
  
    **Nome campi**: `<artist_id><song_id><tsne_0><tsne_1>`
  
    

Suggerimenti per eseguire il codice in locale: 

  - settare la working directory in PYTHON_PROJ.

  - Su MacOs usare un python3.7 non superiore (le versioni superiori non supportano la condivisione delle variabili globali tra processi) e usare pickle5 anziché pickle (è sufficiente digitare

    ```python
    import pickle5 as pickle
    ```

     nel file `PYTHON_PROJ/primary/data_io.py`). Non occorre modificare le funzioni `load_data` and `save_data`

  - Su Linux usare python3.8 non superiore.

  - I file .pkl possono essere aperti e chiusi utilizzando i wrapper `load_data` e `save_data` che si trovano nel file `primary/data_io.py`



## Script `.sbatch`

Gli script si trovano nella cartella `SBATCH_SCRIPTS` e ricalcano il progetto python in quanto a struttura e nomenclatura. 

Per sottomettere un job è sufficiente lanciare il seguente comando da terminale:

```bash
sbatch nome_script.sbatch
```

  ###### 

Gli script che lavorano su un chunk vengono generati a partire da una matrice nella quale il numero di chunk è sostituito dalla dicitura `{NUMBER}`. Uno script `.sh` si occupa di generare lo script  `.sbatch` a partire dalla matrice utilizzato le istruzioni qui sotto e lo sottomette automaticamente:

```bash
for i in {0..29}
do 
    sed -e 's/{NUMBER}/'$i'/g' 1_build_distances_chunk.sbatch > tmp.sbatch
    sbatch tmp.sbatch
done

rm tmp.sbatch
```

  I file `/home/crottondi/PIRISI_TESI/MSD_Environment/SBATCH_SCRIPTS/4_TO_PKLS/1_build_distances_chunk.sbatch` e `/home/crottondi/PIRISI_TESI/MSD_Environment/SBATCH_SCRIPTS/4_TO_PKLS/1_build_distances_many_chunks.sh` ne sono un esempio

