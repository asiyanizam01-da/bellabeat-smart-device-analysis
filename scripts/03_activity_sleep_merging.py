#03_activity_sleep_merging.py
#Author: Asiya Nizam
#Purpose: Merging Cleaned Fitbit Daily Activity and Sleep Data for Bellabeat Case Study

import pandas as pd

#-----------------------
#Load clean datasets
#-----------------------
activity = pd.read_csv("Data/Processed/dailyActivity_cleaned.csv")
sleep = pd.read_csv("Data/Processed/sleepData_cleaned.csv")

#----------------------------------------
#Convert date columns to datetime.date
#----------------------------------------
activity['ActivityDate'] = pd.to_datetime(activity['ActivityDate'], dayfirst = True).dt.date
sleep['SleepDate'] = pd.to_datetime(sleep['SleepDate'], dayfirst = True).dt.date

#Merge datasets on Id and Date
merged = pd.merge(activity, sleep, how = "inner",
                 left_on = ['Id','ActivityDate'],
                 right_on = ['Id', 'SleepDate'])

# ---------------------------
# Drop duplicate date column from sleep
# ---------------------------
merged = merged.drop(columns=['SleepDate'])

# ---------------------------
# Reset index
# ---------------------------
merged = merged.reset_index(drop=True)

# ---------------------------
# Quick inspection
# ---------------------------
print("\n---Merged Dataset Info---")
merged.info()

print("\n---First 10 rows---")
print(merged.head(10))

print("\n---Unique Id Count---")
print(merged['Id'].nunique())

print("\nRows after merging:", len(merged))

# ---------------------------
# Save merged CSV
# ---------------------------
merged_path = "Data/Processed/activity_sleep_merged.csv"
merged.to_csv(merged_path, index=False)
print(f"\nMerged dataset saved to: {merged_path}")