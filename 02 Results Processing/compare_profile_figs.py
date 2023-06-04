'''
Author: Gabriella Vidgen
Date: 01 June 2023

Functions used to create figures comparing the two coordinated charging profiles.
'''

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def process_year_load_data(folder):
    load_file = f'{folder}Load_data.csv'

    load_df = pd.read_csv(load_file)
    load_df = load_df.iloc[:, 9] # Remove irrelevent columns
    load_df /= 1000 # MW to GW

    return load_df

def four_load_profs():
    percent_coord = 35

    folder1 = f'Results1/{percent_coord}/'
    folder2 = f'Results2/{percent_coord}/'

    load_df1 = process_year_load_data(folder1)
    load_df2 = process_year_load_data(folder2)

    # 5th of Jan , April, July, October (all weekdays)
    day_inds = [5, 95, 186, 278]
    season_dfs1 = []
    season_dfs2 = []

    seasons = ['Summer', 'Autumn', 'Winter', 'Spring']

    for ind in day_inds:
        start_ind = (ind-1) * 24
        end_ind = start_ind + 24

        season_day_df1 = load_df1.copy()
        season_day_df1 = season_day_df1.iloc[start_ind:end_ind+1]
        season_dfs1.append(season_day_df1)

        season_day_df2 = load_df2.copy()
        season_day_df2 = season_day_df2.iloc[start_ind:end_ind+1]
        season_dfs2.append(season_day_df2)

    fig, axs = plt.subplots(2, 2, figsize=(12, 8))

    for i, ax in enumerate(axs.flatten()):
        x_values = range(25)  # Create a range from 0 to 23

        ax.plot(x_values, season_dfs1[i], color=color_day, label='Day Peak')
        ax.plot(x_values, season_dfs2[i], color=color_daynight, label='Day and Night Peaks')
        ax.set_xlabel('Hour')
        ax.set_xlim(0, 24)
        ax.set_xticks(range(0, 24, 2))
        ax.set_ylabel('Demand Load (GW)')
        ax.set_ylim(7, 19)
        ax.set_title(seasons[i])
        ax.legend()

    fig.suptitle(f'Comparison of Seasonal Weekday Demand Load Profiles for 35% Coordinated Charging')
    plt.tight_layout()
    plt.savefig(f'Compare - season_loads.png')
    plt.show()

def process_cap_data(folder):
    cap_file = f'{folder}capacity.csv'
    cap_df = pd.read_csv(cap_file)    

    cap_df = cap_df.iloc[:-1, [0, 2, 5]] # Remove irrelevant columns and rows    
    cap_df.iloc[:, [1, 2]] /= 1000 # MW to GW    
    cap_df.iloc[:, 0] = cap_df.iloc[:, 0].str.replace('QLD_', '') # Fix headings

    cap_labels = cap_df['Resource']
    start_cap = cap_df['StartCap']
    end_cap = cap_df['EndCap']

    return cap_labels, start_cap, end_cap

def compare_cap():
    percent_coord = 35

    folder1 = f'Results1/{percent_coord}/'
    folder2 = f'Results2/{percent_coord}/'

    cap_labels, start_cap, end_cap1 = process_cap_data(folder1)
    _, _, end_cap2 = process_cap_data(folder2)

    # Create plot
    plt.bar(np.arange(len(cap_labels))-0.3, start_cap, width=0.3, label='Start', color=neutral_color)
    plt.bar(np.arange(len(cap_labels)), end_cap1, width=0.3, label='End - Day Peak', color=color_day)
    plt.bar(np.arange(len(cap_labels))+0.3, end_cap2, width=0.3, label='End - Day and Night Peaks', color=color_daynight)
    # Adjust the figure size or the margins of the plot
    plt.subplots_adjust(bottom=0.25, right=0.95)
    plt.title(f'Comparison of Total Annual Power Capacity for 35% \nCoordinated Charging')
    plt.ylabel('Capacity (GW)')
    plt.xticks(np.arange(len(cap_labels)), cap_labels, rotation=90)
    # plt.ylim(0, 25)
    plt.legend()
    plt.savefig(f'Compare - cap.png')
    plt.show()

def process_energy_data(folder):
    power_file = f'{folder}power.csv'
    power_df = pd.read_csv(power_file)
    
    power_df = power_df.iloc[[1], 1:-1]
    ener_df = power_df * (8760/(1000)) # MW to GWh
    ener_df.columns = ener_df.columns.str.replace('[_QLD]', '', regex=True) # Fix headings

    return ener_df.iloc[0, :], ener_df.columns

def compare_energy():
    percent_coord = 35

    folder1 = f'Results1/{percent_coord}/'
    folder2 = f'Results2/{percent_coord}/'

    energy_vals1, energy_labels = process_energy_data(folder1)
    energy_vals2, _ = process_energy_data(folder2)

    plt.bar(np.arange(len(energy_labels))-0.2, energy_vals1, width=0.4, label='Day Peak', color=color_day)
    plt.bar(np.arange(len(energy_labels))+0.2, energy_vals2, width=0.4, label='Day and Night Peaks', color=color_daynight)
    # Adjust the figure size or the margins of the plot
    plt.subplots_adjust(bottom=0.25, right=0.95)
    plt.title(f'Comparison of Total Annual Energy Production for 35% \nCoordinated Charging Profile')
    plt.ylabel('Annual Energy Production (GWh)')
    plt.xticks(np.arange(len(energy_labels)), energy_labels, rotation=90)
    # plt.ylim(0, 5 * 10**8)
    plt.legend()
    plt.savefig(f'Compare - energy.png')
    plt.show()

def process_profit_data(folder):
    profit_file = f'{folder}NetRevenue.csv'
    prof_df = pd.read_csv(profit_file)    
    prof_df = prof_df.iloc[:, [1, -1]] # Remove irrelevant columns and rows    
    prof_df.iloc[:, -1] /= 10**6 # Change from $ to $ million    
    prof_df.iloc[:, 0] =prof_df.iloc[:, 0].str.replace('QLD_', '') # Fix headings

    prof_labels = prof_df.iloc[:, 0]
    prof_vals = prof_df.iloc[:, 1]

    return prof_labels, prof_vals

def compare_profit():
    percent_coord = 35

    folder1 = f'Results1/{percent_coord}/'
    folder2 = f'Results2/{percent_coord}/'

    prof_labels, prof_vals1 = process_profit_data(folder1)
    _, prof_vals2 = process_profit_data(folder2)

    plt.bar(np.arange(len(prof_labels))-0.2, prof_vals1, width=0.4, label='Day Peak', color=color_day)
    plt.bar(np.arange(len(prof_labels))+0.2, prof_vals2, width=0.4, label='Day and Night Peaks', color=color_daynight)
    # Adjust the figure size or the margins of the plot
    plt.subplots_adjust(bottom=0.25, right=0.95)
    plt.title(f'Comparison of Total Annual Profit for 35% \nCoordinated Charging Profile')
    plt.ylabel('Annual Profit ($ million AUD)')
    plt.xticks(np.arange(len(prof_labels)), prof_labels, rotation=90)
    # plt.ylim(0, 5 * 10**8)
    plt.legend()
    plt.savefig(f'Compare - profit.png')
    plt.show()



if __name__ == '__main__':
    # COMMENT OUT PROFILE HERE

    color_day = 'blue'
    color_daynight = 'magenta'
    neutral_color = 'orange'


    # DECLARE FUNCTION HERE
    # four_load_profs()
    # compare_cap()
    # compare_energy()
    compare_profit()