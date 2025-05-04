import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from windrose import WindroseAxes
from matplotlib import cm
import math

##IN-SITU

path = '/Users/yanngirodo/Desktop/Svalbard/cours/AGF212/report/Freddy/ws_hourly.csv'

def load_csv(path) :
    data = pd.read_csv(path, index_col = 0)
    for index in data.index : data.rename({index : pd.Timestamp(index)}, axis = 0, inplace = True) # Convert the index to datetime. The indexes are are the dates in the CSV filed that we are running the for loop over. Each time index replaced by time stamps.
    return data, list(data.columns)

data, columns = load_csv(path)

print(columns)
print(data)


df, _ = load_csv(path) # Load the data from the CSV file

Windspeed_TEL = df['TEL-wind_speed@335'] # Extract wind speed
Winddirection_TEL = df['TEL-wind_direction@335'] # Extract wind direction
Windspeed_BLE = df['BLE-wind_speed@335'] # Extract wind speed
Winddirection_BLE = df['BLE-wind_direction@335'] # Extract wind direction
# Create a figure with two subplots
fig, axs = plt.subplots(2, 1, figsize=(10, 8))



# Plot windspeed
axs[0].plot(df.index, Windspeed_TEL, label='TB Windspeed', color='red') #axs is an array with axs[0] and axs[1] as the two subplots
axs[0].plot(df.index, Windspeed_BLE, label='BB Windspeed', color='darkblue')
axs[0].set_title('Windspeed')
axs[0].set_xlabel('Date')
axs[0].set_ylabel('Windspeed (m/s)')
axs[0].legend()
axs[0].grid()

# Plot wind direction
axs[1].scatter(df.index, Winddirection_TEL, label='TB Wind Direction', color='red', s=5)
axs[1].scatter(df.index, Winddirection_BLE, label='BB Wind Direction', color='darkblue',s=5)
axs[1].set_title('Wind Direction')
axs[1].set_xlabel('Date')
axs[1].set_ylabel('Wind Direction (degrees)')
axs[1].legend()
axs[1].grid()

plt.tight_layout()
############################################################################################################
fig, axs = plt.subplots(2, 1, figsize=(10, 8))
# Plot windspeed TB
axs[0].plot(df.index, Windspeed_TEL, label='TB Windspeed', color='red') #axs is an array with axs[0] and axs[1] as the two subplots
axs[0].set_title('Windspeed TB')
axs[0].set_xlabel('Date')
axs[0].set_ylabel('Windspeed (m/s)')
axs[0].legend()
axs[0].grid()

# Plot wind direction TB
axs[1].scatter(df.index, Winddirection_TEL, label='TB Wind Direction', color='red', s=5)
axs[1].set_title('Wind Direction TB')
axs[1].set_xlabel('Date')
axs[1].set_ylabel('Wind Direction (degrees)')
axs[1].legend()
axs[1].grid()

fig, axs = plt.subplots(2, 1, figsize=(10, 8))
# Plot windspeed BB
axs[0].plot(df.index, Windspeed_BLE, label='BB Windspeed', color='darkblue')
axs[0].set_title('Windspeed BB')
axs[0].set_xlabel('Date')
axs[0].set_ylabel('Windspeed (m/s)')
axs[0].legend()
axs[0].grid()

# Plot wind direction BB

axs[1].scatter(df.index, Winddirection_BLE, label='BB Wind Direction', color='darkblue',s=5)
axs[1].set_title('Wind Direction BB')
axs[1].set_xlabel('Date')
axs[1].set_ylabel('Wind Direction (degrees)')
axs[1].legend()
axs[1].grid()

############################################################################################################
##ERA5
fig, axs = plt.subplots(2, 1, figsize=(10, 8))

df_TB = pd.read_csv('/Users/yanngirodo/Desktop/Svalbard/cours/AGF212/report/Freddy/ERA5-LandHourly_allVariables-TB-FINAL.csv') # Load the data from the CSV file
df_TB = df_TB.dropna() # Drop any rows with missing values
Windspeed_TB = np.sqrt(df_TB['u_component_of_wind_10m']**2 + df_TB['v_component_of_wind_10m']**2) # Calculate wind speed
Winddirection_TB = (180 + 180/np.pi * np.arctan2(df_TB['u_component_of_wind_10m'], df_TB['v_component_of_wind_10m'])) % 360 # Calculate wind direction

