# Creation of an objective function for the RNA folding problem
## Aim of this repository

This repository has been created to answer this question For a given ribonucleotide chain, the RNA folding problem consists in finding the native fold among the astronomically large number of possible conformations. The native fold being the one with the lowest Gibbs free energy, the objective function should be an estimator of this energy.

## Method 

To accomplish the objective, a statistical training of an objective function will be performed using the frequency distribution of distances associated with the C3 atom of nucleotides in a training set (n=10 base pairs).

We consider the following base pairs : AA, AU, AC, AG, UU, UC, UG, CC, CG, GG. 
Only C3 atoms, interchain distances and residus separated by at least 3 positions on the sequence are taken into account 
We also consider 30 distance intervals ranging from 1 to 20 Å

## Installation

Run the following commands 

```
git clone https://github.com/SeannaCHARLES/RNA-folding-CHARLES_Seanna-KSONTINI_Amal

```

## Description of Scripts

- training.py : Create one pdf files for each nucleotide couple and a csv files (resuming all the scores per couples and distances)

- Plotting.R : plots the results from training.py with the score as a function of the distance 

- plotting.py : plots the results from training.py with the score as a function of the distance 

- gibbs_calc.py : Create a csv files that resume all the predicted scores per nucleotid couple and distances


## Launching Scripts
```
python3 Srcipts/training.py  # lunches statistical training on ten base pairs 

python3 Sripts/plotting.py

python3 Sripts/gibbs_calc.py  

## Training structures
....;

## Results

- pdf files that resume all the calculated scrores and graph made for each nucleotides couple
- CSV files that represents the differents scores for each nucleotide couple and ditances for the taining and prediction
- Plots that represents the profiles of each RNA sequence


