import pandas as pd
import numpy as np

# TEL-wind_direction@200 not working
# BLE-ground_temperature suspicious

name_map = {'TEL-temperature_1-degC-Avg'          : 'TEL-temperature@200',
            'TEL-temperature_2-degC-Avg'          : 'TEL-temperature@335',
            'TEL-rel_humidity_1-%-Smp'            : 'TEL-relative_humidity@200',
            'TEL-rel_humidity_2-%-Smp'            : 'TEL-relative_humidity@335',
            'TEL-wind_speed_1-m/s-Avg'            : 'TEL-wind_speed@200',
            'TEL-wind_speed_2-m/s-Avg'            : 'TEL-wind_speed@335',
            'TEL-gust_speed_1-m/s-Max'            : 'TEL-gust_speed@200',
            'TEL-gust_speed_2-m/s-Max'            : 'TEL-gust_speed@335',
            'TEL-wind_direction_1-deg-Smp'        : 'TEL-wind_direction@200',
            'TEL-wind_direction_2-deg-Smp'        : 'TEL-wind_direction@335',
            'TEL-air_pressure-hPa-Avg'            : 'TEL-air_pressure',
            'TEL-ground_temperature-degC-Avg'     : 'TEL-ground_temperature',
            'TEL-SWup-W/m^2-Avg'                  : 'TEL-SW_up',
            'TEL-SWdown-W/m^2-Avg'                : 'TEL-SW_down',
            'TEL-LWup-W/m^2-Avg'                  : 'TEL-LW_up',
            'TEL-LWdown-W/m^2-Avg'                : 'TEL-LW_down',
            'BLE-BOT-temperature-degC-Avg'        : 'BLE-temperature@200',
            'BLE-TOP-temperature-degC-Avg'        : 'BLE-temperature@335',
            'BLE-BOT-rel_humidity-%-Smp'          : 'BLE-relative_humidity@200',
            'BLE-TOP-rel_humidity-%-Smp'          : 'BLE-relative_humidity@335',
            'BLE-BOT-wind_speed-m/s-Avg'          : 'BLE-wind_speed@200',
            'BLE-TOP-wind_speed-m/s-Avg'          : 'BLE-wind_speed@335',
            'BLE-BOT-gust_speed-m/s-Max'          : 'BLE-gust_speed@200',
            'BLE-TOP-gust_speed-m/s-Max'          : 'BLE-gust_speed@335',
            'BLE-BOT-wind_direction-deg-Smp'      : 'BLE-wind_direction@200',
            'BLE-TOP-wind_direction-deg-Smp'      : 'BLE-wind_direction@335',
            'BLE-BOT-air_pressure-hPa-Smp'        : 'BLE-air_pressure',
            'BLE-BOT-ground_temperature-degC-Avg' : 'BLE-ground_temperature',
            'BLE-RAD-SW_up_Avg-W/m^2-Avg'         : 'BLE-SW_up',
            'BLE-RAD-SW_down_Avg-W/m^2-Avg'       : 'BLE-SW_down',
            'BLE-RAD-LW_up_Avg-W/m^2-Avg'         : 'BLE-LW_up',
            'BLE-RAD-LW_down_Avg-W/m^2-Avg'       : 'BLE-LW_down'}

# file containing Tellbreen data
tellbreen_path = "/Users/yanngirodo/Desktop/Svalbard/cours/AGF212/report/Met_Data/Tellbreen/Usable/CR3000_MaggieMay_Res_data_1_min.dat"

# folder containing Blekumbreen data
blekumbreen_path = "/Users/yanngirodo/Desktop/Svalbard/cours/AGF212/report/Met_Data/Blekumbreen/Usable"

# paths to individual data files of sub-stations
bot_blekumbreen_path = blekumbreen_path + '/CR1000_Layla_Res_data_1_min.dat'
top_blekumbreen_path = blekumbreen_path + '/CR1000_TomJoad_Res_data_1_min.dat'
rad_blekumbreen_path = blekumbreen_path + '/CR1000_Radiation_Res_data_1_min.dat'

# dropped columns from tellbreen
tellbreen_drops = ['RECORD-RN-', 'BattV-Volts-Min', 'CNR1_T_degC-degC-Avg']

# droppend columns from bottom blekumbreen
bot_blekumbreen_drops = ['RECORD-RN-', 'BattV-Volts-Min', 'SWup-W/m^2-Avg', 'SWdown-W/m^2-Avg']

# droppend columns from top blekumbreen
top_blekumbreen_drops = ['RECORD-RN-', 'BattV-Volts-Min']

# droppend columns from radiation blekumbreen
rad_blekumbreen_drops = ['RECORD-RN-', 'BattV-V-Min', 'Panel_temperature-degC-Smp', 'CNR1_T_degC_Avg-degC-Avg']

def get_data(path) :

    # array that will store the data
    data = []

    # iterate over lines of the specific file at the given path
    with open(path, 'r') as file :
        for line in file :

            # split the values in the line and strip it from spaces, return characters, and quotation marks
            formated_line = line.strip().split(',')
            for k in range(len(formated_line)) : formated_line[k] = formated_line[k].strip('"')

            # check for the 5 first characters, which should be the beginning of a time stamp, and if so, add the line to the data array
            if formated_line[0][:5] == '2025-' : data.append(formated_line)
    
    return data

