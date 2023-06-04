'''
Author: Gabriella Vidgen
Date: 01 June 2023

Functions used to create figures comparing the results of varying the percentage of 
coordinated charging profiles.

Can be used for either coordinated charging profile - select which profile to analyse
within the main function.
'''

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Plot comparing capacity for 30% and 50% coord charging
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
    percent_coord1 = 30
    percent_coord2 = 50

    folder1 = f'Results{folder_num}/{percent_coord1}/'
    folder2 = f'Results{folder_num}/{percent_coord2}/'

    cap_labels, start_cap, end_cap1 = process_cap_data(folder1)
    _, _, end_cap2 = process_cap_data(folder2)

    # Create plot
    plt.bar(np.arange(len(cap_labels))-0.3, start_cap, width=0.3, label='Start', color=neutral_color)
    plt.bar(np.arange(len(cap_labels)), end_cap1, width=0.3, label='End - 30% Coord. Charging', color=color_30)
    plt.bar(np.arange(len(cap_labels))+0.3, end_cap2, width=0.3, label='End - 50% Coord. Charging', color=color_50)
    # Adjust the figure size or the margins of the plot
    plt.subplots_adjust(bottom=0.25, right=0.95)
    plt.title(f'Total Annual Power Capacity for {coord_profile} \nCoordinated Charging Profile')
    plt.ylabel('Capacity (GW)')
    plt.xticks(np.arange(len(cap_labels)), cap_labels, rotation=90)
    # plt.ylim(0, 25)
    plt.legend()
    plt.savefig(f'{coord_profile} - cap.png')
    plt.show()

# Plot comparing energy production for 30% and 50% coord charging
def process_energy_data(folder):
    power_file = f'{folder}power.csv'
    power_df = pd.read_csv(power_file)
    
    power_df = power_df.iloc[[1], 1:-1]
    ener_df = power_df * (8760/(1000)) # MW to GWh
    ener_df.columns = ener_df.columns.str.replace('[_QLD]', '', regex=True) # Fix headings

    return ener_df.iloc[0, :], ener_df.columns

def compare_energy():
    percent_coord1 = 30
    percent_coord2 = 50

    folder1 = f'Results{folder_num}/{percent_coord1}/'
    folder2 = f'Results{folder_num}/{percent_coord2}/'

    energy_vals1, energy_labels = process_energy_data(folder1)
    energy_vals2, _ = process_energy_data(folder2)

    plt.bar(np.arange(len(energy_labels))-0.2, energy_vals1, width=0.4, label='30% Coord. Charging', color=color_30)
    plt.bar(np.arange(len(energy_labels))+0.2, energy_vals2, width=0.4, label='50% Coord. Charging', color=color_50)
    # Adjust the figure size or the margins of the plot
    plt.subplots_adjust(bottom=0.25, right=0.95)
    plt.title(f'Total Annual Energy Production for {coord_profile} \nCoordinated Charging Profile')
    plt.ylabel('Annual Energy Production (GWh)')
    plt.xticks(np.arange(len(energy_labels)), energy_labels, rotation=90)
    # plt.ylim(0, 5 * 10**8)
    plt.legend()
    plt.savefig(f'{coord_profile} - energy.png')
    plt.show()

# Plot of energy production over a typical day
def day_gen_graph(percent_coord): # 30 - 50
    day_index = 95 # 5th April

    folder = f'Results{folder_num}/{percent_coord}/'

    power_file = f'{folder}power.csv'
    power_df = pd.read_csv(power_file)

    start_ind = day_index * 24 + 2
    end_ind = start_ind + 24

    power_df = power_df.iloc[start_ind: end_ind, 1:-1]
    power_df /= 1000 # MW to GW
    power_df.columns = power_df.columns.str.replace('[_QLD]', '', regex=True) # Fix headings
    cumulative = power_df.cumsum(axis=1)

    colors = ['yellow', 'limegreen', 'teal', 'pink', 'crimson', 'magenta', 'orange', 'darkviolet', 'lime', 'blue', 'cyan']
    

    for i in range(power_df.shape[1]): 
        if i == 0:
            plt.fill_between(power_df.index-start_ind, cumulative.iloc[:, i], 
                                alpha=0.5, label=power_df.columns[i], 
                                color=colors[i])
        else:
            plt.fill_between(power_df.index-start_ind, cumulative.iloc[:, i], 
                                cumulative.iloc[:, i-1], alpha=0.5, 
                                label=power_df.columns[i], color=colors[i])

    plt.title(f'Power Generation for a Typical Weekday \n({percent_coord}% {coord_profile} Coordinated Charging Profile)')

    plt.xlabel('Hour')
    plt.xticks(range(0, 24, 2))
    plt.ylabel('Power Generated (GW)')
    plt.ylim(0, 22)
    plt.legend(loc='upper left', bbox_to_anchor=(1.02, 1))
    plt.subplots_adjust(right=0.7)  # Adjust the right margin to accommodate the legend
    plt.savefig(f'{coord_profile} - day_gen_{percent_coord}.png')
    plt.show()

