# this script is sued to normalize source_data.xls obtained from www.chmi.cz to invalida_dates.to_csv
# as chmi is publishing new data once a year only, the data normalization is done manually ad-hoc

import pandas as pd
import numpy as np

# define mapping of the source xls sheets to dataframe columns
sheet_column = {
    'teplota průměrná' : 'temperature_AVG',
    'teplota maximální' : 'temperature_MAX',
    'teplota minimální' : 'temperature_MIN',
    'rychlost větru ' : 'wind_speed',
    'tlak vzduchu' : 'atmospheric_pressure',
    'vlhkost vzduchu' : 'humidity',
    'úhrn srážek' : 'rain_fall',
    'celková výška sněhu' : 'snow_height',
    'sluneční svit' : 'sunshine_duration'
}

# read source xls data into a dataframe
column_values={}
dates_added = False
# loop through the sheets
for sheet, column in sheet_column.items():
    temp_df = pd.read_excel('source_data.xls', sheet_name=sheet, skiprows=[0,1,2])
    dates = []
    values = []
    invalid_dates = []
    # loop through the rows
    for row in temp_df.index:
        for day in range(2,33):
            try:
                dates.append(pd.Timestamp(temp_df.iloc[row,0], temp_df.iloc[row,1], day-1))
                values.append(temp_df.iloc[row,day])
            except ValueError:
                invalid_dates.append(str(temp_df.iloc[row,0]) + '-' + str(temp_df.iloc[row,1]) + '-' + str(day-1))
    # add dates column for the first iteration
    if dates_added == False:
        column_values['date']=dates
        dates_added = True
    # appand normalized data form the current sheet
    column_values[column]=values

# convert to dataframes
df = pd.DataFrame(column_values)
invalid_dates_df = pd.DataFrame(list(set(invalid_dates)), columns=['date'])

# export normalized data to a file
df.to_csv('normalized_data.csv', index=False)
# export skipped invalid dates to a file
invalid_dates_df.to_csv('invalid_dates.csv', index=False)
