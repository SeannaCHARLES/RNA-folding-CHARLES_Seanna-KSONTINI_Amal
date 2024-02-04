import pandas as pd
import math
import csv
def range_(pairs) : 
   
    score_file=pd.read_csv("final_res.csv",sep=",")
    ligne=score_file[score_file['Nucleotide pairs'] == pairs]
    val_min = float(ligne['0A'].min())
    val_max = float(ligne['20A'].max())
    
    return(val_min,val_max)



def parse_pdb_file(pdb_path) :
    
    total=0
    NN_dist_A={}
    R={}
    with open(pdb_path,'r') as pdb_file : 
        kept_lines=[line.strip().split()for line in pdb_file if line.startswith("ATOM")and "C3'" in line]

   
    for i in range(0,len(kept_lines)-4): 
        for j in range(i+4,len(kept_lines)) : 
            NN = str(kept_lines[i][3])+str(kept_lines[j][3])
            x1=float(kept_lines[i][6])
            y1=float(kept_lines[i][7])
            z1=float(kept_lines[i][8])

            x2=float(kept_lines[j][6])
            y2=float(kept_lines[j][7])
            z2=float(kept_lines[j][8])

            dist=round(math.sqrt((x2-x1)**2+(y2-y1)**2+(z2-z1)**2))
     
            if kept_lines[j][4]==kept_lines[i][4]=="A" :
                if NN not in NN_dist_A : 
                    NN_dist_A[NN]=[]
               
                if dist <=20 and dist>0:
                    NN_dist_A[NN].append(dist)
                    if dist not in R : 
                        R[dist]={}
                    if NN not in R[dist] :
                        R[dist][NN]=0
                    R[dist][NN]+=1
                    total+=1
    counts = {key: (len(values))/total for key, values in NN_dist_A.items()}
    return(NN_dist_A,counts,R)

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

def creation_csv(score_dict): 
    with open('Final_res_pred.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)

        entete = ['Nucleotide pairs'] + [str(i) + 'A' for i in range(21)]
        csvwriter.writerow(entete)

        for couple_nu, valeurs in score_dict.items():
            ligne = [couple_nu] + [valeurs.get(i,0) for i in range(21)]
            csvwriter.writerow(ligne)
            
dict_,count,R=parse_pdb_file("2jyf.pdb")
score=calc_gibbs(R)
creation_csv(score)
