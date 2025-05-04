import numpy as np
import pandas as pd

path = '/Users/yanngirodo/Desktop/Svalbard/cours/AGF212/report/'

tellbreen_path = path + 'ERA5_hourly_TB.csv'
blekumbreen_path = path + 'ERA5_hourly_BB.csv'

drops = ['system:index',
         'centroidLatLon',
         'siteName',
         'surface_latent_heat_flux',
         'surface_net_solar_radiation',
         'surface_net_thermal_radiation',
         'surface_sensible_heat_flux',
         'surface_solar_radiation_downwards',
         'surface_thermal_radiation_downwards',
         'snow_albedo',
         'system:time_start',
         '.geo']

name_map = {'temperature_2m'                             : 'temperature@200',
            'wind_speed@1000'                            : 'wind_speed@1000',
            'wind_direction@1000'                        : 'wind_direction@1000',
            'surface_pressure'                           : 'air_pressure',
            'temperature_of_snow_layer'                  : 'ground_temperature',
            'SW_up'                                      : 'SW_up',
            'surface_solar_radiation_downwards_hourly'   : 'SW_down',
            'surface_net_solar_radiation_hourly'         : 'SW_net',
            'LW_up'                                      : 'LW_up',
            'surface_net_thermal_radiation_hourly'       : 'LW_net',
            'surface_thermal_radiation_downwards_hourly' : 'LW_down',
            'surface_latent_heat_flux_hourly'            : 'latent',
            'surface_sensible_heat_flux_hourly'          : 'sensible'}

snow_emissivity = 0.98
Kelvin = 273.15
Watt = 60 * 60
Pascal = 100

couples = {'TEL-temperature@200'     : 'TEL-temperature@200',
           'TEL-wind_speed@1000'     : 'TEL-wind_speed@335',
           'TEL-wind_direction@1000' : 'TEL-wind_direction@335',
           'TEL-air_pressure'        : 'TEL-air_pressure',
           'TEL-ground_temperature'  : 'TEL-ground_temperature',
           'TEL-SW_up'               : 'TEL-SW_up',
           'TEL-SW_down'             : 'TEL-SW_down',
           'TEL-LW_up'               : 'TEL-LW_up',
           'TEL-LW_down'             : 'TEL-LW_down',
           'BLE-temperature@200'     : 'BLE-temperature@200',
           'BLE-wind_speed@1000'     : 'BLE-wind_speed@335',
           'BLE-wind_direction@1000' : 'BLE-wind_direction@335',
           'BLE-air_pressure'        : 'BLE-air_pressure',
           'BLE-ground_temperature'  : 'BLE-ground_temperature',
           'BLE-SW_up'               : 'BLE-SW_up',
           'BLE-SW_down'             : 'BLE-SW_down',
           'BLE-LW_up'               : 'BLE-LW_up',
           'BLE-LW_down'             : 'BLE-LW_down'}

