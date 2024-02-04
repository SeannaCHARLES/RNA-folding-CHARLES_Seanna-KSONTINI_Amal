from results_files import Graph_log_ratio,Graph_distribution, Graph_pairs_distribution,creation_score_file,creation_csv
from parse_pdb import parse_pdb_file
from Calc_scores import Score
# This file calls several function written in differents scripts 
# The result of this script is to have a pdf and a csv file 
# The pdf file has two graph and the list of all the calculate score per distance
def main():
    Main_dict,R_dict,counts=parse_pdb_file("2jyf.pdb")
    Graph_log_ratio(Main_dict,counts)
    Graph_distribution(Main_dict)
    Graph_pairs_distribution(counts)
    Score_dict=Score(counts,R_dict)
    creation_score_file(Score_dict)
    creation_csv(Score_dict,"train")
main()