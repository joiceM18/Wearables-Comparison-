## Import libraries
import pandas as pd
import pytz

## Function to load dataset and standardize column name
def extract_device_data(device_name, time_ranges, output_file):
    # Load the Empatica CSV file
    empatica_df = pd.read_csv('empatica.csv', parse_dates=['minute'])

    # Standardize column names: rename 'minute' to 'Timestamp'
    empatica_df.rename(columns={'minute': 'Timestamp'}, inplace=True)

    # Convert Timestamp to datetime and localize to US/Central
    empatica_df['Timestamp'] = pd.to_datetime(empatica_df['Timestamp'])
    empatica_df['Timestamp'] = empatica_df['Timestamp'].dt.tz_localize('UTC').dt.tz_convert('US/Central')

    # Set Timestamp as index
    empatica_df.set_index('Timestamp', inplace=True)

    # Dictionary mapping device names to their corresponding dataframe and data column.
    devices = {
        'empatica': (empatica_df, 'entry_count')
    }

    if device_name not in devices:
        print("Invalid device name. Choose from: empatica")
        return

    df, col_name = devices[device_name]

    # Resample and compute statistics in 3-minute bins
    df_resampled = df.resample('3min').agg({col_name: ['mean', 'max', 'min', 'std', 'count']})
    df_resampled.columns = ['mean', 'max', 'min', 'std', 'count']

    # Convert time_ranges to timezone-aware timestamps in US/Central
    time_ranges = [(pd.Timestamp(start).tz_localize('US/Central'),
                    pd.Timestamp(end).tz_localize('US/Central'), label) for start, end, label in time_ranges]

    # Collect filtered data for multiple time ranges
    results = []
    for start_time, end_time, label in time_ranges:
        filtered_data = df_resampled.loc[start_time:end_time].reset_index()
        if not filtered_data.empty:
            filtered_data['Date'] = filtered_data['Timestamp'].dt.strftime('%m/%d/%Y')
            filtered_data['Time'] = filtered_data['Timestamp'].dt.strftime('%H:%M:%S')
            filtered_data['activity'] = label  # Assign the activity label
            results.append(filtered_data)

    # Concatenate all results and save to CSV if any data was found
    if results:
        final_data = pd.concat(results, ignore_index=True)
        final_data = final_data[['Date', 'Time', 'mean', 'max', 'min', 'std', 'activity', 'count']]
        final_data.to_csv(output_file, index=False)
        print(f"Extracted data saved to {output_file}")
    else:
        print("No data found in the specified time ranges.")

# Example usage
device = 'empatica'
time_ranges = [
    ('2024-01-22 04:00:00', '2024-01-22 04:30:00', 'sleep'),
    ('2024-01-22 05:36:00', '2024-01-22 06:06:00', 'rest'),
    ('2024-01-22 06:14:00', '2024-01-22 06:44:00', 'exercise'),
    ('2024-01-22 07:36:00', '2024-01-22 08:04:00', 'housework'),
    ('2024-01-22 08:07:00', '2024-01-22 08:37:00', 'computer work'),
    ('2024-01-23 06:07:00', '2024-01-23 06:37:00', 'rest'),
    ('2024-01-23 11:30:00', '2024-01-23 12:00:00', 'housework'),
    ('2024-01-23 12:15:00', '2024-01-23 12:45:00', 'computer work'),
    ('2024-01-23 17:30:00', '2024-01-23 18:00:00', 'shopping'),
    ('2024-01-23 10:10:00', '2024-01-23 10:40:00', 'exercise')
]
output_file = 'output_empatica.csv'

extract_device_data(device, time_ranges, output_file)