def import_data() :

    # get dataframes from the csv files of the glaciers
    tellbreen_df = pd.read_csv(tellbreen_path, index_col = 2)
    blekumbreen_df = pd.read_csv(blekumbreen_path, index_col = 2)

    # remove unneeded columns
    for drop in drops : tellbreen_df.drop(columns = drop, inplace = True)
    for drop in drops : blekumbreen_df.drop(columns = drop, inplace = True)

    # replace all the indices with timestamps objects
    for index in tellbreen_df.index : tellbreen_df.rename({index : pd.Timestamp(index)}, axis = 0, inplace = True)
    for index in blekumbreen_df.index : blekumbreen_df.rename({index : pd.Timestamp(index)}, axis = 0, inplace = True)

    # replace u and v wind components with wind speed and direction for both glaciers
    tellbreen_wind_u = tellbreen_df['u_component_of_wind_10m']
    tellbreen_wind_v = tellbreen_df['v_component_of_wind_10m']
    tellbreen_wind_speed = np.sqrt(tellbreen_wind_u**2 + tellbreen_wind_v**2)
    tellbreen_wind_direction = np.mod(180 + 180 * np.atan2(tellbreen_wind_u, tellbreen_wind_v) / np.pi, 360)
    tellbreen_df['wind_speed@1000'] = tellbreen_wind_speed
    tellbreen_df['wind_direction@1000'] = tellbreen_wind_direction
    tellbreen_df.drop('u_component_of_wind_10m', axis = 1, inplace = True)
    tellbreen_df.drop('v_component_of_wind_10m', axis = 1, inplace = True)

    blekumbreen_wind_u = blekumbreen_df['u_component_of_wind_10m']
    blekumbreen_wind_v = blekumbreen_df['v_component_of_wind_10m']
    blekumbreen_wind_speed = np.sqrt(blekumbreen_wind_u**2 + blekumbreen_wind_v**2)
    blekumbreen_wind_direction = np.mod(180 + 180 * np.atan2(blekumbreen_wind_u, blekumbreen_wind_v) / np.pi, 360)
    blekumbreen_df['wind_speed@1000'] = blekumbreen_wind_speed
    blekumbreen_df['wind_direction@1000'] = blekumbreen_wind_direction
    blekumbreen_df.drop('u_component_of_wind_10m', axis = 1, inplace = True)
    blekumbreen_df.drop('v_component_of_wind_10m', axis = 1, inplace = True)

    # add LW and SW up, and drop LW and SW net for both glaciers
    tellbreen_SW_down = tellbreen_df['surface_solar_radiation_downwards_hourly']
    tellbreen_SW_net = tellbreen_df['surface_net_solar_radiation_hourly']
    tellbreen_SW_up = tellbreen_SW_down - tellbreen_SW_net
    tellbreen_df['SW_up'] = tellbreen_SW_up

    tellbreen_LW_down = tellbreen_df['surface_thermal_radiation_downwards_hourly']
    tellbreen_LW_net = tellbreen_df['surface_net_thermal_radiation_hourly']
    tellbreen_LW_up = tellbreen_LW_down - tellbreen_LW_net
    tellbreen_df['LW_up'] = tellbreen_LW_up

    blekumbreen_SW_down = blekumbreen_df['surface_solar_radiation_downwards_hourly']
    blekumbreen_SW_net = blekumbreen_df['surface_net_solar_radiation_hourly']
    blekumbreen_SW_up = blekumbreen_SW_down - blekumbreen_SW_net
    blekumbreen_df['SW_up'] = blekumbreen_SW_up

    blekumbreen_LW_down = blekumbreen_df['surface_thermal_radiation_downwards_hourly']
    blekumbreen_LW_net = blekumbreen_df['surface_net_thermal_radiation_hourly']
    blekumbreen_LW_up = blekumbreen_LW_down - blekumbreen_LW_net
    blekumbreen_df['LW_up'] = blekumbreen_LW_up

    # reorder and rename columns using the name map
    tellbreen_df = tellbreen_df.reindex(name_map.keys(), axis = 1)
    blekumbreen_df = blekumbreen_df.reindex(name_map.keys(), axis = 1)
    tellbreen_df.rename(name_map, axis = 1, inplace = True)
    blekumbreen_df.rename(name_map, axis = 1, inplace = True)

    # set the temperatures in Celsius
    tellbreen_df['temperature@200'] = tellbreen_df['temperature@200'] - Kelvin
    blekumbreen_df['temperature@200'] = blekumbreen_df['temperature@200'] - Kelvin
    tellbreen_df['ground_temperature'] = tellbreen_df['ground_temperature'] - Kelvin
    blekumbreen_df['ground_temperature'] = blekumbreen_df['ground_temperature'] - Kelvin

    # set the pressure in hPa
    tellbreen_df['air_pressure'] = tellbreen_df['air_pressure'] / Pascal
    blekumbreen_df['air_pressure'] = blekumbreen_df['air_pressure'] / Pascal

    # set the heat fluxes in W/m^2
    tellbreen_df['SW_up'] = tellbreen_df['SW_up'] / Watt
    tellbreen_df['SW_down'] = tellbreen_df['SW_down'] / Watt
    tellbreen_df['SW_net'] = tellbreen_df['SW_net'] / Watt
    tellbreen_df['LW_up'] = tellbreen_df['LW_up'] / Watt
    tellbreen_df['LW_down'] = tellbreen_df['LW_down'] / Watt
    tellbreen_df['LW_net'] = tellbreen_df['LW_net'] / Watt
    tellbreen_df['sensible'] = tellbreen_df['sensible'] / Watt
    tellbreen_df['latent'] = tellbreen_df['latent'] / Watt
    blekumbreen_df['SW_up'] = blekumbreen_df['SW_up'] / Watt
    blekumbreen_df['SW_down'] = blekumbreen_df['SW_down'] / Watt
    blekumbreen_df['SW_net'] = blekumbreen_df['SW_net'] / Watt
    blekumbreen_df['LW_up'] = blekumbreen_df['LW_up'] / Watt
    blekumbreen_df['LW_down'] = blekumbreen_df['LW_down'] / Watt
    blekumbreen_df['LW_net'] = blekumbreen_df['LW_net'] / Watt
    blekumbreen_df['sensible'] = blekumbreen_df['sensible'] / Watt
    blekumbreen_df['latent'] = blekumbreen_df['latent'] / Watt

    # add a prefix to the columns to identify which glacier the variable comes from
    for column in tellbreen_df.columns : tellbreen_df.rename({column : 'TEL-' + column}, axis = 1, inplace = True)
    for column in blekumbreen_df.columns : blekumbreen_df.rename({column : 'BLE-' + column}, axis = 1, inplace = True)

    # concatenate the dataframes columns by columns, filling the incomplete time stamps with NaN values
    formated_data = pd.concat([tellbreen_df, blekumbreen_df], axis = 1, join = 'outer')

    return formated_data, list(formated_data.columns)