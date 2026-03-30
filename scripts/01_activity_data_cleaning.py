#01_activity_data_cleaning.py
#Author: Asiya Nizam
#Purpose: Clean and Prepare Fitbit Daily Activity Data for Bellabeat Case Study

import pandas as pd

#---------------------------
#Load April-May data
#---------------------------
daily_activity = pd.read_csv("Data/Original/mturkfitbit_export_4.12.16-5.12.16/dailyActivity_merged.csv")

#---------------------------
#Inspection
#---------------------------
print("\n---------Dataset Info---------")
daily_activity.info()

print("\n-------First 10 rows of the dataset-------")
print(daily_activity.head(10))

print("\n---Unique Values Per Column---")
print(daily_activity.nunique())

print("---Unique Id Count---")
print(daily_activity['Id'].nunique())

print("\n---Null Values Per Column")
print(daily_activity.isnull().sum())

print("\nRows before cleaning:", len(daily_activity))

#----------------------------
#Clean ActivityDate Column
#----------------------------
#Convert ActivityDate from str to datetime
daily_activity['ActivityDate'] = pd.to_datetime(daily_activity['ActivityDate'], errors = 'coerce')
#Drop rows with invalid dates
invalid_dates_count = daily_activity['ActivityDate'].isnull().sum()
if invalid_dates_count > 0:
    print(f"Found {invalid_dates_count} invalid date rows. Dropping these rows.")
    daily_activity = daily_activity.dropna(subset = ['ActivityDate'])

#---------------------------
#Remove Duplicates
#---------------------------
duplicate_count = daily_activity.duplicated().sum()
if duplicate_count > 0:
    print(f"Found {duplicate_count} duplicate values. Removing duplicates.")
    daily_activity = daily_activity.drop_duplicates()
else:
    print("No duplicates found.")

#Reset index after cleaning
daily_activity = daily_activity.reset_index(drop =True)

#---------------------------
#Final Check
#---------------------------
print("\n---Cleaned Dataset Info---")
daily_activity.info()

print("\n---First 10 rows of Cleaned Dataset---")
print(daily_activity.head(10))

print("Rows after cleaning:", len(daily_activity))

#----------------------------
#Save Cleaned CSV
#----------------------------
clean_path = "Data/Processed/dailyActivity_cleaned.csv"
daily_activity.to_csv(clean_path, index = False)
print(f"\nCleaned dataset saved to: {clean_path}")