def four_gen_profs(percent_coord):
    folder = f'Results{folder_num}/{percent_coord}/'
    power_file = f'{folder}power.csv'
    power_df = pd.read_csv(power_file)
    power_df = power_df.iloc[:, 1:-1]
    power_df /= 1000  # MW to GW
    power_df.columns = power_df.columns.str.replace('[_QLD]', '', regex=True)  # Fix headings
    cumulative = power_df.cumsum(axis=1)

    colors = ['yellow', 'limegreen', 'teal', 'pink', 'crimson', 'magenta', 'orange', 'darkviolet', 'lime', 'blue',
              'cyan']

    # 5th of Jan, April, July, October (all weekdays)
    day_inds = [5, 95, 186, 278]
    season_cum_dfs = []
    season_pow_dfs = []

    seasons = ['Summer', 'Autumn', 'Winter', 'Spring']

    for ind in day_inds:
        start_ind = (ind - 1) * 24
        end_ind = start_ind + 24

        season_cum_df = cumulative.iloc[start_ind:end_ind + 1].reset_index(drop=True)
        season_cum_dfs.append(season_cum_df)

        season_pow_df = power_df.iloc[start_ind:end_ind + 1].reset_index(drop=True)
        season_pow_dfs.append(season_pow_df)

    fig, axs = plt.subplots(2, 2, figsize=(12, 8))

    for i, ax in enumerate(axs.flatten()):
        for j in range(season_pow_dfs[i].shape[1]):
            if j == 0:
                ax.fill_between(range(25), season_cum_dfs[i].iloc[:, j], alpha=0.5,
                                label=power_df.columns[j], color=colors[j])
            else:
                ax.fill_between(range(25), season_cum_dfs[i].iloc[:, j], season_cum_dfs[i].iloc[:, j - 1],
                                alpha=0.5, label=power_df.columns[j], color=colors[j])

        ax.set_xlabel('Hour')
        ax.set_xlim(0, 24)
        ax.set_xticks(range(0, 24, 2))
        ax.set_ylabel('Power Generated (GW)')
        ax.set_ylim(0, 25)
        ax.set_title(seasons[i])
        ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1))

    fig.suptitle(f'Seasonal Weekday Power Generation for {percent_coord}% {coord_profile} Coordinated Charging Profile ')
    fig.subplots_adjust(right=0.7)  # Adjust the right margin to accommodate the legend
    plt.tight_layout()
    plt.savefig(f'{coord_profile} - season_gen_{percent_coord}.png')
    plt.show()