df_BB = pd.read_csv('/Users/yanngirodo/Desktop/Svalbard/cours/AGF212/report/Freddy/ERA5-LandHourly_allVariables-BB-FINAL.csv') # Load the data from the CSV file
df_BB = df_BB.dropna() # Drop any rows with missing values
Windspeed_BB = np.sqrt(df_BB['u_component_of_wind_10m']**2 + df_BB['v_component_of_wind_10m']**2)
Winddirection_BB = (180 + 180/np.pi * np.arctan2(df_BB['u_component_of_wind_10m'], df_BB['v_component_of_wind_10m'])) % 360

# Ensure the index is datetime for proper plotting
df_TB['time'] = pd.to_datetime(df_TB['date']) #The to_datetime() function converts the date column into datetime objects and stores them in a new column named time.'
df_BB['time'] = pd.to_datetime(df_BB['date'])

# Plot windspeed
axs[0].plot(df_TB['time'], Windspeed_TB, label='TB Windspeed (ERA5)', color='red',alpha = 0.3,) # Add ERA5 data to the plot
axs[0].plot(df_BB['time'], Windspeed_BB, label='BB Windspeed (ERA5)', color='lightblue')
axs[0].legend()
axs[0].set_title('Windspeed ERA5')
axs[0].set_xlabel('Date')
axs[0].set_ylabel('Windspeed (m/s)')
axs[0].grid()

# Plot wind direction
axs[1].scatter(df_TB['time'], Winddirection_TB, label='TB Wind Direction (ERA5)', color='red',alpha = 0.3,s=5)
axs[1].scatter(df_BB['time'], Winddirection_BB, label='BB Wind Direction (ERA5)', color='lightblue',s=5)
axs[1].legend()
axs[1].set_title('Wind Direction ERA5')
axs[1].set_xlabel('Date')
axs[1].set_ylabel('Wind Direction (degrees)')
axs[1].grid()

plt.tight_layout()

############################################################################################################
# # Overlay ERA5 data on In-Situ data  
# fig, axs = plt.subplots(2, 1, figsize=(10, 8))

# # Plot windspeed
# axs[0].plot(df.index, Windspeed_TEL, label='TB Windspeed (In-Situ)', color='r')
# axs[0].plot(df.index, Windspeed_BLE, label='BB Windspeed (In-Situ)', color='b')
# axs[0].plot(df_TB['time'], Windspeed_TB, label='TB Windspeed (ERA5)', color='r',alpha = 0.3, linestyle='--')
# axs[0].plot(df_BB['time'], Windspeed_BB, label='BB Windspeed (ERA5)', color='b',alpha = 0.3, linestyle='--')
# # axs[0].set_title('Windspeed Comparison')
# # axs[0].set_xlabel('Date')
# axs[0].set_ylabel('Windspeed (m/s)')
# axs[0].legend()
# axs[0].grid()
# axs[0].xaxis.set_ticklabels([])

# # Plot wind direction
# axs[1].scatter(df.index, Winddirection_TEL, label='TB Wind Direction (In-Situ)', color='r',s=5)
# axs[1].scatter(df.index, Winddirection_BLE, label='BB Wind Direction (In-Situ)', color='b',s=5)
# axs[1].scatter(df_TB['time'], Winddirection_TB, label='TB Wind Direction (ERA5)', color='r',alpha = 0.3,s=4)
# axs[1].scatter(df_BB['time'], Winddirection_BB, label='BB Wind Direction (ERA5)', color='b',alpha = 0.3,s=4)
# # axs[1].set_title('Wind Direction Comparison')
# axs[1].set_xlabel('Date')
# axs[1].set_ylabel('Wind Direction (degrees)')
# axs[1].legend()
# axs[1].grid()
# axs[1].tick_params(axis = 'x', rotation = 30)

