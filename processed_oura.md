## read


import pandas as pd 
import pytz
def extract_device_data(device_name, time_ranges, output_file):
    # Load datasets
    oura_df = pd.read_csv('oura.csv', parse_dates=['timestamp'])
    # mz3_df = pd.read_csv('mz3.csv', parse_dates=['Time'])
    # empatica_df = pd.read_csv('empatica.csv', parse_dates=['minute'])

    # Standardize column names
    oura_df.rename(columns={'timestamp': 'Timestamp'}, inplace=True)
    # mz3_df.rename(columns={'Time': 'Timestamp'}, inplace=True)
    # empatica_df.rename(columns={'minute': 'Timestamp'}, inplace=True)

    # Convert timestamps to UTC then to US/Central
    for df in [oura_df]:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], utc=True)
        df['Timestamp'] = df['Timestamp'].dt.tz_convert('US/Central')

    # Set Timestamp as index
    oura_df.set_index('Timestamp', inplace=True)
    # mz3_df.set_index('Timestamp', inplace=True)
    # empatica_df.set_index('Timestamp', inplace=True)

    # Dictionary mapping device names to their corresponding data and column name
    devices = {
        'oura': (oura_df, 'bpm')
        # 'mz3': (mz3_df, 'hr'),
        # 'empatica': (empatica_df, 'entry_count')
    }

    if device_name not in devices:
        print("Invalid device name. Choose from: oura, mz3, empatica")
        return

    df, col_name = devices[device_name]

    # Resample and compute statistics (keeping the timezone info intact)
    df_resampled = df.resample('3min').agg({col_name: ['mean', 'max', 'min', 'std', 'count']})
    df_resampled.columns = ['mean', 'max', 'min', 'std', 'count']

    # Convert time_ranges to timezone-aware timestamps in US/Central
    time_ranges = [(pd.Timestamp(start).tz_localize('US/Central'),
                    pd.Timestamp(end).tz_localize('US/Central')) for start, end in time_ranges]

    # Collect filtered data for multiple time ranges
    results = []
    for start_time, end_time in time_ranges:
        filtered_data = df_resampled.loc[start_time:end_time].reset_index()
        filtered_data['Date'] = filtered_data['Timestamp'].dt.strftime('%m/%d/%Y')
        filtered_data['Time'] = filtered_data['Timestamp'].dt.strftime('%H:%M:%S')
        results.append(filtered_data)

    # Concatenate all results
    if results:
        final_data = pd.concat(results, ignore_index=True)
        final_data = final_data[['Date', 'Time', 'mean', 'max', 'min', 'std', 'count']]
        final_data.to_csv(output_file, index=False)
        print(f"Extracted data saved to {output_file}")
    else:
        print("No data found in the specified time ranges.")

# Example usage
device = 'oura'  # Change to 'mz3' or 'empatica' as needed
time_ranges = [
    ('2024-01-22 04:00:00', '2024-01-22 04:30:00'),
    ('2024-01-22 05:36:00', '2024-01-22 06:06:00'),
    ('2024-01-22 06:14:00', '2024-01-22 06:44:00'),
    ('2024-01-22 07:36:00', '2024-01-22 07:45:00'),
    ('2024-01-22 08:07:00', '2024-01-22 08:37:00'),
    ('2024-01-23 06:07:00', '2024-01-23 06:37:00'),
    ('2024-01-23 11:30:00', '2024-01-23 12:00:00'),
    ('2024-01-23 12:15:00', '2024-01-23 12:45:00'),
    ('2024-01-23 17:30:00', '2024-01-23 18:00:00'),
    ('2024-01-23 10:10:00', '2024-01-23 10:40:00')
]
output_file = 'output.csv'

extract_device_data(device, time_ranges, output_file)
