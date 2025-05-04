import pandas as pd
import matplotlib.pyplot as plt

def load_csv(name) :

    # path to the report folder where the csv file should be
    path = '/Users/yanngirodo/Desktop/Svalbard/cours/AGF212/report'

    # read the specific csv using the name passed in argument
    data = pd.read_csv(path + '/' + name, index_col = 0)

    # replace all the indices with timestamps objects
    for index in data.index : data.rename({index : pd.Timestamp(index)}, axis = 0, inplace = True)

    # return the dataframe and its columns
    return data, list(data.columns)

def plot(data, columns, name) :
    
    # create figure with name
    fig = plt.figure(name, figsize = (11, 7))

    # create axes for the figure
    ax = fig.subplots()

    # plot the wanted columns from the dataframe all on the same axes
    if isinstance(columns, str) :
        data.plot(y = columns, use_index = True, ax = ax, rot = 45)
    else :
        for column in columns : data.plot(y = column, use_index = True, ax = ax, rot = 45)