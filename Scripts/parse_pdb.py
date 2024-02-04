import math
# This file parse a pdb file
# This script select only the line starting with ATOM and has C3' in it
# With those lines the distance between all nucleotides seperated by at least 4 nucleotide is calculated

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
    counts = {key: (len(values)) for key, values in NN_dist_A.items()}
    return(NN_dist_A,R,counts,total)
