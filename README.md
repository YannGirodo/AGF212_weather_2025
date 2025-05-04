# AGF212_weather_2025
Data and scripts of the 2025 AGF212 fieldwork weather group

Folder Met_Data contains raw data from stations and TinyTags.
Folder positions contains screenshots of the GPS coordinates of the TinyTags and stations.
Files ws_data.py and tt_data.py allow to convert raw data into readable csv files, ws_data.csv and tt_data.csv .
Files ws_hourly.py and tt_hourly.py allow to generate hourly-averaged csv files, ws_hourly.csv and tt_hourly.csv .
File ERA5.py takes raw data from ERA5 csv files ERA5_hourly_BB.csv and ERA5_hourly_TB.csv, and provides a function to import it as a pandas dataframe.
Files tools.py, plots.py, and main.py provide functions to plot the data, using the other data files and scripts.

Folders Tora and Freddy contain programs written by them, on wind data for Freddy, on surface energy balance for Tora.
They used slightly different formats for the csv files, so these files are given in there respective folders.

You will have to modify data path if you want to use these scripts.
