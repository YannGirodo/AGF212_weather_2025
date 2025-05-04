import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

###READ IN DATA
##ERA5
era5_bb = pd.read_csv("ERA5-BB_FINAL.csv")
era5_tb = pd.read_csv("ERA5-TB_FINAL.csv")
date_strings = era5_bb["date"]
era5_time = [datetime.strptime(date_str, "%Y%m%d %H%M") for date_str in date_strings]

##INSITU
insitu = pd.read_csv("hourly_tora(in).csv")
date_insitu = insitu["DATE"]
insitu_time = np.array([datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S") for date_str in date_insitu])
exclude_begin = pd.Timestamp("2025-03-07 06:00:00")
exclude_stop = pd.Timestamp("2025-03-09 10:00:00")

##TINYTAG
bb_tinytag = pd.read_csv("tt_hourly_tora(in).csv")
bb_ground_tt = bb_tinytag["TT6-Black Probe Temperature"]
tb_ground_tt = bb_tinytag["TT14-Black Probe Temperature"]

###VARIABLES
##ERA5 Tellbreen
#SW
era5_tb_sw_net = era5_tb["surface_net_solar_radiation_hourly"]
era5_tb_sw_down = era5_tb["surface_solar_radiation_downwards_hourly"]
era5_tb_sw_up = era5_tb_sw_net - era5_tb_sw_down
#LW
era5_tb_lw_net = era5_tb["surface_net_thermal_radiation_hourly"]
era5_tb_lw_down = era5_tb["surface_thermal_radiation_downwards_hourly"]
era5_tb_lw_up = era5_tb_lw_net - era5_tb_lw_down
#TURBULENT
era5_tb_latent = era5_tb["surface_latent_heat_flux_hourly"]
era5_tb_sensible = era5_tb["surface_sensible_heat_flux_hourly"]
#GROUND
kappa = 0.42 # W/mK
era5_tb_surf = era5_tb["skin_temperature"]
era5_tb_ground_T = era5_tb["temperature_of_snow_layer"]
era5_tb_h_snow = era5_tb["snow_depth"] #m
era5_tb_ground_flux = kappa * (era5_tb_surf- era5_tb_ground_T)/era5_tb_h_snow

##Blekumbreen
#SW
era5_bb_sw_net = era5_bb["surface_net_solar_radiation_hourly"]
era5_bb_sw_down = era5_bb["surface_solar_radiation_downwards_hourly"]
era5_bb_sw_up = era5_bb_sw_net - era5_bb_sw_down
#LW
era5_bb_lw_net = era5_bb["surface_net_thermal_radiation_hourly"]
era5_bb_lw_down = era5_bb["surface_thermal_radiation_downwards_hourly"]
era5_bb_lw_up = era5_bb_lw_net - era5_bb_lw_down
#TURBULENT
era5_bb_latent = era5_bb["surface_latent_heat_flux_hourly"]
era5_bb_sensible = era5_bb["surface_sensible_heat_flux_hourly"]
#GROUND
era5_bb_surf = era5_bb["skin_temperature"]
era5_bb_ground_T = era5_bb["temperature_of_snow_layer"]
era5_bb_h_snow = era5_bb["snow_depth"] #m
era5_bb_ground_flux = kappa * (era5_bb_surf- era5_bb_ground_T)/era5_bb_h_snow


##Insitu Tellbreen
#SW
tb_sw_up = insitu["TEL-SW_up"]
tb_sw_down = insitu["TEL-SW_down"]

#LW
tb_lw_down = insitu["TEL-LW_down"]
tb_lw_up = insitu["TEL-LW_up"]

##Insitu Blekumbreen
#SW
bb_sw_up = insitu["BLE-SW_up"]
bb_sw_down = insitu["BLE-SW_down"]

#LW
bb_lw_down = insitu["BLE-LW_down"]
bb_lw_up = insitu["BLE-LW_up"]

##CALCULATING SENSIBLE LATENT GROUND
sigma = 5.67 * 10 **(-8)
K = 273.15 #Kelvin
uw_tb = insitu["TEL-wind_speed@200"]
T_200_tb = insitu["TEL-temperature@200"] 
uw_bb = insitu["BLE-wind_speed@200"]
T_200_bb = insitu["BLE-temperature@200"] 
T_surf_tb =  (tb_lw_up/sigma)**(1/4) #from lw radiation
T_surf_bb =  (bb_lw_up/sigma)**(1/4) #from lw radiation

#LATENT
Ab_lat = 0.0015 #dimensionless transfer coeff of latent heat
RH_tb = insitu["TEL-relative_humidity@200"]
RH_bb = insitu["BLE-relative_humidity@200"]

def e_sat(temp):
    #Calculating saturated vapor pressure over ice
    e0 = 0.6113 #kPa
    Ld_Rv = 6139 #[K] over ice
    T0 = 273.15 
    T = temp
    #need to convert to Pa
    return e0 * np.exp(Ld_Rv * ((1/T0) - (1/T))) * 1000
"""
def e_sat(temp):
    e0 = 611.153 #Pa
    T = temp - 273.15
    #need to convert to Pa
    return e0 * np.exp((22.443 * T)/ (272.186 + T))
"""
#tell
e_surf = e_sat(T_surf_tb)
e_air = (RH_tb/100) * e_sat(T_200_tb + 273.15)
tb_latent = 22.2 * Ab_lat * uw_tb * (e_air - e_surf)
#blekum
e_surf_b = e_sat(T_surf_bb)
e_air_b = (RH_bb/100) * e_sat(T_200_bb + 273.15)
bb_latent = 22.2 * Ab_lat * uw_bb * (e_air_b - e_surf_b)

#SENSIBLE
rho_air = 1.293 #[kg/m^3]
cp = 1004  #[J/kg K]
Ab_sens = 0.0019 #dimensionless transfer coeff of sensible heat 
tb_sensible = rho_air * cp * Ab_sens * uw_tb *(T_200_tb + K - T_surf_tb )
bb_sensible = rho_air * cp * Ab_sens * uw_bb *(T_200_bb + K - T_surf_bb)


#GROUND - Blekumbreen

bb_ground_mean = np.mean(bb_ground_tt) + 273.15 #K
h_bb_snow = 155/100 #m
#ground_bb = kappa * (T_surf_bb - bb_ground_K[75:215])/h_bb_snow
ground_bb = kappa * (T_surf_bb - bb_ground_mean)/h_bb_snow

tb_ground_mean = np.mean(tb_ground_tt) + 273.15 #K
h_tb_snow = 130/100 #m
#ground_tb = kappa * (T_surf_tb - tb_ground_K[4:215])/h_tb_snow
ground_tb = kappa * (T_surf_tb - tb_ground_mean)/h_tb_snow

###SURFACE ENERGY BALANCE TELLBREEN
J_W = 60*60 #needs a conversion

net_tb_era5 = (era5_tb_sw_net + era5_tb_lw_net + era5_tb_latent + era5_tb_sensible + era5_tb_ground_flux) / J_W
net_tb_insitu =( - tb_sw_up + tb_sw_down - tb_lw_up + tb_lw_down + tb_sensible + tb_latent + ground_tb).where(np.logical_or(insitu_time < exclude_begin, insitu_time > exclude_stop)) 
net_bb_era5 = (era5_bb_sw_net + era5_bb_lw_net + era5_bb_latent + era5_bb_sensible + era5_bb_ground_flux) / J_W
net_bb_insitu = (- bb_sw_up + bb_sw_down - bb_lw_up + bb_lw_down + bb_sensible + bb_latent + ground_bb ).where(np.logical_or(insitu_time < exclude_begin, insitu_time > exclude_stop)) 

#radiative net
rad_net_tb_era5 = (era5_tb_sw_net + era5_tb_lw_net) / J_W
rad_net_tb_insitu = -tb_sw_up + tb_sw_down - tb_lw_up + tb_lw_down 
rad_net_bb_era5 = (era5_bb_sw_net + era5_bb_lw_net) / J_W
rad_net_bb_insitu = -bb_sw_up + bb_sw_down - bb_lw_up + bb_lw_down

sw_net_tb_insitu = (- tb_sw_up + tb_sw_down).where(np.logical_or(insitu_time < exclude_begin, insitu_time > exclude_stop)) 
sw_net_bb_insitu = (- bb_sw_up + bb_sw_down).where(np.logical_or(insitu_time < exclude_begin, insitu_time > exclude_stop))  

lw_net_tb_insitu = (- tb_lw_up + tb_lw_down).where(np.logical_or(insitu_time < exclude_begin, insitu_time > exclude_stop))  
lw_net_bb_insitu = (- bb_lw_up + bb_lw_down).where(np.logical_or(insitu_time < exclude_begin, insitu_time > exclude_stop))  

plt.plot(era5_time, era5_tb_sw_net / J_W, color=(1, 0.6, 0.6), label ="ERA5 TB")
plt.plot(era5_time, era5_bb_sw_net /J_W , color=(0.6, 0.8, 1), label ="ERA5 BB")
plt.plot(insitu_time, sw_net_tb_insitu,color = "r", label = "Insitu TB")
plt.plot(insitu_time, sw_net_bb_insitu ,color = "b", label = "Insitu BB")
plt.legend()
plt.xlabel("DATE UTC")
plt.ylabel("SW NET  W/m^2")
plt.grid()
plt.show()

plt.plot(era5_time, era5_tb_lw_net /J_W , color=(1, 0.6, 0.6), label ="ERA5 TB")
plt.plot(era5_time, era5_bb_lw_net /J_W , color=(0.6, 0.8, 1), label ="ERA5 BB")
plt.plot(insitu_time, lw_net_tb_insitu,color = "r", label = "Insitu TB")
plt.plot(insitu_time, lw_net_bb_insitu ,color = "b", label = "Insitu BB")
plt.legend()
plt.xlabel("DATE UTC")
plt.ylabel("LW NET  W/m^2")
plt.grid()
plt.show()
"""
fig, axs = plt.subplots(3, 1, figsize=(6, 12), sharex = True)

axs[0].plot(era5_time, -era5_bb_sw_up/J_W,"--", color=(0.6, 0.8, 1), label ="ERA5 up")
axs[0].plot(era5_time, era5_bb_sw_down/J_W,color=(0.6, 0.8, 1), label ="ERA5 down")
axs[0].plot(insitu_time, bb_sw_up, "--", color = "b", label = "Insitu up")
axs[0].plot(insitu_time, bb_sw_down, color = "b", label = "Insitu down")
axs[0].legend()
axs[0].grid()
axs[0].set_ylabel("BB SW [W/m^2] ")

axs[1].plot(era5_time, -era5_bb_lw_up/J_W,"--", color=(0.6, 0.8, 1), label ="ERA5 up")
axs[1].plot(era5_time, era5_bb_lw_down/J_W,color=(0.6, 0.8, 1), label ="ERA5 down")
axs[1].plot(insitu_time, bb_lw_up, "--", color = "b", label = "Insitu up")
axs[1].plot(insitu_time, bb_lw_down, color = "b", label = "Insitu down")
axs[1].legend()
axs[1].grid()
#plt.xlabel("DATE UTC")
#plt.title(" Blekumbreen LW")
axs[1].set_ylabel("BB LW [W/m^2] ")

axs[2].plot(era5_time, rad_net_tb_era5 , color=(1, 0.6, 0.6), label ="ERA5 TB")
axs[2].plot(era5_time, rad_net_bb_era5 , color=(0.6, 0.8, 1), label ="ERA5 BB")
axs[2].plot(insitu_time, rad_net_tb_insitu ,color = "r", label = "Insitu TB")
axs[2].plot(insitu_time, rad_net_bb_insitu ,color = "b", label = "Insitu BB")
axs[2].legend()
axs[2].grid()
axs[2].set_ylabel(" Net Radiative [W/m^2] ")

plt.xlabel("Date UTC")
plt.tight_layout()
plt.show()
"""
fig1, ax = plt.subplots(3, 1, figsize=(6, 12), sharex = True)

ax[0].plot(era5_time, era5_bb_ground_flux, color=(0.6, 0.8, 1), label ="ERA5 BB")
ax[0].plot(era5_time, era5_tb_ground_flux,  color=(1, 0.6, 0.6), label ="ERA5 TB")
ax[0].plot(insitu_time, ground_bb ,color = "b", label = "Insitu BB")
ax[0].plot(insitu_time, ground_tb ,color = "r", label = "Insitu TB")
ax[0].legend()
ax[0].grid()
ax[0].set_ylabel(" Ground [W/m^2] ")

ax[1].plot(era5_time, era5_bb_latent/J_W, color=(0.6, 0.8, 1), label ="ERA5 BB")
ax[1].plot(era5_time, era5_tb_latent/J_W, color=(1, 0.6, 0.6),label = "ERA5 TB")
ax[1].plot(insitu_time, bb_latent ,color = "b", label = "Insitu BB")
ax[1].plot(insitu_time, tb_latent ,color = "r", label = "Insitu TB")
ax[1].legend()
ax[1].grid()
ax[1].set_ylabel(" Latent [W/m^2] ")

ax[2].plot(era5_time, era5_bb_sensible/J_W, color=(0.6, 0.8, 1), label ="ERA5 BB")
ax[2].plot(era5_time, era5_tb_sensible/J_W, color=(1, 0.6, 0.6),label = "ERA5 TB")
ax[2].plot(insitu_time, bb_sensible ,color = "b", label = "Insitu BB")
ax[2].plot(insitu_time, tb_sensible ,color = "r", label = "Insitu TB")
ax[2].legend()
ax[2].grid()
ax[2].set_ylabel(" Sensible [W/m^2] ")

plt.xlabel("Date UTC")
plt.tight_layout()
plt.show()

##Look at albedo on its own
##STATISTICS YEAH 
#is there correlation between the radiative fluxes? the turbulent?  so era5 againt observations
#need to normalize 
"""
fig2, ax2 = plt.subplots(2, 1, figsize=(6, 12), sharex = True)

ax2[0].plot(era5_time, net_tb_era5, color=(1, 0.6, 0.6),label = "ERA5 TB")
ax2[0].plot(insitu_time, net_tb_insitu,color = "r", label = "INSITU TB")
ax2[0].legend()
ax2[0].grid()
ax2[0].set_ylabel("W/m^2")
"""
fig = plt.figure(figsize = (11, 7))
axl = fig.subplots()
axl.plot(era5_time, net_tb_era5, color=(1, 0.6, 0.6),label = "ERA5 TB")
axl.plot(era5_time, net_bb_era5, color=(0.6, 0.8, 1), label = "ERA5 BB")
axl.plot(insitu_time, net_tb_insitu,color = "r", label = "INSITU TB")
axl.plot(insitu_time, net_bb_insitu, color="b",label = "INSITU BB")

#axr.plot(insitu_time, T_surf_tb, label = "TB T")
#axr.plot(insitu_time, T_surf_bb, label = "BB T")
axl.legend()
axl.grid()

axl.set_xlabel("DATE UTC")
axl.set_ylabel("Total SEB [W/m^2]")
plt.show()

"""
##ALBEDO 
era5_tb_albedo = era5_tb["snow_albedo"]
era5_bb_albedo = era5_bb["snow_albedo"] 
insitu_tb_albedo = tb_sw_up/tb_sw_down
insitu_bb_albedo = bb_sw_up/bb_sw_down

plt.plot(era5_time, era5_tb_albedo , color=(1, 0.6, 0.6), label ="ERA5 TB")
plt.plot(era5_time, era5_bb_albedo , color=(0.6, 0.8, 1), label ="ERA5 BB")
#plt.plot(insitu_time, insitu_tb_albedo ,color = "r", label = "Insitu TB")
#plt.plot(insitu_time, insitu_bb_albedo ,color = "b", label = "Insitu BB")
plt.xlabel("DATE UTC")
plt.grid()
plt.legend()
plt.show()
"""