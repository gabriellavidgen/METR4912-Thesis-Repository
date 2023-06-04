# METR4912-Thesis-Repository
All scripts and files used to manipulate input data, create GenX cases, and process output data are included here.

This repository contains three folders:

1. 00 Load Profile Generation
2. 01 GenX Cases
3. Results Processing


# 00 Load Profile Generation Folder:

The Load Profile Generation folder contains all CSV files and scripts that were used to generate the contents of the
Load_data.csv files. No CSV files should need to be altered in any way.

To generate the load profiles, the scripts have to be run in a very particular order. Calculations were split into
various different scripts to reduce computation time. The workflow is as follows:

1. Run qld_loads_gen.py.
2. Run calcs_for_constants.py and copy the printed outputs.
3. Paste the printed outputs into constants.py
4. Select the coordinated charging profile and percentage in constants.py
5. Run charge_profile_sorting.py


# 01 GenX Cases Folder:

Thie GenX cases folder provides all of the files used to run each of the simulations used in my thesis report. The 
file structure is such that each of the GenX cases are ready to be run as all relevant file fields are populated.

The only input file that differs between the GenX cases is the Load_data.csv file.

The results of running the GenX simulations are also included in their respective GenX case folders.


# 02 Results Processing Folder:

The Results processing folder contains all CSV files and scripts that were used to produce the figures in the 
"Results and Discussion" section of my thesis, in addition to slider widgets that were used in my demonstration.

If the user wishes to use these scripts for different GenX results data, they simply need to populate the 
Results1 and Results2 folders with their output data and then run the scripts as usual.
