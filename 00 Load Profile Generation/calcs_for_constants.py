'''
Author: Gabriella Vidgen
Date: 4 May 2023

Functions to print outputs to copy-paste into constants1.py to reduce the 
runtime of charge_profile_sorting6.py
'''

import pandas as pd
import numpy as np
import datetime

solar_csv = 'QLD_solar_var_timestamps.csv'

def solar_months(solar_csv):
    df = pd.read_csv(solar_csv)

    # extract month and create new column
    df['month'] = pd.DatetimeIndex(df['time'], dayfirst=True).month
    
    month_averages = []
    for i in range(1, 13):
        month_data = df.loc[df['month']==i]
        month_mean = month_data['electricity'].mean()
        month_averages.append(month_mean)

    # normalise month averages to get scales
    month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    avg = np.mean(month_averages)

    month_scales = []
    for num, day in zip(month_averages, month_days):
        month_scales.append((day/sum(month_days)) * (num/avg) * 12)

    print(month_scales)
    print(sum(month_scales))

def weekday_weekend_ratio(year, count=False, ratio=False):
    # GET TOTAL NUMBER OF WEEKDAYS AND WEEKENDS FOR YEAR
    start_date = datetime.date(year, 1, 1)
    end_date = datetime.date(year, 12, 31)
    weekday_count = sum(1 for i in range((end_date - start_date).days + 1) 
                        if (start_date + datetime.timedelta(i)).weekday() < 5)
    weekend_count = (end_date - start_date).days + 1 - weekday_count

    # GET RATIO OF WEEKDAYS AND WEEKENDS FOR YEAR
    weekday_ratio = weekday_count/(weekday_count + weekend_count)
    weekend_ratio = 1 - weekday_ratio

    if count == True:
        print(weekday_count)
        print(weekend_count)
        return weekday_count, weekend_count
    
    elif ratio == True:
        print(weekday_ratio)
        print(weekend_ratio)
        return weekday_ratio, weekend_ratio

solar_months(solar_csv)
