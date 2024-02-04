import pandas as pd
import math
import csv
from results_files import creation_csv
from parse_pdb import parse_pdb_file
from Calc_scores import calc_gibbs

def main ():    
    dict_,count,R=parse_pdb_file("2jyf.pdb")
    score=calc_gibbs(R)
    creation_csv(score,"pred")
main()