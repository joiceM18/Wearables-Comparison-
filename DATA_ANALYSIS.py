import pandas as pd
from scipy.stats import ks_2samp

# File paths for the three devices
oura_file = "processed_Oura (3).csv"
empatica_file = "processed_empatica (2).csv"
mz3_file = "output_mz3(3).csv"

# Load the CSV files
df_oura = pd.read_csv(oura_file)
df_empatica = pd.read_csv(empatica_file)
df_mz3 = pd.read_csv(mz3_file)

# (Assumption: Each CSV contains at least these columns: 
#   'activity'  - text label of the activity,
#   'mean'      - the measurement you want to summarize (e.g. heart rate),
#   plus other stats.)

def summarize_by_activity(df, device_name):
    print(f"Summary statistics for {device_name}:")
    # Group by activity and compute summary stats for the 'mean' column
    summary = df.groupby("activity")["mean"].agg(["count", "mean", "std", "min", "max"])
    print(summary, "\n")
    return summary

summary_oura = summarize_by_activity(df_oura, "Oura")
summary_empatica = summarize_by_activity(df_empatica, "Empatica")
summary_mz3 = summarize_by_activity(df_mz3, "MZ3")

# Get common activities across all three files
activities_oura = set(df_oura["activity"].unique())
activities_empatica = set(df_empatica["activity"].unique())
activities_mz3 = set(df_mz3["activity"].unique())

common_activities = activities_oura & activities_empatica & activities_mz3
print("Common activities across devices:", common_activities, "\n")

def perform_ks_tests(activity):
    # Filter the data for this activity and drop any missing values in 'mean'
    data_oura = df_oura[df_oura["activity"] == activity]["mean"].dropna()
    data_empatica = df_empatica[df_empatica["activity"] == activity]["mean"].dropna()
    data_mz3 = df_mz3[df_mz3["activity"] == activity]["mean"].dropna()
    
    print(f"KS tests for activity: {activity}")
    # Compare Oura vs Empatica
    ks_stat, p_value = ks_2samp(data_oura, data_empatica)
    print(f"  Oura vs Empatica: KS statistic = {ks_stat:.4f}, p-value = {p_value:.4f}")
    
    # Compare Oura vs MZ3
    ks_stat, p_value = ks_2samp(data_oura, data_mz3)
    print(f"  Oura vs MZ3:       KS statistic = {ks_stat:.4f}, p-value = {p_value:.4f}")
    
    # Compare Empatica vs MZ3
    ks_stat, p_value = ks_2samp(data_empatica, data_mz3)
    print(f"  Empatica vs MZ3:    KS statistic = {ks_stat:.4f}, p-value = {p_value:.4f}")
    print("\n")

# Run KS tests for each common activity
for activity in common_activities:
    perform_ks_tests(activity)
  
