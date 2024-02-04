import csv
import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PyPDF2 import PdfMerger
import matplotlib.pyplot as plt
import math
# This file contains all the script that create a results files (csv or pdf)
# The creation_csv function create a csv file containing all the different score per nucleotide couple and distance
# The creation score file function create a pdf file containg two graphs and the list of all calculated scores per distance. One file per nucleotide couple
# The grahp log ration create a graph that represents the distribution of log ration per pairs
# The Graph pairs distribution create a graph that represents the frequency of nucleotide couple in the sequence
# The Graph pairs distribution  create a graph that represents the frequency of each distance per nucleotide couple
def creation_csv(score_dict,type):
     with open(f'Results/Final_res_{type}.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)

        entete = ['Nucleotide pairs'] + [str(i) + 'A' for i in range(21)]
        csvwriter.writerow(entete)

        for couple_nu, valeurs in score_dict.items():
            if type=="pred" :
                ligne=[couple_nu] + [valeurs.get(i,0) for i in range(21)]
            else : 
                ligne=[couple_nu] + [valeurs.get(i, [0, 0, 0])[2] for i in range(21)]
            csvwriter.writerow(ligne)

def creation_score_file(score_dict):
    for key, values in score_dict.items():
        with open(f"Results/Result_file_pairs_{key}.pdf", 'wb') as res:
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
 

        pdfs = [f'Results/histogram_Distribution_{key}.pdf', f'Results/Log_ratio_{key}.pdf', f'Results/Result_file_pairs_{key}.pdf']
 
        for pdf in pdfs:
            merger.append(pdf)
        merger.write(f"{key}.pdf")
        merger.close()
        for pdf in pdfs : 
            os.remove(pdf)

def Graph_log_ratio(dict_NN_dist,counts) :
    for key, values in dict_NN_dist.items():
        plt.figure(figsize=(8, 4))
        log_ratios = [math.log(value / counts[key]) for value in values]
        plt.hist(log_ratios, bins='auto', alpha=0.7)
        plt.xlabel(f'Log ratio log(distance/nb of apparition {key})')
        plt.ylabel('Frequency')
        plt.title(f'Log ratio distribution for {key}')
        plt.savefig(f'Results/Log_ratio_{key}.pdf') 
        plt.close()
        
def Graph_distribution(dict_NN_dist) :
    for key, values in dict_NN_dist.items():
        plt.figure(figsize=(8, 4))
        plt.hist(values, bins='auto', alpha=0.7)
        plt.xlabel('Distance values')
        plt.ylabel('Frequency')
        plt.title(f'Ditribution histogram for {key}')
        plt.savefig(f'Results/histogram_Distribution_{key}.pdf')  
        plt.close()

def Graph_pairs_distribution(counts):
    plt.bar(counts.keys(), counts.values())
    plt.xlabel('Nucleotide couple')
    plt.ylabel('Number of apparitions')
    plt.title('Number of time a nucleotide couple appears in the sequence')
    plt.savefig(f'Results/Number_of_time_a_nucleotide_couple_appears_in_the_sequence_chainA.pdf')  
    plt.close()
