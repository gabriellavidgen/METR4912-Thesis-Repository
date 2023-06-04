# from constants import *
import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np

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

    # iterate over the column names
    for col_name1, col_name2, col_name3 in zip(sml_df.columns, med_df.columns, lrg_df.columns):
        # plot the values in the current column against the dataframe index
        sml_df[col_name1].plot(x=sml_df.index, y=col_name1)
        # med_df[col_name2].plot(x=med_df.index, y=col_name2)
        # lrg_df[col_name3].plot(x=lrg_df.index, y=col_name3)

        title = col_name1

        # split the string into a list using the ", " separator
        title_parts = title.split(", ")

        # select the last part of the list using negative indexing
        new_title = title_parts[-1]
                
        # set the x axis label
        plt.xlabel('Time')
        plt.xticks(sml_df.index[::2])
        
        # set the y axis label to the current column name
        plt.ylabel('Charging Density')

        # plt.legend(labels=['Small', 'Medium', 'Large'], loc='upper left')

        plt.title(new_title)
        
        # display the plot
        plt.show()

def compare_profiles(input_csv):
    # CONVERT HALF-HOURLY DATA TO HOURLY DATA
    df = pd.read_csv(input_csv)

    # Get python to recognise that the 1st column is time data
    df["Time"] = pd.to_datetime(df["Time"], format='%H:%M')
    df.set_index("Time", inplace=True)

    # Dataframe we work with from here is "hourly_data"
    hourly_data = df.resample('H').mean()
    hourly_data.reset_index(inplace=True)
    hourly_data["Time"] = hourly_data["Time"].dt.strftime("%H:00")

    # NORMALISE EACH CHARGING PROFILE
    norm_df = hourly_data.copy()
    norm_df.columns = norm_df.columns.str.replace('Coordinated Charging - ', '', regex=True)

    # Plot the DataFrame
    # norm_df.plot(x=norm_df.iloc[:, 0], y=norm_df.iloc[:, 1:], kind='line')
    norm_df.iloc[:, 1:].plot(color=['blue', 'magenta'])

    # Add labels and title
    plt.xlabel('Hour', fontsize=12)
    plt.ylabel('Charging Density', fontsize=12)
    plt.title('Comparison of Coordinated Charging Profiles', fontsize=14)
    plt.xticks(np.arange(0, 24, 2))

    # Display the plot
    plt.show()
 
def day_end(csv_1, csv_2):
    # CONVERT HALF-HOURLY DATA TO HOURLY DATA
    df1 = pd.read_csv(csv_1)
    df2 = pd.read_csv(csv_2)

    # Get python to recognise that the 1st column is time data
    df1["Time"] = pd.to_datetime(df1["Time"])
    df1.set_index("Time", inplace=True)
    df2["Time"] = pd.to_datetime(df2["Time"])
    df2.set_index("Time", inplace=True)

    # Dataframe we work with from here is "hourly_data"
    hourly_data1 = df1.resample('H').mean()
    hourly_data1.reset_index(inplace=True)
    hourly_data1["Time"] = hourly_data1["Time"].dt.strftime("%H:00")
    hourly_data2 = df2.resample('H').mean()
    hourly_data2.reset_index(inplace=True)
    hourly_data2["Time"] = hourly_data2["Time"].dt.strftime("%H:00")

    # NORMALISE EACH CHARGING PROFILE
    norm_df1 = hourly_data1.copy()
    norm_df2 = hourly_data2.copy()

    # Normalised dataframe we work with from here is "norm_df"
    for i in range(1,norm_df1.shape[1]):
        col_name1 = norm_df1.columns[i]
        normalised_col1 = norm_df1[col_name1] / norm_df1[col_name1].sum()
        norm_df1[col_name1] = normalised_col1 / normalised_col1.sum() 
    
    for i in range(1,norm_df2.shape[1]):
        col_name2 = norm_df2.columns[i]
        normalised_col2 = norm_df2[col_name2] / norm_df2[col_name2].sum()
        norm_df2[col_name2] = normalised_col2 / normalised_col2.sum() 

    # SPLIT DATA INTO VEHICLE SIZE CATEGORIES
    sml_df1 = norm_df1.filter(regex="Small")
    sml_df2 = norm_df2.filter(regex="Small")

    # iterate over the column names
    for col_name1, col_name2 in zip(sml_df1.columns, sml_df2.columns):
        # plot the values in the current column against the dataframe index
        sml_df1[col_name1].plot(x=sml_df1.index, y=col_name1)
        sml_df2[col_name2].plot(x=sml_df2.index, y=col_name2)

        title = col_name1

        # split the string into a list using the ", " separator
        title_parts = title.split(", ")

        # select the last part of the list using negative indexing
        new_title = title_parts[-1]
                
        # set the x axis label
        plt.xlabel('Time')
        plt.xticks(sml_df1.index[::2])
        
        # set the y axis label to the current column name
        plt.ylabel('Normalised Demand Load')

        plt.legend(labels=['Weekday', 'Weekend'], loc='upper left')

        plt.title(new_title)
        
        # display the plot
        plt.show()

def solar_plot():
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    solar_scales = [1.0933332601166563, 0.9753339063066112, 0.9046930771032093, 
                    0.9741283310496434, 0.8881737556552943, 0.7928392166762441, 
                    0.9548332460832463, 1.0644170965141648, 1.101801691189991, 
                    1.094491788534328, 1.0844649309093028, 1.065352152445179]
    
    fig, ax = plt.subplots()
    ax.bar(months, solar_scales)

    # Add a horizontal line at y=1
    ax.axhline(y=1, color='r', linestyle='--')
    ax.set_title('Solar Generation Scales for each Month of the Year')
    ax.set_xlabel('Month')
    ax.set_ylabel('Scale')
    ax.set_ylim(0.75, 1.15)
    plt.show()

if __name__ == "__main__":
    # compare_profiles('Coord Profiles.csv')
    # day_end(weekday_csv, weekend_csv)
    # solar_plot()
    csv_to_size_categories('2040_weekday_residential_profiles1.csv')