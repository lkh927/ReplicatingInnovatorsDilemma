# ReplicatingInnovatorsDilemma
Written by Emma Knippel (lkh927) and Anna Abildskov (bvh632).

The code found in this zip folder contains a Python-translation of a part of Mitsuru Igami's MATLAB/C code used to produce the results of "Estimating the Inovator's Dilemma" (2017), as well as the full original code for comparison and the altered version of the MATLAB/C code for counterfactual analysis. 

The code is divided into seven subfolders:
0) Prep                         MATLAB data and Python program for initial data conversion. 

1) Summary Statistics           CSV Data folder and Python programmes for summary statistics.

2) Supply                       Python programmes for period profit optimization.

3) Maximum Likelihood           MATLAB data and Python programmes for maximum likelihood estimation.

4) Simulation                   MATLAB data and Python program for plotting simulated states

* Altered MATLAB code           MATLAB data and programs to replicate estimated model structure & run our counterfactual

* Original MATLAB code          Original unedited MATLAB data and programs from Igami (2017). 


0. Prep 
This folder contains the Matlab data file 'Data.mat' and the Python notebook 'Conversion.ipynb'. Everything in this folder was written by Knippel and serves the purpose of converting the data variables contained the .mat files into .csv files to use in following folders

1. Summary Statistics
Herein lies a notebook titled 'Summary Statistic.ipynb' and a py-file titled 'fun1.py', and the code was written equally by Knippel and Abildskov (respectively authors of the figures of quality and market structure and of shipment and average price). The notebook calls the py-file to produce a 2x2 figure based on the data in the folder titled 'Data', which houses the csv-files from the Data.mat conversion in folder 0.

2. Supply
Contains two .py-files titled 'Supply.py' and 'CheckPi.py' as well as the notebook 'Supply.ipynb'. 
This is translated code, based on the original MATLAB code by Igami, where the 'Supply.py' file, translated by Knippel, is a Class that houses all of the translated versions of the first-order-conditions (FOC, FOC_001, FOC_010, FOC_011, FOC_100, FOC_101, FOC_110), all of the non-linear constraints (nonlcon, nonlcon_001, nonlcon_010, nonlcon_011, nonlcon_100, nonlcon_101, nonlcon_110) and the optimization code to find profit-maximizing quantities. The 'CheckPi.py' file corrects unrealistic results in the profit maximization and was translated by Abildskov. The 'Supply.ipynb' is the Jupyter notebook that calls the two py-files to produce and save the final optimization results, created by Knippel.

3. Maximum Likelihood
This folder contains two MATLAB datasets: CheckPi.mat and Data.mat. From CheckPi.mat, Pi (optimal period profits) are imported, where other relevant data variables are imported from the 'Data' folder in (1). This folder futher contains several .py-files and one notebook, all of which are translations from Igami's original code, where fun1-fun13 has been translated from C and Likelihood has been translated from MATLAB. The MLEstimation.ipynb is the translated version of Igami's 'MLEstimation.m', and it draws on all of the .py-files. The code was partly translated by Abildskov and partly translated by Knippel.

4. Simulation
As we were not succesful in replicating Igami's original results using our translated Python code (time challenges), we opted for replicating the results running his original (slighty modified) code in MATLAB. See *Altered MATLAB code, subsection (02-04). The resulting estimated dataset - which is equal to the estimated model he presents on page 829 - can be found in the 'PostEstimation.mat' data file. Further, two other MATLAB data files can be found, which are the results of a manual change in the alpha_3-parameter in MATLAB and then running the original code on this basis. See *Altered MATLAB code, subsection 05. The corresponding figures of both estimated models can be found in the 'Figures.ipynb' notebook, which calls the py-file 'fun1.py', which is a simple plotting function.

* Altered MATLAB code
This subfolder contains the necessary MATLAB code with minor adjustments made by Abildskov and Knippel to reproduce the original estimated model in MATLAB (02_Supply, 03_Investment, 04_PostEstimation). It also contains the altered code for the counterfactual scenario where demand for capacity, alpha_3, is increased by 50 pct, necessary to produce a counterfactual estimated model (05_GreaterDemand).

* Original MATLAB code
This subfolder contains the untouched MATLAB code, downloaded directly from https://www.journals.uchicago.edu/doi/abs/10.1086/691524?mobileUi=0& for comparison to * Altered MATLAB code. See "Readme.pdf" in the folder for an overview.