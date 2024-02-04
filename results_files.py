import csv
# This file contains all the script that create a results files (csv or pdf)
def creation_csv(score_dict): 
    with open('Final_res.csv', 'w', newline='') as csvfile:

        csvwriter = csv.writer(csvfile)


        entete = ['Nucleotide pairs'] + [str(i) + 'A' for i in range(21)]
        csvwriter.writerow(entete)


        for couple_nu, valeurs in score_dict.items():
            ligne = [couple_nu] + [valeurs.get(i, [0, 0, 0])[2] for i in range(21)]
            csvwriter.writerow(ligne)

def creation_csv(score_dict): 
    with open('Final_res_pred.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)

        entete = ['Nucleotide pairs'] + [str(i) + 'A' for i in range(21)]
        csvwriter.writerow(entete)

        for couple_nu, valeurs in score_dict.items():
            ligne = [couple_nu] + [valeurs.get(i,0) for i in range(21)]
            csvwriter.writerow(ligne)