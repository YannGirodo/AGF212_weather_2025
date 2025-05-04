import ERA5
import ws_data
import tt_data
import tools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def compare_ERA5_WS(ERA5_hourly_data, ws_hourly_data) :
    for ERA5_variable, WS_variable in ERA5.couples.items() :
        fig = plt.figure(figsize = (11, 7))
        ax = fig.subplots(1, 1)
        ax.plot(ERA5_hourly_data.index, ERA5_hourly_data[ERA5_variable], label = 'ERA5-' + ERA5_variable, color = 'b')
        ax.plot(ws_hourly_data.index, ws_hourly_data[WS_variable], label = 'WS-' + WS_variable, color = 'r')
        ax.xaxis.set_tick_params(rotation = 45)
        ax.legend()

def show_ws(ws_hourly_data) :
    for column in ws_hourly_data.columns : tools.plot(ws_hourly_data, column, column)

def show_tt(tt_hourly_data) :
    tools.plot(tt_hourly_data, tt_data.air_temperatures, 'air temperatures')
    tools.plot(tt_hourly_data, tt_data.air_humidities, 'air humidities')
    tools.plot(tt_hourly_data, tt_data.snow_pit_tellbreen, 'snow pit tellbreen')
    tools.plot(tt_hourly_data, tt_data.snow_pit_blekumbreen, 'snow pit blekumbreen')

