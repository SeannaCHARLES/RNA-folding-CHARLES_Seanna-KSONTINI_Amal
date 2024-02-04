import pandas as pd 
import math
import matplotlib.pyplot as plt
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PyPDF2 import PdfMerger
import os 
import csv
#from gibbs_calc import calc_gibs
def creation_csv(score_dict): 
    with open('Final_res.csv', 'w', newline='') as csvfile:
    # Créer un objet writer CSV
        csvwriter = csv.writer(csvfile)

    # Écrire l'en-tête avec les couples de NU de 0 à 20
        entete = ['Nucleotide pairs'] + [str(i) + 'A' for i in range(21)]
        csvwriter.writerow(entete)

    # Parcourir chaque couple de NU et écrire les données dans le fichier CSV
        for couple_nu, valeurs in score_dict.items():
            ligne = [couple_nu] + [valeurs.get(i, [0, 0, 0])[2] for i in range(21)]
            csvwriter.writerow(ligne)
def creation_score_file(score_dict):
    for key, values in score_dict.items():
        with open(f"Result_file_pairs_{key}.pdf", 'wb') as res:
            pdf_canvas = canvas.Canvas(res)
            title = f'For the pairs of nucleotide : {key}'
            pdf_canvas.drawString(100, pdf_canvas._pagesize[1] - 50, title)

            y_position = pdf_canvas._pagesize[1] - 70  

            for key2, values in values.items():
                if y_position-90 < 30:
                    pdf_canvas.showPage()  # Passer à une nouvelle page
                    y_position = pdf_canvas._pagesize[1] - 30  # Réinitialiser la position y

                pdf_canvas.drawString(100, y_position, f'\t for the distance of : {key2} :')
                y_position -= 20  
                pdf_canvas.drawString(100, y_position, f'\t \t The observed probability = {values[0]}')
                y_position -= 20  
                pdf_canvas.drawString(100, y_position, f'\t \t The reference frequency = {values[1]}')
                y_position -= 20  
                pdf_canvas.drawString(100, y_position, f'\t \t The score = {values[2]}')
                y_position -= 30  
            pdf_canvas.save()
        merger = PdfMerger()
 

        pdfs = [f'histogram_Distribution_{key}.pdf', f'Log_ratio_{key}.pdf', f'Result_file_pairs_{key}.pdf']
 
        for pdf in pdfs:
            merger.append(pdf)
        merger.write(f"{key}.pdf")
        merger.close()
        for pdf in pdfs : 
            os.remove(pdf)



def Grap_log_ratio(dict_NN_dist,counts) :
    for key, values in dict_NN_dist.items():
        plt.figure(figsize=(8, 4))
        log_ratios = [math.log(value / counts[key]) for value in values]
        plt.hist(log_ratios, bins='auto', alpha=0.7)
        plt.xlabel(f'Log ratio log(distance/nb of apparition {key})')
        plt.ylabel('Frequency')
        plt.title(f'Log ratio distribution for {key}')
        plt.savefig(f'Log_ratio_{key}.pdf') 
        plt.close()
def Grap_distribution(dict_NN_dist) :
    for key, values in dict_NN_dist.items():
        plt.figure(figsize=(8, 4))
        plt.hist(values, bins='auto', alpha=0.7)
        plt.xlabel('Distance values')
        plt.ylabel('Frequency')
        plt.title(f'Ditribution histogram for {key}')
        plt.savefig(f'histogram_Distribution_{key}.pdf')  
        plt.close()
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
    return(NN_dist_A,R,counts)

def Graph_pairs_distribution(counts):
    plt.bar(counts.keys(), counts.values())
    plt.xlabel('Nucleotide couple')
    plt.ylabel('Number of apparitions')
    plt.title('Number of time a nucleotide couple appears in the sequence')
    plt.savefig(f'Number_of_time_a_nucleotide_couple_appears_in_the_sequence_chainA.pdf')  
    plt.close()

def Score (counts,R) :
    score_dict={}
    for key, values in R.items() : 
        for key2,values2 in values.items() :
        #print(key2, values2)
            obs_prob=values2/counts[key2]
            ref_freq=len(values)/20
            pseudo_en=-math.log(obs_prob/ref_freq)
            if key2 not in score_dict :
                score_dict[key2]={}
            if key not in score_dict[key2] : 
                score_dict[key2][key]=[obs_prob,ref_freq,pseudo_en]
    return(score_dict)

def main():
    Main_dict,R_dict,counts=parse_pdb_file("2jyf.pdb")
    Grap_log_ratio(Main_dict,counts)
    Grap_distribution(Main_dict)
    Graph_pairs_distribution(counts)
    Score_dict=Score(counts,R_dict)
    creation_score_file(Score_dict)
    creation_csv(Score_dict)
    #calc_gibs(Main_dict)
    #calc_gibs
main()