def year_gen(percent_coord):
    # Create a list of abbreviated month names
    months = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']
    month_indices = [1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]
    month_ind_new = [(ind - 1) * 24 for ind in month_indices]

    folder = f'Results{folder_num}/{percent_coord}/'
    power_file = f'{folder}power.csv'
    power_df = pd.read_csv(power_file)
    power_df = power_df.iloc[:, 1:-1]
    power_df /= 1000  # MW to GW
    power_df.columns = power_df.columns.str.replace('[_QLD]', '', regex=True)  # Fix headings
    cumulative = power_df.cumsum(axis=1)

    colors = ['yellow', 'limegreen', 'teal', 'pink', 'crimson', 'magenta', 'orange', 'darkviolet', 'lime', 'blue',
              'cyan']

    fig, ax = plt.subplots(figsize=(16, 4))  # Adjust the figure size as desired

    for i in range(power_df.shape[1]):
        if i == 0:
            ax.fill_between(power_df.index, cumulative.iloc[:, i],
                            alpha=0.5, label=power_df.columns[i],
                            color=colors[i], linewidth=0.5)  # Set the linewidth
        else:
            ax.fill_between(power_df.index, cumulative.iloc[:, i],
                            cumulative.iloc[:, i-1], alpha=0.5,
                            label=power_df.columns[i], color=colors[i], linewidth=0.5)  # Set the linewidth

    ax.set_title(f'Power Generation for 2050 ({percent_coord}% {coord_profile} Coordinated Charging Profile)')
    ax.set_xlabel('Month')
    ax.set_xlim(0, 8760)
    ax.set_xticks(month_ind_new)
    ax.set_xticklabels(months)
    ax.set_ylabel('Power Generated (GW)')
    ax.set_ylim(0, 30)
    ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1))
    fig.subplots_adjust(left=0.05, right=0.87)  # Adjust the right margin to accommodate the legend
    # plt.savefig(f'{coord_profile} - day_gen_{percent_coord}.png')
    plt.show()


# Plot comparing the generator profit for 30% and 50% coord charging
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
    percent_coord1 = 30
    percent_coord2 = 50

    folder1 = f'Results{folder_num}/{percent_coord1}/'
    folder2 = f'Results{folder_num}/{percent_coord2}/'

    prof_labels, prof_vals1 = process_profit_data(folder1)
    _, prof_vals2 = process_profit_data(folder2)

    plt.bar(np.arange(len(prof_labels))-0.2, prof_vals1, width=0.4, label='30% Coord. Charging', color=color_30)
    plt.bar(np.arange(len(prof_labels))+0.2, prof_vals2, width=0.4, label='50% Coord. Charging', color=color_50)
    # Adjust the figure size or the margins of the plot
    plt.subplots_adjust(bottom=0.25, right=0.95)
    plt.title(f'Total Annual Profit for {coord_profile} \nCoordinated Charging Profile')
    plt.ylabel('Annual Profit ($ million AUD)')
    plt.xticks(np.arange(len(prof_labels)), prof_labels, rotation=90)
    # plt.ylim(0, 5 * 10**8)
    plt.legend()
    plt.savefig(f'{coord_profile} - profit.png')
    plt.show()

# Plot comparing the GenX objective function for all charging %s
def process_cost_data(folder):
    cost_file = f'{folder}costs.csv'
    cost_df = pd.read_csv(cost_file)
    cost_df = cost_df.iloc[1, 1] # Remove irrelevant columns and rows
    cost_df /= 10**9 # Change from $ to $ billion

    return cost_df

def compare_obj_func():
    percent_coords = [30, 35, 40, 45, 50]
    obj_func_vals = []

    for percent in percent_coords:
        folder = f'Results{folder_num}/{percent}/'
        genx_obj_val = process_cost_data(folder)
        obj_func_vals.append(genx_obj_val)

    # plt.plot(percent_coords, obj_func_vals, color=neutral_color)
    # plt.title(f'GenX Objective Function Value for {coord_profile} \nCoordinated Charging Profile')
    # plt.xlabel('Percentage of Coordinated Charging')
    # plt.ylabel('GenX Objective Function Value ($ billion AUD)')
    # plt.xticks(np.arange(30, 51, 5))
    # plt.savefig(f'{coord_profile} - obj_func.png')
    # plt.show()
    print(obj_func_vals)