def scatter_ERA5_WS(ERA5_hourly_data, ws_hourly_data, type) :
    
    names = {'TEL-temperature@200' :
                {'name'    : 'Temperature',
                 'glacier' : 'Tellbreen'  },
             'TEL-wind_speed@335' :
                {'name'    : 'Win speed',
                 'glacier' : 'Tellbreen'},
             'TEL-wind_direction@335' :
                {'name'    : 'Wind direction',
                 'glacier' : 'Tellbreen'     },
             'TEL-air_pressure' :
                {'name'    : 'Air pressure',
                 'glacier' : 'Tellbreen'   },
             'TEL-ground_temperature' :
                {'name'    : 'Ground temperature',
                 'glacier' : 'Tellbreen'         },
             'TEL-SW_up' :
                {'name'    : 'SW_up'    ,
                 'glacier' : 'Tellbreen'},
             'TEL-SW_down' :
                {'name'    : 'SW_down'  ,
                 'glacier' : 'Tellbreen'},
             'TEL-LW_up' :
                {'name'    : 'LW_up'    ,
                 'glacier' : 'Tellbreen'},
             'TEL-LW_down' :
                {'name'    : 'LW_down'  ,
                 'glacier' : 'Tellbreen'},
             'BLE-temperature@200' :
                {'name'    : 'Temperature',
                 'glacier' : 'Blekumbreen'},
             'BLE-wind_speed@335' :
                {'name'    : 'Wind speed' ,
                 'glacier' : 'Blekumbreen'},
             'BLE-wind_direction@335' :
                {'name'    : 'Wind direction',
                 'glacier' : 'Blekumbreen'   },
             'BLE-air_pressure' :
                {'name'    : 'Air pressure',
                 'glacier' : 'Blekumbreen' },
             'BLE-ground_temperature' :
                {'name'    : 'Ground temperature',
                 'glacier' : 'Blekumbreen'       },
             'BLE-SW_up' :
                {'name'    : 'SW_up'      ,
                 'glacier' : 'Blekumbreen'},
             'BLE-SW_down' :
                {'name'    : 'SW_down'    ,
                 'glacier' : 'Blekumbreen'},
             'BLE-LW_up' :
                {'name'    : 'LW_up'      ,
                 'glacier' : 'Blekumbreen'},
             'BLE-LW_down' :
                {'name'    : 'LW_down'    ,
                 'glacier' : 'Blekumbreen'}}

    def normalise(data1, data2) :
        data1_min = np.nanmin(data1)
        data1_max = np.nanmax(data1)
        data2_min = np.nanmin(data2)
        data2_max = np.nanmax(data2)
        data_min = min(data1_min, data2_min)
        data_max = max(data1_max, data2_max)
        return (data1 - data_min) / (data_max - data_min), (data2 - data_min) / (data_max - data_min)
    
    def r2(data1, data2) :
        return np.array(pd.concat([data1, data2], axis = 1, join = 'outer').corr())[0, 1]**2

    ws_index = ws_hourly_data.index
    ERA5_index = ERA5_hourly_data.index
    begin_index = max(ERA5_index[0], ws_index[0])
    end_index = min(ERA5_index[-1], ws_index[-1])
    ws_hourly_data_cut = ws_hourly_data[np.logical_and(ws_index >= begin_index, ws_index <= end_index)]
    ERA5_hourly_data_cut = ERA5_hourly_data[np.logical_and(ERA5_index >= begin_index, ERA5_index <= end_index)]
    
    if type == 'full' :
        fig = plt.figure(figsize = (9, 8))
        ax = fig.subplots(1, 1)
        for ERA5_variable, WS_variable in ERA5.couples.items() :
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            WS_data_reduced, ERA5_data_reduced = normalise(ws_hourly_data_cut[WS_variable], ERA5_hourly_data_cut[ERA5_variable])
            ax.scatter(WS_data_reduced, ERA5_data_reduced, s = 2, label = WS_variable, color = 'b' if names[WS_variable]['glacier'] == 'Blekumbreen' else 'r')
        ax.set_xlabel('Normalised WS data')
        ax.set_ylabel('Normalised ERA5 data')
        ax.legend()
        fig.tight_layout()
    
    if type == 'variables' :
        fig = plt.figure(figsize = (22, 22))
        axes = fig.subplots(3, 3)
        i = 0
        for ERA5_variable, WS_variable in ERA5.couples.items() :
            
            WS_data_reduced, ERA5_data_reduced = normalise(ws_hourly_data_cut[WS_variable], ERA5_hourly_data_cut[ERA5_variable])

            line = (i%9)//3
            col = (i%9)%3
            i += 1

            label = WS_variable.split('@')[0] + ' – R2 = ' + str(np.round(r2(WS_data_reduced, ERA5_data_reduced), 4))

            axes[line][col].scatter(WS_data_reduced, ERA5_data_reduced, s = 5, label = label, color = 'b' if names[WS_variable]['glacier'] == 'Blekumbreen' else 'r')

            axes[line][col].set_xlabel('Normalised WS data')
            axes[line][col].set_ylabel('Normalised ERA5 data')
            axes[line][col].legend()
            axes[line][col].set_xlim(0, 1)
            axes[line][col].set_ylim(0, 1)
        
        fig.tight_layout()
    
    if type == 'glaciers' :
        fig = plt.figure(figsize = (15, 8))
        axes = fig.subplots(1, 2)
        for ERA5_variable, WS_variable in ERA5.couples.items() :
            col = int(names[WS_variable]['glacier'] == 'Blekumbreen')
            WS_data_reduced, ERA5_data_reduced = normalise(ws_hourly_data_cut[WS_variable], ERA5_hourly_data_cut[ERA5_variable])
            axes[col].scatter(WS_data_reduced, ERA5_data_reduced, s = 5, label = WS_variable)
            axes[col].set_xlabel('Normalised WS data')
            axes[col].set_ylabel('Normalised ERA5 data')
            axes[col].legend()
            axes[col].set_xlim(0, 1)
            axes[col].set_ylim(0, 1)
        fig.tight_layout()
    
    if type == 'temperature' :

        fig = plt.figure(figsize = (9, 8))
        ax = fig.subplots(1, 1)

        WS_temp_TEL_reduced, ERA5_temp_TEL_reduced = normalise(ws_hourly_data_cut['TEL-temperature@200'], ERA5_hourly_data_cut['TEL-temperature@200'])
        WS_temp_BLE_reduced, ERA5_temp_BLE_reduced = normalise(ws_hourly_data_cut['BLE-temperature@200'], ERA5_hourly_data_cut['BLE-temperature@200'])

        label = 'Tellbreen temperature – R2 = ' + str(np.round(r2(WS_temp_TEL_reduced, ERA5_temp_TEL_reduced), 4))
        ax.scatter(WS_temp_TEL_reduced, ERA5_temp_TEL_reduced, s = 2, label = label, color = 'r')

        label = 'Blekumbreen temperature – R2 = ' + str(np.round(r2(WS_temp_BLE_reduced, ERA5_temp_BLE_reduced), 4))
        ax.scatter(WS_temp_BLE_reduced, ERA5_temp_BLE_reduced, s = 2, label = label, color = 'b')

        ax.set_xlabel('Normalised in-situ temperature')
        ax.set_ylabel('Normalised ERA5 temperature')
        ax.legend()
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.plot([0, 1], [0, 1], c = 'gray', alpha = 0.6, linestyle = '--', linewidth = 0.8)
        ax.grid()

        fig.suptitle('Correlation plot of temperature')
        fig.tight_layout()

    if type == 'wind' :

        # fig = plt.figure(figsize = (15, 8))
        # axes = fig.subplots(1, 2)

        fig = plt.figure(figsize = (8, 7))
        axes = fig.subplots(1, 1)

        WS_wind_speed_TEL_reduced, ERA5_wind_speed_TEL_reduced = normalise(ws_hourly_data_cut['TEL-wind_speed@335'], ERA5_hourly_data_cut['TEL-wind_speed@1000'])
        WS_wind_speed_BLE_reduced, ERA5_wind_speed_BLE_reduced = normalise(ws_hourly_data_cut['BLE-wind_speed@335'], ERA5_hourly_data_cut['BLE-wind_speed@1000'])

        label = 'Tellbreen wind speed – R2 = ' + str(np.round(r2(WS_wind_speed_TEL_reduced, ERA5_wind_speed_TEL_reduced), 4))
        axes.scatter(WS_wind_speed_TEL_reduced, ERA5_wind_speed_TEL_reduced, s = 2, label = label, color = 'r')

        label = 'Blekumbreen wind speed – R2 = ' + str(np.round(r2(WS_wind_speed_BLE_reduced, ERA5_wind_speed_BLE_reduced), 4))
        axes.scatter(WS_wind_speed_BLE_reduced, ERA5_wind_speed_BLE_reduced, s = 2, label = label, color = 'b')

        axes.set_xlabel('Normalised in-situ wind speed')
        axes.set_ylabel('Normalised ERA5 wind speed')
        axes.legend()
        axes.set_xlim(0, 1)
        axes.set_ylim(0, 1)
        axes.plot([0, 1], [0, 1], c = 'gray', alpha = 0.6, linestyle = '--', linewidth = 0.8)
        axes.grid()

        fig.tight_layout()

        plt.savefig('wind_correlation0.pdf', format = 'pdf')

        fig = plt.figure(figsize = (8, 7))
        axes = fig.subplots(1, 1)

        WS_wind_direction_TEL_reduced, ERA5_wind_direction_TEL_reduced = normalise(ws_hourly_data_cut['TEL-wind_direction@335'], ERA5_hourly_data_cut['TEL-wind_direction@1000'])
        WS_wind_direction_BLE_reduced, ERA5_wind_direction_BLE_reduced = normalise(ws_hourly_data_cut['BLE-wind_direction@335'], ERA5_hourly_data_cut['BLE-wind_direction@1000'])

        label = 'Tellbreen wind direction – R2 = ' + str(np.round(r2(WS_wind_direction_TEL_reduced, ERA5_wind_direction_TEL_reduced), 4))
        axes.scatter(WS_wind_direction_TEL_reduced, ERA5_wind_direction_TEL_reduced, s = 2, label = label, color = 'r')

        label = 'Blekumbreen wind direction – R2 = ' + str(np.round(r2(WS_wind_direction_BLE_reduced, ERA5_wind_direction_BLE_reduced), 4))
        axes.scatter(WS_wind_direction_BLE_reduced, ERA5_wind_direction_BLE_reduced, s = 2, label = label, color = 'b')

        axes.set_xlabel('Normalised in-situ wind direction')
        axes.set_ylabel('Normalised ERA5 wind direction')
        axes.legend()
        axes.set_xlim(0, 1)
        axes.set_ylim(0, 1)
        axes.plot([0, 1], [0, 1], c = 'gray', alpha = 0.6, linestyle = '--', linewidth = 0.8)
        axes.grid()

        fig.tight_layout()

        plt.savefig('wind_correlation1.pdf', format = 'pdf')

        # fig.suptitle('Correlation plots of wind variables')
        # fig.tight_layout()

    if type == 'radiation' :

        exclude_begin = pd.Timestamp('2025-03-07 06:00:00')
        exclude_end = pd.Timestamp('2025-03-09 10:00:00')

        fig = plt.figure(figsize = (15, 13))
        axes = fig.subplots(2, 2)

        WS_SW_net_TEL = (ws_hourly_data_cut['TEL-SW_down'] - ws_hourly_data_cut['TEL-SW_up'])
        
        WS_SW_net_BLE = (ws_hourly_data_cut['BLE-SW_down'] - ws_hourly_data_cut['BLE-SW_up']).where(np.logical_or(ws_hourly_data_cut.index < exclude_begin, ws_hourly_data_cut.index > exclude_end))
        ERA5_SW_net_TEL = ERA5_hourly_data_cut['TEL-SW_net'].where(np.logical_or(ERA5_hourly_data_cut.index < exclude_begin, ERA5_hourly_data_cut.index > exclude_end))
        ERA5_SW_net_BLE = ERA5_hourly_data_cut['BLE-SW_net'].where(np.logical_or(ERA5_hourly_data_cut.index < exclude_begin, ERA5_hourly_data_cut.index > exclude_end))
        WS_SW_net_TEL_reduced, ERA5_SW_net_TEL_reduced = normalise(WS_SW_net_TEL, ERA5_SW_net_TEL)
        WS_SW_net_BLE_reduced, ERA5_SW_net_BLE_reduced = normalise(WS_SW_net_BLE, ERA5_SW_net_BLE)

        # axes[0, 0].plot(WS_SW_net_BLE_reduced.index, WS_SW_net_BLE_reduced)
        # axes[0, 0].plot(ERA5_SW_net_BLE_reduced.index, ERA5_SW_net_BLE_reduced, linestyle = '--')

        label = 'Tellbreen SW net – R2 = ' + str(np.round(r2(WS_SW_net_TEL_reduced, ERA5_SW_net_TEL_reduced), 4))
        axes[0, 0].scatter(WS_SW_net_TEL_reduced, ERA5_SW_net_TEL_reduced, s = 2, label = label, color = 'r')

        label = 'Blekumbreen SW net – R2 = ' + str(np.round(r2(WS_SW_net_BLE_reduced, ERA5_SW_net_BLE_reduced), 4))
        axes[0, 0].scatter(WS_SW_net_BLE_reduced, ERA5_SW_net_BLE_reduced, s = 2, label = label, color = 'b')

        axes[0, 0].set_xlabel('Normalised in-situ SW net')
        axes[0, 0].set_ylabel('Normalised ERA5 SW net')
        axes[0, 0].legend()
        axes[0, 0].set_xlim(0, 1)
        axes[0, 0].set_ylim(0, 1)

        WS_LW_net_TEL = (ws_hourly_data_cut['TEL-LW_down'] - ws_hourly_data_cut['TEL-LW_up']).where(np.logical_or(ws_hourly_data_cut.index < exclude_begin, ws_hourly_data_cut.index > exclude_end))
        WS_LW_net_BLE = (ws_hourly_data_cut['BLE-LW_down'] - ws_hourly_data_cut['BLE-LW_up']).where(np.logical_or(ws_hourly_data_cut.index < exclude_begin, ws_hourly_data_cut.index > exclude_end))
        ERA5_LW_net_TEL = ERA5_hourly_data_cut['TEL-LW_net'].where(np.logical_or(ERA5_hourly_data_cut.index < exclude_begin, ERA5_hourly_data_cut.index > exclude_end))
        ERA5_LW_net_BLE = ERA5_hourly_data_cut['BLE-LW_net'].where(np.logical_or(ERA5_hourly_data_cut.index < exclude_begin, ERA5_hourly_data_cut.index > exclude_end))
        WS_LW_net_TEL_reduced, ERA5_LW_net_TEL_reduced = normalise(WS_LW_net_TEL, ERA5_LW_net_TEL)
        WS_LW_net_BLE_reduced, ERA5_LW_net_BLE_reduced = normalise(WS_LW_net_BLE, ERA5_LW_net_BLE)

        # axes[0, 1].plot(WS_LW_net_BLE_reduced.index, WS_LW_net_BLE_reduced)
        # axes[0, 1].plot(ERA5_LW_net_BLE_reduced.index, ERA5_LW_net_BLE_reduced, linestyle = '--')

        label = 'Tellbreen LW net – R2 = ' + str(np.round(r2(WS_LW_net_TEL_reduced, ERA5_LW_net_TEL_reduced), 4))
        axes[0, 1].scatter(WS_LW_net_TEL_reduced, ERA5_LW_net_TEL_reduced, s = 2, label = label, color = 'r')

        label = 'Blekumbreen LW net – R2 = ' + str(np.round(r2(WS_LW_net_BLE_reduced, ERA5_LW_net_BLE_reduced), 4))
        axes[0, 1].scatter(WS_LW_net_BLE_reduced, ERA5_LW_net_BLE_reduced, s = 2, label = label, color = 'b')

        axes[0, 1].set_xlabel('Normalised in-situ LW net')
        axes[0, 1].set_ylabel('Normalised ERA5 LW net')
        axes[0, 1].legend()
        axes[0, 1].set_xlim(0, 1)
        axes[0, 1].set_ylim(0, 1)


        rho_air = 1.293 #[kg/m^3]
        cp = 1004  #[J/kg K]
        Ab_sens = 0.0019 #dimensionless transfer coeff of sensible heat 
        Kelvin = 273.15
        sigma = 5.67 * 10 **(-8)

        WS_wind_speed_TEL = ws_hourly_data_cut['TEL-wind_speed@200']
        WS_temperature_TEL =  ws_hourly_data_cut['TEL-temperature@200']
        WS_LW_up_TEL = ws_hourly_data_cut['TEL-LW_up']
        WS_T_surf_TEL = (WS_LW_up_TEL / sigma)**(1/4) - Kelvin
        WS_sensible_TEL = - rho_air * cp * Ab_sens * WS_wind_speed_TEL * (WS_T_surf_TEL - WS_temperature_TEL)

        WS_wind_speed_BLE = ws_hourly_data_cut['BLE-wind_speed@200']
        WS_temperature_BLE =  ws_hourly_data_cut['BLE-temperature@200']
        WS_LW_up_BLE = ws_hourly_data_cut['BLE-LW_up']
        WS_T_surf_BLE = (WS_LW_up_BLE / sigma)**(1/4) - Kelvin
        WS_sensible_BLE = - rho_air * cp * Ab_sens * WS_wind_speed_BLE * (WS_T_surf_BLE - WS_temperature_BLE)

        WS_sensible_TEL_reduced, ERA5_sensible_TEL_reduced = normalise(WS_sensible_TEL, ERA5_hourly_data_cut['TEL-sensible'])
        WS_sensible_BLE_reduced, ERA5_sensible_BLE_reduced = normalise(WS_sensible_BLE, ERA5_hourly_data_cut['BLE-sensible'])

        # axes[1, 0].plot(WS_sensible_BLE_reduced.index, WS_sensible_BLE_reduced)
        # axes[1, 0].plot(ERA5_sensible_BLE_reduced.index, ERA5_sensible_BLE_reduced, linestyle = '--')

        label = 'Tellbreen sensible heat – R2 = ' + str(np.round(r2(WS_sensible_TEL_reduced, ERA5_sensible_TEL_reduced), 4))
        axes[1, 0].scatter(WS_sensible_TEL_reduced, ERA5_sensible_TEL_reduced, s = 2, label = label, color = 'r')

        label = 'Blekumbreen sensible net – R2 = ' + str(np.round(r2(WS_sensible_BLE_reduced, ERA5_sensible_BLE_reduced), 4))
        axes[1, 0].scatter(WS_sensible_BLE_reduced, ERA5_sensible_BLE_reduced, s = 2, label = label, color = 'b')

        axes[1, 0].set_xlabel('Normalised in-situ sensible heat')
        axes[1, 0].set_ylabel('Normalised ERA5 sensible heat')
        axes[1, 0].legend()
        axes[1, 0].set_xlim(0, 1)
        axes[1, 0].set_ylim(0, 1)


        Ab_lat = 0.0015 #dimensionless transfer coeff of latent heat

        def e_sat(T_C) :
            e0 = 0.6113 #kPa
            Ld_Rv = 6139 #[K] over ice
            T0 = Kelvin
            T = T_C + Kelvin
            return e0 * np.exp(Ld_Rv * ((1/T0) - (1/T))) * 1000

        WS_RH_TEL = ws_hourly_data_cut['TEL-relative_humidity@200']
        WS_e_surf = e_sat(WS_T_surf_TEL)
        WS_e_air = (WS_RH_TEL / 100) * e_sat(WS_temperature_TEL)
        WS_latent_TEL = 22.2 * Ab_lat * WS_wind_speed_TEL * (WS_e_air - WS_e_surf)

        WS_RH_BLE = ws_hourly_data_cut['BLE-relative_humidity@200']
        WS_e_surf = e_sat(WS_T_surf_BLE)
        WS_e_air = (WS_RH_BLE / 100) * e_sat(WS_temperature_BLE)
        WS_latent_BLE = 22.2 * Ab_lat * WS_wind_speed_BLE * (WS_e_air - WS_e_surf)

        WS_latent_TEL_reduced, ERA5_latent_TEL_reduced = normalise(WS_latent_TEL, ERA5_hourly_data_cut['TEL-latent'])
        WS_latent_BLE_reduced, ERA5_latent_BLE_reduced = normalise(WS_latent_BLE, ERA5_hourly_data_cut['BLE-latent'])

        # axes[1, 1].plot(WS_latent_BLE_reduced.index, WS_latent_BLE_reduced)
        # axes[1, 1].plot(ERA5_latent_BLE_reduced.index, ERA5_latent_BLE_reduced, linestyle = '--')

        label = 'Tellbreen latent heat – R2 = ' + str(np.round(r2(WS_latent_TEL_reduced, ERA5_latent_TEL_reduced), 4))
        axes[1, 1].scatter(WS_latent_TEL_reduced, ERA5_latent_TEL_reduced, s = 2, label = label, color = 'r')

        label = 'Blekumbreen latent net – R2 = ' + str(np.round(r2(WS_latent_BLE_reduced, ERA5_latent_BLE_reduced), 4))
        axes[1, 1].scatter(WS_latent_BLE_reduced, ERA5_latent_BLE_reduced, s = 2, label = label, color = 'b')

        axes[1, 1].set_xlabel('Normalised in-situ latent heat')
        axes[1, 1].set_ylabel('Normalised ERA5 latent heat')
        axes[1, 1].legend()
        axes[1, 1].set_xlim(0, 1)
        axes[1, 1].set_ylim(0, 1)

        fig.tight_layout()

        WS_net_total_TEL = WS_SW_net_TEL + WS_LW_net_TEL + WS_latent_TEL + WS_sensible_TEL
        WS_net_total_BLE = WS_SW_net_BLE + WS_LW_net_BLE + WS_latent_BLE + WS_sensible_BLE
        ERA5_net_total_TEL = ERA5_SW_net_TEL + ERA5_LW_net_TEL + ERA5_hourly_data_cut['TEL-latent'] + ERA5_hourly_data_cut['TEL-sensible']
        ERA5_net_total_BLE = ERA5_SW_net_BLE + ERA5_LW_net_BLE + ERA5_hourly_data_cut['BLE-latent'] + ERA5_hourly_data_cut['BLE-sensible']

        WS_net_total_TEL_reduced, ERA5_net_total_TEL_reduced = normalise(WS_net_total_TEL, ERA5_net_total_TEL)
        WS_net_total_BLE_reduced, ERA5_net_total_BLE_reduced = normalise(WS_net_total_BLE, ERA5_net_total_BLE)

        fig = plt.figure(figsize = (11, 7))
        ax = fig.subplots(2, 1)

        ax[0].plot(WS_net_total_TEL.index, WS_net_total_TEL, c = 'r')
        ax[1].plot(WS_net_total_BLE.index, WS_net_total_BLE, c = 'b')
        ax[0].plot(ERA5_net_total_TEL.index, ERA5_net_total_TEL, c = 'r', alpha = 0.3)
        ax[1].plot(ERA5_net_total_BLE.index, ERA5_net_total_BLE, c = 'b', alpha = 0.3)

        ax[0].grid()
        ax[1].grid()

        fig.tight_layout()

        fig = plt.figure(figsize = (11, 7))
        ax = fig.subplots()

        label = 'Tellbreen total heat – R2 = ' + str(np.round(r2(WS_net_total_TEL_reduced, ERA5_net_total_TEL_reduced), 4))
        ax.scatter(WS_net_total_TEL_reduced, ERA5_net_total_TEL_reduced, s = 2, label = label, color = 'r')

        label = 'Blekumbreen total net – R2 = ' + str(np.round(r2(WS_net_total_BLE_reduced, ERA5_net_total_BLE_reduced), 4))
        ax.scatter(WS_net_total_BLE_reduced, ERA5_net_total_BLE_reduced, s = 2, label = label, color = 'b')

        ax.set_xlabel('Normalised in-situ total heat')
        ax.set_ylabel('Normalised ERA5 total heat')
        ax.legend()
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)

        fig.tight_layout()

    if type == 'simple_radiation' :

        def cut_radiation(array) :

            exclude_begin = pd.Timestamp('2025-03-07 06:00:00')
            exclude_end = pd.Timestamp('2025-03-09 10:00:00')
            
            return array.where(np.logical_or(ws_hourly_data_cut.index < exclude_begin, ws_hourly_data_cut.index > exclude_end))

        def day_mean_bias(ERA5_array, WS_array) :

            day_start = 8
            day_end = 15

            WS_array_day = WS_array.where(np.logical_and(WS_array.index.hour >= day_start, WS_array.index.hour <= day_end))
            ERA5_array_day = ERA5_array.where(np.logical_and(ERA5_array.index.hour >= day_start, ERA5_array.index.hour <= day_end))

            return (ERA5_array_day - WS_array_day).mean()
        
        def day_r2(ERA5_array, WS_array) :

            day_start = 8
            day_end = 15

            WS_array_day = WS_array.where(np.logical_and(WS_array.index.hour >= day_start, WS_array.index.hour <= day_end))
            ERA5_array_day = ERA5_array.where(np.logical_and(ERA5_array.index.hour >= day_start, ERA5_array.index.hour <= day_end))

            return r2(WS_array_day, ERA5_array_day)
        
        # fig = plt.figure(figsize = (15, 13))
        # axes = fig.subplots(2, 2)

        fig = plt.figure(figsize = (8, 7))
        axes = fig.subplots(1, 1)

        WS_SW_up_TEL_reduced, ERA5_SW_up_TEL_reduced = normalise(cut_radiation(ws_hourly_data_cut['TEL-SW_up']), cut_radiation(ERA5_hourly_data_cut['TEL-SW_up']))
        WS_SW_up_BLE_reduced, ERA5_SW_up_BLE_reduced = normalise(cut_radiation(ws_hourly_data_cut['BLE-SW_up']), cut_radiation(ERA5_hourly_data_cut['BLE-SW_up']))

        label = 'Tellbreen SW up \nR2 = ' + str(np.round(r2(WS_SW_up_TEL_reduced, ERA5_SW_up_TEL_reduced), 4)) + '\nDay R2 = ' + str(np.round(day_r2(ERA5_SW_up_TEL_reduced, WS_SW_up_TEL_reduced), 4)) + '\nDay mean bias = ' + str(np.round(day_mean_bias(ERA5_SW_up_TEL_reduced, WS_SW_up_TEL_reduced), 4))
        axes.scatter(WS_SW_up_TEL_reduced, ERA5_SW_up_TEL_reduced, s = 2, label = label, color = 'r')

        label = 'Blekumbreen SW up \nR2 = ' + str(np.round(r2(WS_SW_up_BLE_reduced, ERA5_SW_up_BLE_reduced), 4)) + '\nDay R2 = ' + str(np.round(day_r2(ERA5_SW_up_BLE_reduced, WS_SW_up_BLE_reduced), 4)) + '\nDay mean bias = ' + str(np.round(day_mean_bias(ERA5_SW_up_BLE_reduced, WS_SW_up_BLE_reduced), 4))
        axes.scatter(WS_SW_up_BLE_reduced, ERA5_SW_up_BLE_reduced, s = 2, label = label, color = 'b')

        axes.set_xlabel('Normalised in-situ SW up')
        axes.set_ylabel('Normalised ERA5 SW up')
        axes.legend()
        axes.grid()
        axes.plot([0, 1], [0, 1], c = 'gray', alpha = 0.6, linestyle = '--', linewidth = 0.8)
        axes.set_xlim(0, 1)
        axes.set_ylim(0, 1)

        fig.tight_layout()

        plt.savefig('radiation_correlation00.pdf', format = 'pdf')

        # axes[0, 0].plot(WS_SW_up_TEL_reduced.index, WS_SW_up_TEL_reduced, c = 'r')
        # axes[0, 0].plot(ERA5_SW_up_TEL_reduced.index, ERA5_SW_up_TEL_reduced, c = 'r', alpha = 0.4)

        fig = plt.figure(figsize = (8, 7))
        axes = fig.subplots(1, 1)

        WS_SW_down_TEL_reduced, ERA5_SW_down_TEL_reduced = normalise(cut_radiation(ws_hourly_data_cut['TEL-SW_down']), cut_radiation(ERA5_hourly_data_cut['TEL-SW_down']))
        WS_SW_down_BLE_reduced, ERA5_SW_down_BLE_reduced = normalise(cut_radiation(ws_hourly_data_cut['BLE-SW_down']), cut_radiation(ERA5_hourly_data_cut['BLE-SW_down']))

        label = 'Tellbreen SW down \nR2 = ' + str(np.round(r2(WS_SW_down_TEL_reduced, ERA5_SW_down_TEL_reduced), 4)) + '\nDay R2 = ' + str(np.round(day_r2(ERA5_SW_down_TEL_reduced, WS_SW_down_TEL_reduced), 4)) + '\nDay mean bias = ' + str(np.round(day_mean_bias(ERA5_SW_down_TEL_reduced, WS_SW_down_TEL_reduced), 4))
        axes.scatter(WS_SW_down_TEL_reduced, ERA5_SW_down_TEL_reduced, s = 2, label = label, color = 'r')

        label = 'Blekumbreen SW down \nR2 = ' + str(np.round(r2(WS_SW_down_BLE_reduced, ERA5_SW_down_BLE_reduced), 4)) + '\nDay R2 = ' + str(np.round(day_r2(ERA5_SW_down_BLE_reduced, WS_SW_down_BLE_reduced), 4)) + '\nDay mean bias = ' + str(np.round(day_mean_bias(ERA5_SW_down_BLE_reduced, WS_SW_down_BLE_reduced), 4))
        axes.scatter(WS_SW_down_BLE_reduced, ERA5_SW_down_BLE_reduced, s = 2, label = label, color = 'b')

        axes.set_xlabel('Normalised in-situ SW down')
        axes.set_ylabel('Normalised ERA5 SW down')
        axes.legend()
        axes.grid()
        axes.plot([0, 1], [0, 1], c = 'gray', alpha = 0.6, linestyle = '--', linewidth = 0.8)
        axes.set_xlim(0, 1)
        axes.set_ylim(0, 1)

        fig.tight_layout()

        plt.savefig('radiation_correlation01.pdf', format = 'pdf')

        # axes[0, 1].plot(WS_SW_down_TEL_reduced.index, WS_SW_down_TEL_reduced, c = 'r')
        # axes[0, 1].plot(ERA5_SW_down_TEL_reduced.index, ERA5_SW_down_TEL_reduced, c = 'r', alpha = 0.4)

        fig = plt.figure(figsize = (8, 7))
        axes = fig.subplots(1, 1)

        WS_LW_up_TEL_reduced, ERA5_LW_up_TEL_reduced = normalise(cut_radiation(ws_hourly_data_cut['TEL-LW_up']), cut_radiation(ERA5_hourly_data_cut['TEL-LW_up']))
        WS_LW_up_BLE_reduced, ERA5_LW_up_BLE_reduced = normalise(cut_radiation(ws_hourly_data_cut['BLE-LW_up']), cut_radiation(ERA5_hourly_data_cut['BLE-LW_up']))

        label = 'Tellbreen LW up – R2 = ' + str(np.round(r2(WS_LW_up_TEL_reduced, ERA5_LW_up_TEL_reduced), 4))
        axes.scatter(WS_LW_up_TEL_reduced, ERA5_LW_up_TEL_reduced, s = 2, label = label, color = 'r')

        label = 'Blekumbreen LW up – R2 = ' + str(np.round(r2(WS_LW_up_BLE_reduced, ERA5_LW_up_BLE_reduced), 4))
        axes.scatter(WS_LW_up_BLE_reduced, ERA5_LW_up_BLE_reduced, s = 2, label = label, color = 'b')

        axes.set_xlabel('Normalised in-situ LW up')
        axes.set_ylabel('Normalised ERA5 LW up')
        axes.legend()
        axes.grid()
        axes.plot([0, 1], [0, 1], c = 'gray', alpha = 0.6, linestyle = '--', linewidth = 0.8)
        axes.set_xlim(0, 1)
        axes.set_ylim(0, 1)

        fig.tight_layout()

        plt.savefig('radiation_correlation10.pdf', format = 'pdf')

        # axes[1, 0].plot(WS_LW_up_TEL_reduced.index, WS_LW_up_TEL_reduced, c = 'r')
        # axes[1, 0].plot(ERA5_LW_up_TEL_reduced.index, ERA5_LW_up_TEL_reduced, c = 'r', alpha = 0.4)

        fig = plt.figure(figsize = (8, 7))
        axes = fig.subplots(1, 1)

        WS_LW_down_TEL_reduced, ERA5_LW_down_TEL_reduced = normalise(cut_radiation(ws_hourly_data_cut['TEL-LW_down']), cut_radiation(ERA5_hourly_data_cut['TEL-LW_down']))
        WS_LW_down_BLE_reduced, ERA5_LW_down_BLE_reduced = normalise(cut_radiation(ws_hourly_data_cut['BLE-LW_down']), cut_radiation(ERA5_hourly_data_cut['BLE-LW_down']))

        label = 'Tellbreen LW down – R2 = ' + str(np.round(r2(WS_LW_down_TEL_reduced, ERA5_LW_down_TEL_reduced), 4))
        axes.scatter(WS_LW_down_TEL_reduced, ERA5_LW_down_TEL_reduced, s = 2, label = label, color = 'r')

        label = 'Blekumbreen LW down – R2 = ' + str(np.round(r2(WS_LW_down_BLE_reduced, ERA5_LW_down_BLE_reduced), 4))
        axes.scatter(WS_LW_down_BLE_reduced, ERA5_LW_down_BLE_reduced, s = 2, label = label, color = 'b')

        axes.set_xlabel('Normalised in-situ LW down')
        axes.set_ylabel('Normalised ERA5 LW down')
        axes.legend()
        axes.grid()
        axes.plot([0, 1], [0, 1], c = 'gray', alpha = 0.6, linestyle = '--', linewidth = 0.8)
        axes.set_xlim(0, 1)
        axes.set_ylim(0, 1)

        fig.tight_layout()

        plt.savefig('radiation_correlation11.pdf', format = 'pdf')

        # axes[1, 1].plot(WS_LW_down_TEL_reduced.index, WS_LW_down_TEL_reduced, c = 'r')
        # axes[1, 1].plot(ERA5_LW_down_TEL_reduced.index, ERA5_LW_down_TEL_reduced, c = 'r', alpha = 0.4)

        # fig.tight_layout()

