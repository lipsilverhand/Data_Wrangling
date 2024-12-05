import requests
import pandas as pd

# Read Data
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DA0321EN-SkillsNetwork/LargeData/m1_survey_data.csv"

response = requests.get(url)

file_name = "output.csv"

if response.status_code == 200:
    with open(file_name, "wb") as file:
        file.write(response.content)
    print(f"Data successfully saved to {file_name}")
else:
    print(f"Failed to fetch data, status code: {response.status_code}")


df = pd.read_csv(file_name)

# Finding duplicates
duplicate_count = df.duplicated().sum()
print(f"Number of duplicate rows: {duplicate_count}")

# Remove duplicate
remove_duplicate = df.drop_duplicates()

removed_duplicate = remove_duplicate.duplicated().sum()
print(f"Total of duplicate rows after removal: {removed_duplicate}")

remaining_rows = len(remove_duplicate)
print(f"Total rows without duplicates: {remaining_rows}")

# Finding missing values
missing_value = df.isnull().sum()
print(f"Total missing value: {missing_value}")


# Imputing missing values
if 'WorkLoc' in df.columns:
    workloc_counts = df['WorkLoc'].value_counts()
    print("Value counts for 'WorkLoc' column:")
    print(workloc_counts)

    majority_value = workloc_counts.idxmax()
    print(f"\nMost frequent value in 'WorkLoc': {majority_value}")

    # Impute missing values in 'WorkLoc' with the majority value
    df['WorkLoc'].fillna(majority_value, inplace=True)

    missing_after_imputation = df['WorkLoc'].isnull().sum()
    print(f"\nNumber of missing rows in 'WorkLoc' after imputation: {missing_after_imputation}")
else:
    print("'WorkLoc' column not found in the dataset.")


# List out the various categories in the column 'CompFreq'
if 'CompFreq' in df.columns:
    compfreq_categories = df['CompFreq'].value_counts()
    print("Categories in 'CompFreq':")
    print(compfreq_categories)
else:
    print("'CompFreq' column not found in the dataset.")

# Normalize 'CompTotal' to annual compensation
if 'CompTotal' in df.columns and 'CompFreq' in df.columns:
    # Create a mapping for frequency to multiplier
    freq_multiplier = {'Yearly': 1, 'Monthly': 12, 'Weekly': 52}

    # Create and calculate normalized annual compensation
    df['NormalizedAnnualCompensation'] = df.apply(
        lambda row: row['CompTotal'] * freq_multiplier[row['CompFreq']] 
        if row['CompFreq'] in freq_multiplier and pd.notnull(row['CompTotal']) 
        else None, axis=1
    )

    # Verify the results
    print("\nPreview of 'NormalizedAnnualCompensation':")
    print(df[['CompFreq', 'CompTotal', 'NormalizedAnnualCompensation']].head())
else:
    print("Required columns ('CompFreq' or 'CompTotal') not found in the dataset.")


if 'CompFreq' in df.columns:
    unique_values_compfreq = df['CompFreq'].nunique()
    print(f"Number of unique values in the 'CompFreq' column: {unique_values_compfreq}")
else:
    print("'CompFreq' column not found.")



