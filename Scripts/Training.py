from results_files import Grap_log_ratio,Grap_distribution, Graph_pairs_distribution,creation_score_file,creation_csv
from parse_pdb import parse_pdb_file
from Calc_scores import Score

def main():
    Main_dict,R_dict,counts=parse_pdb_file("2jyf.pdb")
    Grap_log_ratio(Main_dict,counts)
    Grap_distribution(Main_dict)
    Graph_pairs_distribution(counts)
    Score_dict=Score(counts,R_dict)
    creation_score_file(Score_dict)
    creation_csv(Score_dict)
main()