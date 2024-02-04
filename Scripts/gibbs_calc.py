from results_files import creation_csv
from parse_pdb import parse_pdb_file
from Calc_scores import calc_gibbs
# This file calls several function that will predicted a score for any pdb file based on the training script result
# The result of this file is a csv file containing all the different score per nucleotide couples and distances

def main ():    
    dict_,count,R=parse_pdb_file("2jyf.pdb")
    score=calc_gibbs(R)
    creation_csv(score,"pred")
main()