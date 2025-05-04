import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

path = '/Users/yanngirodo/Desktop/Svalbard/cours/AGF212/report/Met_Data/Tiny_tags/csv'

air_temperatures = ['TH5-Temperature', 'TH6-Temperature', 'TH3-Temperature', 'TH2-Temperature', 'TH8-Temperature']
air_humidities = ['TH5-Humidity', 'TH6-Humidity', 'TH3-Humidity', 'TH2-Humidity', 'TH8-Humidity']
snow_pit_tellbreen = ['TT2-Black Probe Temperature', 'TT14-Black Probe Temperature', 'TT4-Black Probe Temperature', 'TT2-White Probe Temperature', 'TT14-White Probe Temperature', 'TT4-White Probe Temperature']
snow_pit_blekumbreen = ['TT9-Black Probe Temperature', 'TT6-Black Probe Temperature', 'TT13-Black Probe Temperature', 'TT9-White Probe Temperature','TT6-White Probe Temperature', 'TT13-White Probe Temperature']

start_times = {'TH2' : pd.Timestamp('2025-03-04 14:00:00'),
               'TH3' : pd.Timestamp('2025-03-01 14:00:00'),
               'TH5' : pd.Timestamp('2025-03-01 14:00:00'),
               'TH6' : pd.Timestamp('2025-03-04 12:00:00'),
               'TH8' : pd.Timestamp('2025-03-01 14:00:00'),
               'TT2' : pd.Timestamp('2025-03-01 15:00:00'),
               'TT4' : pd.Timestamp('2025-03-01 15:00:00'),
               'TT6' : pd.Timestamp('2025-03-04 14:00:00'),
               'TT9' : pd.Timestamp('2025-03-04 14:00:00'),
               'TT13' : pd.Timestamp('2025-03-04 14:00:00'),
               'TT14' : pd.Timestamp('2025-03-01 15:00:00')}

stop_times = {'TH2' : pd.Timestamp('2025-03-10 12:00:00'),
              'TH3' : pd.Timestamp('2025-03-10 12:00:00'),
              'TH5' : pd.Timestamp('2025-03-10 12:00:00'),
              'TH6' : pd.Timestamp('2025-03-10 12:00:00'),
              'TH8' : pd.Timestamp('2025-03-10 12:00:00'),
              'TT2' : pd.Timestamp('2025-03-10 10:00:00'),
              'TT4' : pd.Timestamp('2025-03-10 10:00:00'),
              'TT6' : pd.Timestamp('2025-03-10 09:00:00'),
              'TT9' : pd.Timestamp('2025-03-10 09:00:00'),
              'TT13' : pd.Timestamp('2025-03-10 09:00:00'),
              'TT14' : pd.Timestamp('2025-03-10 10:00:00')}

def get_data(name) :

    # array that will store the data
    data = []

    # iterate over lines of the specific file at the given path
    with open(path + '/' + name, 'r', errors = 'ignore') as file :
        for line in file :

            # split the values in the line and strip it from spaces, return characters, and quotation marks
            formated_line = line.strip().split(',')[1:]
            for k in range(1, len(formated_line)) : formated_line[k] = formated_line[k].strip(' C%RH')

            # check for the 5 first characters, which should be the beginning of a time stamp, and if so, add the line to the data array
            if formated_line[0][:5] == '2025-' : data.append(formated_line)
    
    return data

def get_columns(name) :

    # open the file at the given path to read its overhead
    with open(path + '/' + name, 'r', errors = 'ignore') as file :
        
        # get the 5 first lines, split and strip them
        i = 0
        while i < 5 :
            formated_line = file.readline().strip().split(',')
            
            # fith line contains the name of the data at the 3rd and 4th positions
            if i == 4 : columns = formated_line[2:]
            
            i += 1
    
    # add the name of the sensor, which is the name of the file without extension, to the beginning of each column
    return [name[:-4] + '-' + col for col in columns]

def get_dataframe(data, columns) :

    # split the data into time stamps (which will be used as indices of the dataframe), and actual numerical values
    data = np.array(data)
    time_stamps = data[:, 0]
    values = data[:, 1:]

    # set time stamps to a proper timestamp type
    time_stamps = [pd.Timestamp(str(ts)) for ts in time_stamps]

    # generate the pandas dataframe
    formated_data = pd.DataFrame(data = values, index = time_stamps, columns = columns, dtype = float)

    return formated_data

def import_data() :

    # list to store all the dataframes
    dataframes = []

    # get dataframes from all sensors
    for name in os.listdir(path) : dataframes.append(get_dataframe(get_data(name), get_columns(name)))

    # concatenate the 4 dataframes columns by columns, filling the incomplete time stamps with NaN values
    formated_data = pd.concat(dataframes, axis = 1, join = 'outer')

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
    
    # got through all indices and columns to remove the samples outside of the actual measurement period
    for index in range(len(hourly_indices)) :
        for column in range(len(data.columns)) :
            if hourly_indices[index] < start_times[data.columns[column].split('-')[0]] or hourly_indices[index] > stop_times[data.columns[column].split('-')[0]] :
                hourly_averaged_data[index][column] = np.nan

    # return a dataframe formed with the hourly averages, the new hourly indices, and the columns of the input data
    return pd.DataFrame(hourly_averaged_data, index = hourly_indices, columns = data.columns, dtype = float)