    import pandas as pd
    import pytz

  ## Function to load dataset and standardize column name
    def extract_device_data(device_name, time_ranges, output_file):
        # Load the MZ3 CSV file
        mz3_df = pd.read_csv('mz3.csv', parse_dates=['Time'])
    
        # Rename 'Time' column to 'Timestamp'
        mz3_df.rename(columns={'Time': 'Timestamp'}, inplace=True)
    
  ## Assume timestamps are already in local time and localize them to US/Central
        mz3_df['Timestamp'] = pd.to_datetime(mz3_df['Timestamp'])
        mz3_df['Timestamp'] = mz3_df['Timestamp'].dt.tz_localize('US/Central')  # NOT converting, just assigning
    
        # Set Timestamp as index
        mz3_df.set_index('Timestamp', inplace=True)
    
        # Device mapping
        devices = {
            'mz3': (mz3_df, 'hr')
        }
    
        if device_name not in devices:
            print("Invalid device name. Choose from: mz3")
            return
    
        df, col_name = devices[device_name]
    
  ## Resample in 3-minute bins and compute stats
        df_resampled = df.resample('3min').agg({col_name: ['mean', 'max', 'min', 'std', 'count']})
        df_resampled.columns = ['mean', 'max', 'min', 'std', 'count']
    
  ## Localize time ranges to US/Central
        time_ranges = [
            (pd.Timestamp(start).tz_localize('US/Central'),
             pd.Timestamp(end).tz_localize('US/Central'),
             label)
            for start, end, label in time_ranges
        ]
    
  ## Filter and collect data by time range
        results = []
        for start_time, end_time, label in time_ranges:
            filtered_data = df_resampled.loc[start_time:end_time].reset_index()
            if not filtered_data.empty:
                filtered_data['Date'] = filtered_data['Timestamp'].dt.strftime('%m/%d/%Y')
                filtered_data['Time'] = filtered_data['Timestamp'].dt.strftime('%H:%M:%S')
                filtered_data['activity'] = label
                results.append(filtered_data)
    
  ## Save if data exists
        if results:
            final_data = pd.concat(results, ignore_index=True)
            final_data = final_data[['Date', 'Time', 'activity', 'mean', 'max', 'min', 'std', 'count']]
            final_data.to_csv(output_file, index=False)
            print(f"Extracted data saved to {output_file}")
        else:
            print("No data found in the specified time ranges.")
    
## Example usage
    device = 'mz3'
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
    output_file = 'output_mz3.csv'
    
    extract_device_data(device, time_ranges, output_file)
