import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from windrose import WindroseAxes
from matplotlib import cm
import math

#ERA5 - TB
df = pd.read_csv('/Users/yanngirodo/Desktop/Svalbard/cours/AGF212/report/Freddy/ERA5-LandHourly_allVariables-TB-FINAL.csv') # Load the data from the CSV file
df = df.dropna() # Drop any rows with missing values
ax = WindroseAxes.from_ax() # Create a wind rose plotting area
Windspeed_TB = np.sqrt(df['u_component_of_wind_10m']**2 + df['v_component_of_wind_10m']**2) # Calculate wind speed
Winddirection_TB = (180 + 180/np.pi * np.arctan2(df['u_component_of_wind_10m'], df['v_component_of_wind_10m'])) % 360 # Calculate wind direction
ax.bar(Winddirection_TB, Windspeed_TB, normed=True, opening=0.8, edgecolor='white', cmap=cm.viridis) # Plot wind speed and direction as a wind rose
ax.set_title('ERA5 - Tellbreen Wind', loc='center') 
ax.legend(loc='upper right', title="Wind Speed (m/s)")
plt.savefig('windrose_ERA5_TB.pdf', format = 'pdf')

#ERA5 - BB
df = pd.read_csv('/Users/yanngirodo/Desktop/Svalbard/cours/AGF212/report/Freddy/ERA5-LandHourly_allVariables-BB-FINAL.csv') # Load the data from the CSV file
df = df.dropna() # Drop any rows with missing values
ax = WindroseAxes.from_ax() # Create a wind rose plotting area
Windspeed_TB = np.sqrt(df['u_component_of_wind_10m']**2 + df['v_component_of_wind_10m']**2) # Calculate wind speed
Winddirection_TB = (180 + 180/np.pi * np.arctan2(df['u_component_of_wind_10m'], df['v_component_of_wind_10m'])) % 360 # Calculate wind direction
ax.bar(Winddirection_TB, Windspeed_TB, normed=True, opening=0.8, edgecolor='white', cmap=cm.viridis) # Plot wind speed and direction as a wind rose
ax.set_title('ERA5 - Blekumbreen Wind', loc='center')
ax.legend(loc='upper right', title="Wind Speed (m/s)")
plt.savefig('windrose_ERA5_BB.pdf', format = 'pdf')

# In-situ

path = '/Users/yanngirodo/Desktop/Svalbard/cours/AGF212/report/ws_hourly.csv'

def load_csv(path) :
    data = pd.read_csv(path, index_col = 0)
    for index in data.index : data.rename({index : pd.Timestamp(index)}, axis = 0, inplace = True) # Convert the index to datetime. The indexes are are the dates in the CSV filed that we are running the for loop over. Each time index replaced by time stamps.
    return data, list(data.columns)

data, columns = load_csv(path)

print(columns)
print(data)

#TB
df = pd.read_csv(path) # Load the data from the CSV file
df = df.dropna() # Drop any rows with missing values
ax = WindroseAxes.from_ax() # Create a wind rose plotting area
Windspeed = df['TEL-wind_speed@335'] # Extract wind speed
Winddirection = df['TEL-wind_direction@335'] # Extract wind direction
cmap = ax.bar(Winddirection, Windspeed, normed=True, opening=0.8, edgecolor='white', cmap=cm.viridis) # Plot wind speed and direction as a wind rose
ax.set_title('Tellbreen Wind', loc='center') # Set the title in the center
ax.set_title('Tellbreen Wind', loc='center')
ax.legend(loc='upper right', title="Wind Speed (m/s)")
plt.savefig('windrose_WS_TB.pdf', format = 'pdf')

#BB
df = pd.read_csv(path) # Load the data from the CSV file
df = df.dropna() # Drop any rows with missing values
ax = WindroseAxes.from_ax() # Create a wind rose plotting area
Windspeed = df['BLE-wind_speed@335'] # Extract wind speed
Winddirection = df['BLE-wind_direction@335'] # Extract wind direction
ax.bar(Winddirection, Windspeed, normed=True, opening=0.8, edgecolor='white', cmap=cm.viridis) # Plot wind speed and direction as a wind rose
ax.set_title('Blekumbreen Wind', loc='center') # Set the title in the center
ax.set_title('Blekumbreen Wind', loc='center')
ax.legend(loc='upper right', title="Wind Speed (m/s)")
plt.savefig('windrose_WS_BB.pdf', format = 'pdf')
plt.show() # Display the plot