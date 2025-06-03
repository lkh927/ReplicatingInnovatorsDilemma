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

* Original MATLAB code          Original unedited MATLAB data and programs from Igami (2017). See Readme.pdf for overview.



0. Prep 
This folder contains the Matlab data file 'Data.mat' and the Python notebook 'Conversion.ipynb'. Everything in this folder was written by Knippel and serves the purpose of converting the data variables contained the .mat files into .csv files to use in following folders

1. Summary Statistics
Herein lies a notebook titled 'Summary Statistic.ipynb', and the code was written equally by Knippel and Abildskov (respectively authors of the figures of quality and market structure and of shipment and average price). These figures are based on the data in the folder titled 'Data', which houses the csv-files from the .mat conversion in folder 0.

2. Supply
Contains two .py-files titled 'Supply.py' and 'CheckPi.pi' as well as the notebook 'Supply.ipynb'. This is translated code, based on the original Matlab code by Igami, where the 'Supply.py' file, translated by Knippel, houses all of the original first-order-conditions (FOC.m, FOC_001.m, FOC_010.m, FOC_011.m, FOC_100.m, FOC_101.m, FOC_110.m), all of the non-linear constraints (nonlcon.m, nonlcon_001.m, nonlcon_010.m, nonlcon_011.m, nonlcon_100.m, nonlcon_101.m, nonlcon_110.m) and the 'FindMC.m' in a Python class. The 'Supply.ipynb' is the Python-translated version of 'FindPi.m'. The 'CheckPi.pi' is a translation of the Matlab code with the same name, and was translated by Abildskov.

3. Maximum Likelihood
This folder contains two Matlab datasets: CheckPi.mat and Data.mat. From CheckPi.mat, Pi (per period profits) are imported, where other relevant data variables are important from the 'Data' folder in (1). This folder futher contains several .py-files and one notebook, all of which are translations from Igami's original code, where fun1-fun13 has been translated from C and Likelihood has been translated from Matlab. The MLEstimation.ipynb is the translated version of Igami's 'MLEstimation.m', and it draws on all of the .py-files.

4. Simulation
As we were not succesful in replicating Igami's original results using our translated Python code, we opted for replicating the results running his original (slighty modified) code in Matlab. The resulting estimated model - which is equal to the estimated model he presents on page 829 - can be found in the 'PostEstimation.mat' data file. Using this Matlab data file, we can replicate his figure on the aforementioned page. Further, two other Matlab data files can be found, which are the results of a manual change in the alpha-parameters in Matlab and then running the original code on this basis. The corresponding figures of all three estimated models can be found in the 'Figures.ipynb' notebook.

* Altered MATLAB code
This subfolder contains the necessary subfolders to run the original 


* Original MATLAB code
