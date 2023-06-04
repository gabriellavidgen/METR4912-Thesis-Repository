'''
Author: Gabriella Vidgen
Date: 4 May 2023

Script to produce CSV files in the format that can be copy-pasted into
Load_Data.csv for a given flexible charging percentage.

JUST PRODUCE CSIRO PROFILES WITHOUT OVERALL LOADS FIRST
'''

from constants1 import *
import pandas as pd
import datetime
import math

def csv_to_size_categories(input_csv):
    # CONVERT HALF-HOURLY DATA TO HOURLY DATA
    df = pd.read_csv(input_csv)

    # Get python to recognise that the 1st column is time data
    df["Time"] = pd.to_datetime(df["Time"])
    df.set_index("Time", inplace=True)

    # Dataframe we work with from here is "hourly_data"
    hourly_data = df.resample('H').mean()
    hourly_data.reset_index(inplace=True)
    hourly_data["Time"] = hourly_data["Time"].dt.strftime("%H:00")

    # NORMALISE EACH CHARGING PROFILE
    norm_df = hourly_data.copy()

    # Normalised dataframe we work with from here is "norm_df"
    for i in range(1,norm_df.shape[1]):
        col_name = norm_df.columns[i]
        normalised_col = norm_df[col_name] / norm_df[col_name].sum()
        norm_df[col_name] = normalised_col / normalised_col.sum() 
    
    # SPLIT DATA INTO VEHICLE SIZE CATEGORIES
    sml_df = norm_df.filter(regex="Small")
    med_df = norm_df.filter(regex="Medium")
    lrg_df = norm_df.filter(regex="Large")

    return sml_df, med_df, lrg_df

def charge_type_percentages(month): # month:int. 1=jan, 12=dec
    percentages_df = pd.read_csv(percentages_csv)

    # Get the column name that matches the specified percent_flex value
    percent_col_name = percentages_df.filter(regex=str(percent_flex)).columns[0]

    percentage_col_dict = {}

    for index, row in percentages_df.iterrows():
        key = row['Charge Type']
        value = row[percent_col_name]
        # Format the value to display up to 8 decimal places
        formatted_value = '{:.8f}'.format(value)
        if not math.isnan(value):
            percentage_col_dict[key] = float(formatted_value)

    # Scale coordinated charging percentage depending on its month
    percentage_col_dict['Residential - Coordinated Charging'] *=\
            solar_scales[month-1]
    
    # Adjust other percentages based on scaled solar
    remaining_scale = 1 - percentage_col_dict['Residential - Coordinated Charging']
    static_sum = sum(list(percentage_col_dict.values())[:-1])
    
    for key in list(percentage_col_dict.keys())[:-1]:
        percentage_col_dict[key] *= remaining_scale / static_sum
    
    return percentage_col_dict

def superimposed_size_profile(size_df, day, month, size_res_GWh):
    # MULTIPLY EACH CHARGE PROFILE BY ITS PERCENTAGE (IN DECIMAL FORM)
    scaled_size_df = size_df.copy()

    percentage_dict = charge_type_percentages(month)

    # Percentage scaled dataframe we work with from here is "scaled_size_df"
    for col, percentage in zip(scaled_size_df.columns, percentage_dict.values()):
        scaled_size_df[col] = scaled_size_df[col] * percentage

    # SUPERIMPOSE ALL CHARGING PROFILES INTO 1 COLUMN
    superimposed_col = pd.Series([0] * 24)

    # Single column dataframe is "superimposed_col"
    for i in range(scaled_size_df.shape[1]):
        superimposed_col += scaled_size_df.iloc[:, i]

    # MULTIPLY SUPERIMPOSED PROFILE BY ITS POWER CONSUMPTION
    # Resulting dataframe represents a single day
    # GenX requires load inputs to be MW
    if day == "weekday":
        size_profile = superimposed_col.apply(lambda x: x * weekday_ratio * 
                                             size_res_GWh * 1000 / #GWh to MWh
                                             weekday_count)

    elif day == "weekend":
        size_profile = superimposed_col.apply(lambda x: x * weekend_ratio * 
                                             size_res_GWh * 1000 / #GWh to MWh
                                             weekend_count)
    return size_profile

def superimposed_day_profile(day, month):
    # COMBINE THE DAY CHARGING PROFILES FOR SML, MED, LRG VEHICLES
    superimposed_day = pd.Series([0] * 24)

    if day == "weekday":
        size_dfs = list(csv_to_size_categories(weekday_csv))

        for size_df, power in zip(size_dfs, vehicle_sizes_GWh.values()):
            superimposed_day += superimposed_size_profile(size_df, 
                                                          "weekday", month,
                                                          power)
    elif day == "weekend":
        size_dfs = list(csv_to_size_categories(weekend_csv))

        for size_df, power in zip(size_dfs, vehicle_sizes_GWh.values()):
            superimposed_day += superimposed_size_profile(size_df, 
                                                          "weekend", month,
                                                          power)            
    return superimposed_day

def month_profile_MW(month_int):
    # CONCATENATE EACH DAY'S PROFILE FOR A GIVEN MONTH
    start_date = datetime.date(year, month_int, 1)
    end_date = datetime.date(year, month_int, month_days[month_int-1])

    month_profile = []
    
    for i in range(0, (end_date - start_date).days + 1):
        date = start_date + datetime.timedelta(i)

        if date.weekday() < 5: # Monday = 0, Sunday = 6
            month_profile.append(list(superimposed_day_profile("weekday", 
                                                               month_int)))

        else:
            month_profile.append(list(superimposed_day_profile("weekend", 
                                                               month_int)))

    # Convert nested list -> flat list -> series -> dataframe
    flat_list = [item for sublist in month_profile for item in sublist]
    list_to_series = pd.Series(flat_list)
    
    month_profile_df = pd.DataFrame(list_to_series)

    return month_profile_df

def year_profile_MW():
    # CONCATENATE EACH MONTH'S PROFILE FOR THE YEAR
    year_profile = []

    for i in range(12):
        year_profile.append(month_profile_MW(i+1))

    year_profile_df = pd.concat(year_profile, ignore_index=True)
    year_profile_df.columns = ['Load (MW)']

    # COMBINE RES EV LOAD PROFILE WITH TOTAL QLD LOAD PROFILE
    qld_loads = pd.read_csv(total_qld_loads)
    year_profile_df += qld_loads
  
    # Export year dataframe to csv file
    year_profile_df.to_csv(export_csv, index=False)


if __name__ == "__main__":
    year_profile_MW()