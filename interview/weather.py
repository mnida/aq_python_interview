
from datetime import datetime
def process_csv(reader, writer):
    
    station_days = {} # key = station, value = dict {key = date, values= [min, max, (start, time), (end, time)]}

    header = next(reader) # Assume the header is the first line
    for row in reader:
        column_values = row.split(',')
        station = column_values[0]
        datetimestring = column_values[1]
        parsed_datetime = datetime.strptime(datetimestring, '%m/%d/%Y %H:%M:%S %p')
        date = parsed_datetime.date()
        time = parsed_datetime.time()

        temp = float(column_values[2])

        if station not in station_days:
            station_days[station] = {
                date: [temp, temp,(temp,time), (temp,time) ]
            }
        else:
            station_dates = station_days[station]
            if date not in station_dates:
                station_dates[date] =  [temp, temp,(temp,time), (temp,time) ]
            else: # if there are already temperature readings from this station and day

                min_temp, max_temp, (start_temp, start_time), (end_temp, end_time) = station_dates[date]
                max_temp = max(max_temp, temp)
                min_temp = min(min_temp, temp)
                if time < start_time:
                    start_temp = temp
                    start_time = time
                if time > end_time:
                    end_time = time
                    end_temp = temp
                station_dates[date] =  [min_temp, max_temp, (start_temp, start_time), (end_temp, end_time) ] # update the station's stats


    # Now write this to a csv file but we need to specify the new header
    header = 'Station Name,Date,Min Temp,Max Temp,First Temp,Last Temp'
    writer.write(header)
    for station in station_days:
        for date in station_days[station]:
            min_temp, max_temp, (start_temp, start_time), (end_temp, end_time) = station_days[station][date]
            writer.write(f"{station},{date.strftime('%m/%d/%Y')},{min_temp},{max_temp},{start_temp},{end_temp}\n")
    



### How would I have done with with pandas

# import pandas as pd

# df = pd.read_csv('csv', header=0)

# df['datetime'] = pd.to_datetime(df['datetime'], format='%m/%d/%Y %H:%M:%S %p')
# df['date'] = df['datetime'].dt.date
# df['time'] = df['datetime'].dt.time

# df.rename(columns={'temp': 'Air Temperatur'}, inplace=True)

# new_df = df.groupby(['station', 'date'])

# aggregated = new_df.agg(
#     min_temp = ('temp', 'min'),
#     max_temp = ('temp', 'max'),
#     first_temp = ('temp', 'first'),
#     last_temp = ('temp', 'last')
# )

# aggregated= aggregated.reset_index()
# aggregated.columns = ['Station Name', 'Date', 'Min Temp', 'Max Temp', 'First Temp', 'Last Temp']
# aggregated.to_csv('aggregated.csv', index=False)

