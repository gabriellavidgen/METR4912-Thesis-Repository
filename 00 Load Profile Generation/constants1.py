'''
Author: Gabriella Vidgen
Date: 4 May 2023

Constants for importing into charge_profile_sorting6.py
'''

todays_date = '230518' # YYMMDD

# IMPORTED FILE NAMES
weekday_csv = "2040_weekday_residential_profiles2.csv" # ALTER
weekend_csv = "2040_weekend_residential_profiles2.csv" # ALTER
percentages_csv = "230504_percentages.csv"
# percentages_csv = "CSIRO_original_percentages.csv"
total_qld_loads = "QLD_loads_2050_no_res_EVs1.csv" # ALTER

percent_flex = 50 # ALTER

# VALUES SPECIFIC TO 2050
year = 2050
total_GWh = 9545    
vehicle_sizes_GWh = {"Small": 2623, "Medium": 3418, "Large": 3504}

# From calcs_for_constants.py
weekday_count = 260
weekend_count = 105
weekday_ratio = 0.7123287671232876
weekend_ratio = 0.28767123287671237

# GENERAL VALUES
month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# From calcs_for_constants.py
solar_scales = [1.0933332601166563, 0.9753339063066112, 0.9046930771032093, 
                0.9741283310496434, 0.8881737556552943, 0.7928392166762441, 
                0.9548332460832463, 1.0644170965141648, 1.101801691189991, 
                1.094491788534328, 1.0844649309093028, 1.065352152445179]

# EXPORTING FILENAME
export_csv = f"{todays_date}_{year}_loads_{percent_flex}_flex.csv"
# export_csv = f"{year}_res_EV_loads_{percent_flex}2.csv"


