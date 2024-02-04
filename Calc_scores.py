import pandas as pd
#This file contains all the function that calculate the differents score
def range_(pairs) : 
   
    score_file=pd.read_csv("final_res.csv",sep=",")
    ligne=score_file[score_file['Nucleotide pairs'] == pairs]
    val_min = float(ligne['0A'].min())
    val_max = float(ligne['20A'].max())
    
    return(val_min,val_max)

def calc_gibbs(R) :
    score_dist={}
    for key,values in R.items():
        for key2, values2 in values.items():
            max_v,min_v=range_(key2)
            gibbs=float(min_v + ((values2 - 1) / (20 - 1)) * (max_v - min_v))
            if key2 not in score_dist : 
                score_dist[key2]={}
            if key not in score_dist[key2]:
                score_dist[key2][key]=gibbs
    return(score_dist)