# Plot comparing renewables curtailment for all charging %s
def process_curtailment_data(folder):

    power_file = f'{folder}power.csv'
    curt_file = f'{folder}curtail.csv'

    power_df = pd.read_csv(power_file)
    power_df.columns = power_df.columns.str.replace('[_QLD]', '', regex=True) # Fix headings

    total_used_wind = power_df.iloc[1, 6]
    total_used_solar = power_df.iloc[1, 7]
    total_used_renew = total_used_wind + total_used_solar

    curt_df = pd.read_csv(curt_file)
    curt_df.columns = curt_df.columns.str.replace('[_QLD]', '', regex=True) # Fix headings

    total_curt_wind = curt_df.iloc[1, 6]
    total_curt_solar = curt_df.iloc[1, 7]
    total_curt_renew = total_curt_wind + total_curt_solar

    curt_wind_percent = 100 * (total_curt_wind)/(total_curt_wind + total_used_wind)
    curt_solar_percent = 100 * (total_curt_solar)/(total_curt_solar + total_used_solar)
    total_curt_percent = 100 * (total_curt_renew)/(total_curt_renew + total_used_renew)

    return curt_wind_percent, curt_solar_percent, total_curt_percent

def compare_curt():
    percent_coords = [30, 35, 40, 45, 50]
    wind_curt = []
    solar_curt = []
    total_curt = []

    for percent in percent_coords:
        folder = f'Results{folder_num}/{percent}/'
        curt_wind_percent, curt_solar_percent, total_curt_percent = process_curtailment_data(folder)
        wind_curt.append(curt_wind_percent)
        solar_curt.append(curt_solar_percent)
        total_curt.append(total_curt_percent)

    plt.plot(percent_coords, wind_curt, label='Wind', color='orangered')
    plt.plot(percent_coords, solar_curt, label='Solar', color='gold')
    plt.plot(percent_coords, total_curt, label='Total', color='orange')
    plt.title(f'Total Renewables Curtailment for {coord_profile} \nCoordinated Charging Profile')
    plt.xlabel('Percentage of Coordinated Charging')
    plt.ylabel('Nameplate Capacity (%)')
    plt.xticks(np.arange(30, 51, 5))
    plt.ylim(6, 13)
    plt.legend()
    plt.savefig(f'{coord_profile} - curt.png')
    plt.show()

    print(wind_curt)
    print(solar_curt)
    print(total_curt)

def day_curt_graph(percent_coord): # 30 - 50
    day_index = 95 # 5th April

    start_ind = day_index * 24 + 2
    end_ind = start_ind + 24

    folder = f'Results{folder_num}/{percent_coord}/'
    cap_file = f'{folder}capacity.csv'
    gen_var_file = f'{folder}Generators_variability.csv'
    power_file = f'{folder}power.csv'

    gen_var_df = pd.read_csv(gen_var_file)
    gen_var_df = gen_var_df.iloc[:, [6, 7]] # Remove irrelevant columns and rows
    gen_var_df.columns = gen_var_df.columns.str.replace('[_QLD]', '', regex=True) # Fix headings

    cap_df = pd.read_csv(cap_file)
    cap_df = cap_df.iloc[[5, 6], [0, 4]] # Remove irrelevant columns and rows
    cap_df.iloc[:, 0] = cap_df.iloc[:, 0].str.replace('QLD_', '') # Fix headings

    wind_inst_cap = cap_df.iloc[0, 1]
    solar_inst_cap = cap_df.iloc[1, 1]

    avail_power_df = gen_var_df.copy()
    avail_power_df /= 1000 # MW to GW
    avail_power_df['wind'] *= wind_inst_cap
    avail_power_df['solar'] *= solar_inst_cap
    avail_renew_power = avail_power_df.iloc[start_ind:end_ind, :]['wind'] + avail_power_df.iloc[start_ind:end_ind, :]['solar']
    # avail_renew_power = avail_power_df.iloc[start_ind:end_ind, :]['wind']

    power_df = pd.read_csv(power_file)
    power_df = power_df.iloc[start_ind: end_ind, [6, 7]]
    power_df /= 1000 # MW to GW
    power_df.columns = power_df.columns.str.replace('[_QLD]', '', regex=True) # Fix headings
    used_renew_power = power_df.iloc[:, 0] + power_df.iloc[:, 1]
    # used_renew_power = power_df.iloc[:, 0]
    
    curt = avail_renew_power - used_renew_power

    plt.bar(list(range(start_ind, end_ind)), used_renew_power, label='Generation', color='limegreen')
    plt.bar(list(range(start_ind, end_ind)), curt, bottom=used_renew_power, label='Curtailment', color='red')

    # Customize the graph
    plt.xlabel('Hour')
    plt.xticks(range(start_ind-day_index, 24, 2))
    plt.ylabel('Power Generation (GW)')
    plt.ylim(0, 10)
    plt.title(f'Renewables Generation and Curtailment for a Typical Weekday \n({percent_coord}% {coord_profile} Coordinated Charging Profile)')
    plt.legend()
    plt.savefig(f'{coord_profile} - day_curt_{percent_coord}.png')
    plt.show()

