## Import important libraries for processing 
    import pandas as pd
    import pytz
    from datetime import datetime

## Define timezone objects
    utc_zone = pytz.utc
    central_zone = pytz.timezone("US/Central")

## Load the CSV file
    file_path = "/content/sps.csv"  # Update this to the path of your CSV file
    data = pd.read_csv(\\files.times.uh.edu\Labs\Grigorenko\Wearables Data Analysis\New folder\New folder\Empatica systolic peaks)

## Convert systolic_peak_timestamp to numeric and drop invalid entries
    print(data['systolic_peak_timestamp'].dtype)
    data['systolic_peak_timestamp'] = pd.to_numeric(data['systolic_peak_timestamp'], errors='coerce')
    data = data.dropna(subset=['systolic_peak_timestamp'])

## Convert Unix timestamps from nanoseconds to human-readable datetime in US/Central time
    data['readable_datetime'] = data['systolic_peak_timestamp'].apply(
    lambda x: datetime.fromtimestamp(x / 1e9, tz=utc_zone)
                     .astimezone(central_zone)
                     .strftime('%Y-%m-%d %H:%M:%S.%f')
    )

## Save the processed file with readable datetimes -> outputs file "systolic_peak_processed"
    output_path = "systolic_peak_processed.csv"  # Update this to your desired output path
    data.to_csv(output_path, index=False)
    print(data.head())

## Create a new column for minute-level grouping (US/Central)
    data['minute'] = data['systolic_peak_timestamp'].apply(
    lambda x: datetime.fromtimestamp(x / 1e9, tz=utc_zone)
                     .astimezone(central_zone)
                     .strftime('%Y-%m-%d %H:%M')
  )

## Group by 'minute' and count the entries (this gives the number of systolic peaks per minute)
    minute_counts = data.groupby('minute').size().reset_index(name='entry_count')

## Merge the counts back into the original data for reference
    data = data.merge(minute_counts, on='minute', how='left')

## Save the result to a new file
    output_path = "systolic_peak_per_minute.csv"  # Update this to your desired output path
    data.to_csv(output_path, index=False)
    print(minute_counts.head())

## Save a simplified DataFrame with only 'minute' and 'entry_count' columns -> outputs file "systolic_peak_minute_counts"
    minute_counts.to_csv("systolic_peak_minute_counts.csv", index=False)
