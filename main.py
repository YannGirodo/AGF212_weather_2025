import ws_data
import tt_data
import ERA5
import tools
import plots
import matplotlib.pyplot as plt

# raw_ws_data, ws_columns = ws_data.import_data()
# ws_hourly_data = ws_data.hourly_averaged_data(raw_ws_data)

# raw_ws_data.to_csv('ws_data.csv')
# ws_hourly_data.to_csv('ws_hourly.csv')

ws_hourly_data, ws_columns = tools.load_csv('ws_hourly.csv')

# raw_tt_data, tt_columns = tt_data.import_data()
# tt_hourly_data = tt_data.hourly_averaged_data(raw_tt_data)

# raw_tt_data.to_csv('tt_data.csv')
# tt_hourly_data.to_csv('tt_hourly.csv')

tt_hourly_data, tt_columns = tools.load_csv('tt_hourly.csv')

ERA5_hourly_data, ERA5_columns = ERA5.import_data()

# print(ws_columns)
# print(tt_columns)
# print(ERA5_columns)

# plots.show_tt(tt_hourly_data)
# plots.show_ws(ws_hourly_data)
# plots.compare_ERA5_WS(ERA5_hourly_data, ws_hourly_data)

plots.scatter_ERA5_WS(ERA5_hourly_data, ws_hourly_data, 'wind')

# plots.temperature(ERA5_hourly_data, ws_hourly_data)

# plots.LW_up_check(ERA5_hourly_data, ws_hourly_data)

# plots.compare_winds(ERA5_hourly_data, ws_hourly_data)

plt.show()
# plt.savefig('radiation_correlation.pdf', format = 'pdf')