# plt.tight_layout()

fig, axs = plt.subplots(1, 1, figsize=(10, 4))

axs.plot(df.index, Windspeed_TEL, label='TB Windspeed (In-Situ)', color='r')
axs.plot(df.index, Windspeed_BLE, label='BB Windspeed (In-Situ)', color='b')
axs.plot(df_TB['time'], Windspeed_TB, label='TB Windspeed (ERA5)', color='r',alpha = 0.3, linestyle='--')
axs.plot(df_BB['time'], Windspeed_BB, label='BB Windspeed (ERA5)', color='b',alpha = 0.3, linestyle='--')
# axs.set_title('Windspeed Comparison')
axs.set_xlabel('Date')
axs.set_ylabel('Windspeed (m/s)')
axs.legend()
axs.grid()
axs.tick_params(axis = 'x', rotation = 30)

plt.tight_layout()

plt.savefig('wind_timeseries1.pdf', format = 'pdf')

fig, axs = plt.subplots(1, 1, figsize=(10, 4))

# Plot wind direction
axs.scatter(df.index, Winddirection_TEL, label='TB Wind Direction (In-Situ)', color='r',s=5)
axs.scatter(df.index, Winddirection_BLE, label='BB Wind Direction (In-Situ)', color='b',s=5)
axs.scatter(df_TB['time'], Winddirection_TB, label='TB Wind Direction (ERA5)', color='r',alpha = 0.3,s=4)
axs.scatter(df_BB['time'], Winddirection_BB, label='BB Wind Direction (ERA5)', color='b',alpha = 0.3,s=4)
# axs.set_title('Wind Direction Comparison')
axs.set_xlabel('Date')
axs.set_ylabel('Wind Direction (degrees)')
axs.legend()
axs.grid()
axs.tick_params(axis = 'x', rotation = 30)

plt.tight_layout()

plt.savefig('wind_timeseries2.pdf', format = 'pdf')

############################################################################################################
#ERA5 BB vs BB and ERA5 TB vs TB
fig, axs = plt.subplots(4, 1, figsize=(10, 8))
axs[0].plot(df.index, Windspeed_TEL, label='TB Windspeed (In-Situ)', color='red')
axs[0].plot(df_TB['time'], Windspeed_TB, label='TB Windspeed (ERA5)', color='red',alpha = 0.3, linestyle='--')
axs[0].set_title('TB Windspeed Comparison')
axs[0].set_xlabel('Date')
axs[0].set_ylabel('Windspeed (m/s)')
axs[0].legend()
axs[0].grid()

axs[1].plot(df.index, Windspeed_BLE, label='BB Windspeed (In-Situ)', color='darkblue')
axs[1].plot(df_BB['time'], Windspeed_BB, label='BB Windspeed (ERA5)', color='lightblue', linestyle='--')
axs[1].set_title('BB Windspeed Comparison')
axs[1].set_xlabel('Date')
axs[1].set_ylabel('Windspeed (m/s)')
axs[1].legend()
axs[1].grid()


axs[2].scatter(df.index, Winddirection_TEL, label='TB Wind Direction (In-Situ)', color='red',s=5)
axs[2].scatter(df_TB['time'], Winddirection_TB, label='TB Wind Direction (ERA5)', color='red',alpha = 0.3, s=5)
axs[2].set_title('TB Wind Direction Comparison')
axs[2].set_xlabel('Date')
axs[2].set_ylabel('Wind Direction (degrees)')
axs[2].legend()
axs[2].grid()

axs[3].scatter(df.index, Winddirection_BLE, label='BB Wind Direction (In-Situ)', color='darkblue',s=5)
axs[3].scatter(df_BB['time'], Winddirection_BB, label='BB Wind Direction (ERA5)', color='lightblue',s=5)
axs[3].set_title('BB Wind Direction Comparison')
axs[3].set_xlabel('Date')
axs[3].set_ylabel('Wind Direction (degrees)')
axs[3].legend()
axs[3].grid()

plt.tight_layout()
plt.show()