def get_columns(path) :

    # open the file at the given path to read its overhead
    with open(path, 'r') as file :
        
        # get the 4 first lines, split and strip them
        i = 0
        while i < 4 :
            formated_line = file.readline().strip().split(',')
            for k in range(len(formated_line)) : formated_line[k] = formated_line[k].strip('"')
            
            # second line contains the variable names
            if i == 1 :
                columns = formated_line[1:]
            
            # third line contains the unit of the variables
            if i == 2 :
                for j in range(len(columns)) :
                    columns[j] += '-' + formated_line[j+1]
            
            # fourth line contains the type of data (min, avg...)
            if i == 3 :
                for j in range(len(columns)) :
                    columns[j] += '-' + formated_line[j+1]
            
            i += 1
    
    return columns

def get_dataframe(data, columns, drops) :

    # split the data into time stamps (which will be used as indices of the dataframe), and actual numerical values
    data = np.array(data)
    time_stamps = data[:, 0]
    values = data[:, 1:]

    # set time stamps to a proper timestamp type
    time_stamps = [pd.Timestamp(str(ts)) for ts in time_stamps]

    # generate the pandas dataframe
    formated_data = pd.DataFrame(data = values, index = time_stamps, columns = columns, dtype = float)

    # remove dropped columns
    for drop in drops : formated_data.drop(columns = drop, inplace = True)

    return formated_data

def import_data() :

    # get dataframes from tellbreen and blekumbreen
    tellbreen_dataframe = get_dataframe(get_data(tellbreen_path), get_columns(tellbreen_path), drops = tellbreen_drops)
    bot_blekumbreen_dataframe = get_dataframe(get_data(bot_blekumbreen_path), get_columns(bot_blekumbreen_path), drops = bot_blekumbreen_drops)
    top_blekumbreen_dataframe = get_dataframe(get_data(top_blekumbreen_path), get_columns(top_blekumbreen_path), drops = top_blekumbreen_drops)
    rad_blekumbreen_dataframe = get_dataframe(get_data(rad_blekumbreen_path), get_columns(rad_blekumbreen_path), drops = rad_blekumbreen_drops)

    # add a prefix to the columns to identify which glacier and which logger the variable comes from
    for column in tellbreen_dataframe.columns : tellbreen_dataframe.rename({column : 'TEL-' + column}, axis = 1, inplace = True)
    for column in bot_blekumbreen_dataframe.columns : bot_blekumbreen_dataframe.rename({column : 'BLE-BOT-' + column}, axis = 1, inplace = True)
    for column in top_blekumbreen_dataframe.columns : top_blekumbreen_dataframe.rename({column : 'BLE-TOP-' + column}, axis = 1, inplace = True)
    for column in rad_blekumbreen_dataframe.columns : rad_blekumbreen_dataframe.rename({column : 'BLE-RAD-' + column}, axis = 1, inplace = True)

    # concatenate the 4 dataframes columns by columns, filling the incomplete time stamps with NaN values
    formated_data = pd.concat([tellbreen_dataframe, bot_blekumbreen_dataframe, top_blekumbreen_dataframe, rad_blekumbreen_dataframe], axis = 1, join = 'outer')

    # reorder and rename columns using the name map
    formated_data = formated_data.reindex(name_map.keys(), axis = 1)
    formated_data.rename(name_map, axis = 1, inplace = True)

    # sort the table
    formated_data.sort_index(axis = 0, inplace = True)

    # return both the dataframe and its columns as a list
    return formated_data, list(formated_data.columns)

def hourly_averaged_data(data) :

    # arrays to store the hourly averaged columns and the indices
    hourly_averaged_data = []
    hourly_indices = []

    # initialise the current hour
    current_index = data.index[0]
    current_hour = current_index.hour

    # accumulators to sum the data and count how many data points were summed
    data_accu = np.zeros(len(data.columns))
    counts_accu = np.zeros(len(data.columns))

    # iterate over the indices of the table
    for index, row in data.iterrows() :

        # get the hour of the index
        hour = index.hour

        # if the hour has changed, register the previous hourly mean and index
        if hour != current_hour :
            
            # set NaNs in the counter where value is still 0 at the end of the hour, to indicate no data was registered
            for i in range(len(counts_accu)) :
                if counts_accu[i] == 0 :
                    counts_accu[i] = np.nan
            
            # register the averaged data with a resonable number of decimals
            hourly_averaged_data.append(np.round(data_accu / counts_accu, decimals = 3))
            
            # rebuild the timestamp of the previous hour and store it
            hourly_indices.append(pd.Timestamp(str(current_index.year) + '-' + str(current_index.month) + '-' + str(current_index.day) + ' ' + str(current_index.hour) + ':00'))
            
            # reset the accumulators
            data_accu = np.zeros(len(data.columns))
            counts_accu = np.zeros(len(data.columns))
            
            # store the new index and its hour
            current_index = index
            current_hour = current_index.hour

        # sum the current data accumulator with the current row, where NaNs are replaced with 0
        data_accu = data_accu + np.nan_to_num(np.array(row), nan = 0)

        # add ones to the counter at the indices where the data is not NaN
        counts_accu = counts_accu + np.logical_not(np.isnan(np.array(row)))
    
    # register the last mean from the remaining accumulators, same as in the loop
    for i in range(len(counts_accu)) :
                if counts_accu[i] == 0 :
                    counts_accu[i] = np.nan
    hourly_averaged_data.append(np.round(data_accu / counts_accu, decimals = 3))
    hourly_indices.append(pd.Timestamp(str(current_index.year) + '-' + str(current_index.month) + '-' + str(current_index.day) + ' ' + str(current_index.hour) + ':00'))
    
    # return a dataframe formed with the hourly averages, the new hourly indices, and the columns of the input data
    return pd.DataFrame(hourly_averaged_data, index = hourly_indices, columns = data.columns, dtype = float)