def compare_winds(ERA5_hourly_data, ws_hourly_data) :

    ws_index = ws_hourly_data.index
    ERA5_index = ERA5_hourly_data.index
    begin_index = max(ERA5_index[0], ws_index[0])
    end_index = min(ERA5_index[-1], ws_index[-1])
    ws_hourly_data_cut = ws_hourly_data[np.logical_and(ws_index >= begin_index, ws_index <= end_index)]
    ERA5_hourly_data_cut = ERA5_hourly_data[np.logical_and(ERA5_index >= begin_index, ERA5_index <= end_index)]
    
    wind_speed_TEL = ws_hourly_data_cut['TEL-wind_speed@335']
    wind_direction_diff_TEL = np.mod(ERA5_hourly_data_cut['TEL-wind_direction@1000'] - ws_hourly_data_cut['TEL-wind_direction@335'] + 180, 360) - 180
    wind_speed_BLE = ws_hourly_data_cut['BLE-wind_speed@335']
    wind_direction_diff_BLE = np.mod(ERA5_hourly_data_cut['BLE-wind_direction@1000'] - ws_hourly_data_cut['BLE-wind_direction@335'] + 180, 360) - 180

    fig = plt.figure(figsize = (11, 7))
    ax = fig.subplots(1, 1)
    ax.scatter(wind_speed_TEL, wind_direction_diff_TEL, color = 'r', label = 'Tellbreen', s = 5)
    ax.scatter(wind_speed_BLE, wind_direction_diff_BLE, color = 'b', label = 'Blekumbreen', s = 5)
    ax.set_xlabel('in-situ wind speed [m/s]')
    ax.set_ylabel('wind direction bias (ERA5 - in-situ) [°]')
    ax.set_ylim(-180, 180)
    ax.grid()
    ax.legend()

    ax.set_title('Comparison of the wind direction bias with the wind speed')
    fig.tight_layout()