def four_curt_profs(percent_coord):
    folder = f'Results{folder_num}/{percent_coord}/'

    power_file = f'{folder}power.csv'
    curt_file = f'{folder}curtail.csv'

    power_df = pd.read_csv(power_file)
    power_df = power_df.iloc[2:, [6, 7]]
    power_df /= 1000 # MW to GW
    power_df.columns = power_df.columns.str.replace('[_QLD]', '', regex=True) # Fix headings

    curt_df = pd.read_csv(curt_file)
    curt_df = curt_df.iloc[2:, [6, 7]]
    curt_df /= 1000 # MW to GW
    curt_df.columns = curt_df.columns.str.replace('[_QLD]', '', regex=True) # Fix headings

    # 5th of Jan, April, July, October (all weekdays)
    day_inds = [5, 95, 186, 278]
    season_gen_dfs = []
    season_wind_dfs = []
    season_solar_dfs = []

    seasons = ['Summer', 'Autumn', 'Winter', 'Spring']

    for ind in day_inds:
        start_ind = (ind - 1) * 24
        end_ind = start_ind + 24

        used_wind_power = power_df.iloc[:, 0]
        used_solar_power = power_df.iloc[:, 1]
        used_renew_power = used_wind_power + used_solar_power

        wind_curt = curt_df.iloc[:, 0]
        solar_curt = curt_df.iloc[:, 1]
        curt = wind_curt + solar_curt

        season_gen_df = used_renew_power.iloc[start_ind:end_ind + 1].reset_index(drop=True)
        season_gen_dfs.append(season_gen_df)

        season_wind_df = wind_curt.iloc[start_ind:end_ind + 1].reset_index(drop=True)
        season_wind_dfs.append(season_wind_df)

        season_solar_df = solar_curt.iloc[start_ind:end_ind + 1].reset_index(drop=True)
        season_solar_dfs.append(season_solar_df)

    fig, axs = plt.subplots(2, 2, figsize=(12, 8))

    for i, ax in enumerate(axs.flatten()):
        ax.bar(range(25), season_gen_dfs[i], label='Generation', alpha=0.7, color='blue')
        ax.bar(range(25), season_wind_dfs[i], label='Wind Curtailment', bottom=season_gen_dfs[i], alpha=0.7, color='red')
        ax.bar(range(25), season_solar_dfs[i], label='Solar Curtailment', bottom=season_gen_dfs[i] + season_wind_dfs[i], alpha=0.7, color='gold')

        ax.set_xticks(range(0, 25, 2))  # Set x-ticks to every second value
        ax.set_xticklabels(range(0, 25, 2))  # Set x-tick labels to every second value
        ax.set_xlabel('Hour')
        ax.set_ylabel('Power (GW)')
        ax.set_ylim(-1, 35)
        ax.set_title(f'{seasons[i]}')

        ax.legend()

    fig.suptitle(f'Seasonal Weekday Renewable Generation and Curtailment for {percent_coord}% {coord_profile} Coordinated Charging Profile ')
    fig.subplots_adjust(right=0.7)  # Adjust the right margin to accommodate the legend
    plt.tight_layout()
    plt.savefig(f'{coord_profile} - season_curt_{percent_coord}.png')
    plt.show()

# Compare carbon emissions for all charging %s
def process_emissions_data(folder):
    emissions_file = f'{folder}emissions.csv'
    emis_df = pd.read_csv(emissions_file)    
    emis_df = emis_df.iloc[2:, 2] # Remove irrelevant columns and rows
    total_emis = emis_df.sum() 
    total_emis /= 1000 # Mt to Gt

    return total_emis

