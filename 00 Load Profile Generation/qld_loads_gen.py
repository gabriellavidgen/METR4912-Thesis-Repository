'''
Generate the overall load profile for Queensland for the year 2050.
Start by generating the profile for 2022, then scale up.
'''
import os
import pandas as pd

folder_path = 'C:/Users/Gabriella Vidgen/OneDrive/UNI/Subjects/METR4912/00 Modelling/00 Input Generation/02 Load Profile Generation/2022 Loads'
assumed_res_ev_loads = "2050_res_EV_loads_CSIRO1.csv" # KEEP CONSTANT BETWEEN SCENARIOS!!

consumption_2050 = 109955.026 # GWh

def pre_process(filename): # input: folder_dir
    # Remove redundant columns
    df = pd.read_csv(filename) # Demand data is in MW for each 5 min interval
    df = df.drop(['REGION', 'RRP', 'PERIODTYPE'], axis=1)
    
    # Get python to recognise that the 1st column is time data
    df['SETTLEMENTDATE'] = pd.to_datetime(df['SETTLEMENTDATE'], format='%Y/%m/%d %H:%M:%S')
    df.set_index('SETTLEMENTDATE', inplace=True)

    # Resample the data to hourly intervals and calculate the mean of each hour
    df = df.resample("1H").mean() 

    # Remove the last row (next month's data)
    df = df.drop(df.index[-1])
    return df
    
def get_year():
    # Create an empty list to store the DataFrames
    dataframes = []

    # Iterate through each file in the directory
    for filename in os.listdir(folder_path):
        # Check if the file is a CSV file
        if filename.endswith(".csv"):
            # Read the CSV file into a DataFrame
            filepath = os.path.join(folder_path, filename)
            df = pre_process(filepath)
            # Append the DataFrame to the list
            dataframes.append(df)

    # Concatenate all the DataFrames into a single DataFrame
    year_df = pd.concat(dataframes, ignore_index=True)

    # Scale up 2022 data to get 2050 profile
    consumption_2022 = (year_df/1000).sum() # GWh
    scale = float(consumption_2050/consumption_2022) # ~2.09
    scaled_year_df = year_df.multiply(scale, axis=0)

    # Rename column to show units
    scaled_year_df = scaled_year_df.rename(columns={'TOTALDEMAND': 'Load (MW)'})

    # Subtract EV loads (CSIRO assumed loads)
    res_EV_loads = pd.read_csv(assumed_res_ev_loads)
    no_res_EV_year_df = scaled_year_df - res_EV_loads

    no_res_EV_year_df.to_csv('QLD_loads_2050_no_res_EVs2.csv', index=None) # ALTER

if __name__ == '__main__':
    get_year()