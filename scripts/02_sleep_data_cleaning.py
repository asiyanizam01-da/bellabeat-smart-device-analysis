#02_sleep_data_cleaning.py
#Author: Asiya Nizam
#Purpose: Clean and Prepare Fitbit Daily Sleep Data for Bellabeat Case Study

import pandas as pd

#---------------------------
#Load April-May data
#---------------------------
sleep = pd.read_csv("Data/Original/mturkfitbit_export_4.12.16-5.12.16/sleepDay_merged.csv")

#---------------------------
#Inspection
#---------------------------
print("\n-------Dataset Info--------")
sleep.info()

print("\n--------First 10 rows--------")
print(sleep.head(10))

print("\n------Unique Values Per Column------")
print(sleep.nunique())

print("\n------Unique Id Count------")
print(sleep["Id"].nunique())

print("\n------Null Values Per Column-------")
print(sleep.isnull().sum())

print(f"\nRows before cleaning: {len(sleep)}")

#----------------------------
#Clean SleepDay Column
#----------------------------
sleep = sleep.rename(columns = {"SleepDay": "SleepDate"})
sleep["SleepDate"] = pd.to_datetime(sleep["SleepDate"], errors = "coerce")

invalid_dates_count = sleep["SleepDate"].isnull().sum()

if invalid_dates_count > 0:
    print(f"Found {invalid_dates_count} invalid date rows. Dropping.")
    sleep = sleep.dropna(subset = ["SleepDate"])
else:
    print("No invalid dates found")

#Extract date only, remove time
sleep["SleepDate"] = sleep["SleepDate"].dt.normalize()

#--------------------------------------
#Remove Duplicates (Per user per day)
#--------------------------------------
duplicate_count = sleep.duplicated(subset = ["Id","SleepDate"]).sum()

if duplicate_count > 0:
    print(f"Found {duplicate_count} duplicate values. Dropping.")
    sleep = sleep.drop_duplicates(subset = ["Id","SleepDate"])
else:
    print("No duplicate sleep records found")

#Reset index after cleaning
sleep = sleep.reset_index(drop = True)

#---------------------------
# Create SleepLatency feature
#---------------------------
sleep["SleepLatency"] = (sleep["TotalTimeInBed"] - sleep["TotalMinutesAsleep"])

#Check for negative latency
negative_latency = (sleep["SleepLatency"] < 0).sum()
print(f"Negative sleep latency records: {negative_latency}")

#---------------------------
#Final Check
#---------------------------
print("\n---Cleaned Dataset Info---")
sleep.info()

print("\n---First 10 rows of Cleaned Dataset---")
print(sleep.head(10))

print("\n---Null Values After Cleaning---")
print(sleep.isnull().sum())

print("\n---Sleep Days Per User Summary---")
print(sleep.groupby("Id")["SleepDate"].nunique().describe())

print("Rows after cleaning:", len(sleep))

#----------------------------
#Save Cleaned CSV
#----------------------------
clean_path = "Data/Processed/sleepData_cleaned.csv"
sleep.to_csv(clean_path, index = False)
print(f"\nClean dataset saved to: {clean_path}")