def compare_emissions():
    percent_coords = [30, 35, 40, 45, 50]
    emissions_vals = []

    for percent in percent_coords:
        folder = f'Results{folder_num}/{percent}/'
        emissions = process_emissions_data(folder)
        emissions_vals.append(emissions)

    # plt.plot(percent_coords, emissions_vals, color=neutral_color)
    # plt.title(f'Total Carbon Emissions for {coord_profile} \nCoordinated Charging Profile')
    # plt.xlabel('Percentage of Coordinated Charging')
    # plt.ylabel('Total Emissions (CO2-e)')
    # plt.xticks(np.arange(30, 51, 5))
    # plt.savefig(f'{coord_profile} - emissions.png')
    # plt.show()
    print(emissions_vals)

def process_year_load_data(folder):
    load_file = f'{folder}Load_data.csv'

    load_df = pd.read_csv(load_file)
    load_df = load_df.iloc[:, 9] # Remove irrelevent columns
    load_df /= 1000 # MW to GW

    return load_df

def compare_year_load():
    percent_coord1 = 30
    percent_coord2 = 50

    folder1 = f'Results{folder_num}/{percent_coord1}/'
    folder2 = f'Results{folder_num}/{percent_coord2}/'

    load_df1 = process_year_load_data(folder1)
    load_df2 = process_year_load_data(folder2)

    # Create a list of abbreviated month names
    months = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']
    month_indices = [1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]
    month_ind_new = []
    for ind in month_indices:
        ind = (ind-1)*24
        month_ind_new.append(ind)

    # Create two subplots, one above the other
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    # Plot the data on the first subplot
    ax1.plot(load_df1.index, load_df1, linewidth=0.5, color=neutral_color, label='30% Coord. Charging')
    ax1.set_title(f'Demand Load Over the Year of 2050 for {coord_profile} Coordinated Charging Profile')
    ax1.set_ylabel('Demand Load (GW)')
    ax1.set_xlim(0, 8760)
    ax1.set_ylim(5, 22)
    ax1.set_xticks(month_ind_new)
    ax1.set_xticklabels(months)
    ax1.legend()

    # Plot the data on the second subplot
    ax2.plot(load_df2.index, load_df2, linewidth=0.5, color=color_50, label='50% Coord. Charging')
    ax2.set_ylabel('Demand Load (GW)')
    ax2.set_xlim(0, 8760)
    ax2.set_ylim(5, 22)
    ax2.set_xticks(month_ind_new)
    ax2.set_xticklabels(months)
    ax2.legend()

    plt.tight_layout()  # Adjust the spacing between subplots
    plt.savefig(f'{coord_profile} - year_loads.png')
    plt.show()

def four_load_profs():
    percent_coord1 = 30
    percent_coord2 = 50

    folder1 = f'Results{folder_num}/{percent_coord1}/'
    folder2 = f'Results{folder_num}/{percent_coord2}/'

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

        ax.plot(x_values, season_dfs1[i], color=color_30, label='30% Coord.Charging')
        ax.plot(x_values, season_dfs2[i], color='blue', label='50% Coord. Charging')
        ax.set_xlabel('Hour')
        ax.set_xlim(0, 24)
        ax.set_xticks(range(0, 24, 2))
        ax.set_ylabel('Demand Load (GW)')
        ax.set_ylim(7, 19)
        ax.set_title(seasons[i])
        ax.legend()

    fig.suptitle(f'Seasonal Weekday Demand Load Profiles for {coord_profile} Coordinated Charging Profile ')
    plt.tight_layout()
    plt.savefig(f'{coord_profile} - season_loads.png')
    plt.show()


if __name__ == '__main__':
    # COMMENT OUT PROFILE HERE

    coord_profile = "Day Peak"
    # coord_profile = "Day and Night Peaks"

    if coord_profile == "Day Peak":
        folder_num = 1

    elif coord_profile == "Day and Night Peaks":
        folder_num = 2

    color_30 = 'cyan'
    color_50 = 'darkturquoise'
    neutral_color = 'orange'


    # DECLARE FUNCTION HERE

    # compare_curt()
    # day_curt_graph2(50)
    # compare_emissions()
    # four_load_profs()
    # four_curt_profs(35)
    # year_gen(50)
    four_gen_profs(35)