def LW_up_check(ERA5_hourly_data, ws_hourly_data) :

    eps_sigma = 0.98 * 5.67 * 10 **(-8)
    Kelvin = 273.15
    
    WS_LW_up_TEL = ws_hourly_data['TEL-LW_up']
    ERA5_LW_up_TEL = ERA5_hourly_data['TEL-LW_up']

    WS_gound_temp_TEL = ws_hourly_data['TEL-ground_temperature']
    WS_LW_up_TEL_estimated = eps_sigma * (WS_gound_temp_TEL + Kelvin)**4

    fig = plt.figure(figsize = (11, 7))
    ax = fig.subplots()

    ax.plot(WS_LW_up_TEL.index, WS_LW_up_TEL, color = 'r', label = 'Tellbreen in-situ LW up')
    ax.plot(WS_LW_up_TEL_estimated.index, WS_LW_up_TEL_estimated, color = 'r', linestyle = '--', label = 'Tellbreen reconstructed LW up')
    ax.plot(ERA5_LW_up_TEL.index, ERA5_LW_up_TEL, color = 'r', alpha = 0.3, label = 'Tellbreen ERA5 LW up')

    WS_LW_up_BLE = ws_hourly_data['BLE-LW_up']
    ERA5_LW_up_BLE = ERA5_hourly_data['BLE-LW_up']

    WS_gound_temp_BLE = ws_hourly_data['BLE-ground_temperature']
    WS_LW_up_BLE_estimated = eps_sigma * (WS_gound_temp_BLE + Kelvin)**4

    ax.plot(WS_LW_up_BLE.index, WS_LW_up_BLE, color = 'b', label = 'Blekumbreen in-situ LW up')
    ax.plot(WS_LW_up_BLE_estimated.index, WS_LW_up_BLE_estimated, color = 'b', linestyle = '--', label = 'Blekumbreen reconstructed LW up')
    ax.plot(ERA5_LW_up_BLE.index, ERA5_LW_up_BLE, color = 'b', alpha = 0.3, label = 'Blekumbreen ERA5 LW up')

    ax.tick_params(axis = 'x', rotation = 30)
    ax.grid()
    ax.legend()

def temperature(ERA5_hourly_data, ws_hourly_data) :
    fig = plt.figure(figsize = (11, 7))
    ax = fig.subplots(1, 1)
    ax.plot(ERA5_hourly_data.index, ERA5_hourly_data['TEL-temperature@200'], label = 'Tellbreen ERA5 temperature', color = 'r', alpha = 0.25)
    ax.plot(ws_hourly_data.index, ws_hourly_data['TEL-temperature@200'], label = 'Tellbreen in-situ temperature', color = 'r')
    ax.plot(ERA5_hourly_data.index, ERA5_hourly_data['BLE-temperature@200'], label = 'Blekumbreen ERA5 temperature', color = 'b', alpha = 0.25)
    ax.plot(ws_hourly_data.index, ws_hourly_data['BLE-temperature@200'], label = 'Blekumbreen in-situ temperature', color = 'b')
    ax.xaxis.set_tick_params(rotation = 45)
    ax.legend()

    ax.set_title('ERA5 and in-situ temperatures on Tellbreen and Blekumbreen')
    ax.set_xlabel('time')
    ax.set_ylabel('temperature (°C)')
    ax.grid()
    fig.tight_layout()