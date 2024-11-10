import pandas as pd
import numpy as np

df = pd.read_csv('RealEstate_Prices.csv')

# Clean column names (remove spaces, special characters, and standardize)
df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace('[^A-Za-z0-9_]+', '')

# View the cleaned column names
print("Cleaned Column Names:", df.columns)

# Option 1: Drop rows with missing values
df_cleaned = df.dropna()

# Option 2: Impute missing values with mean (for numerical columns)
df.fillna(df.mean(), inplace=True)

# For categorical columns, fill missing values with mode (most frequent value)
for column in df.select_dtypes(include=['object']).columns:
    df[column].fillna(df[column].mode()[0], inplace=True)

# Convert 'X1_transaction_date' to a numeric or date format
df['X1_transaction_date'] = pd.to_numeric(df['X1_transaction_date'], errors='coerce')  # Convert to numeric if it's in a number format

# Now we can filter based on transaction date, assuming it represents a year
df_filtered = df[df['X1_transaction_date'] >= 2010]



# Example: Calculate average house price by number of convenience stores
avg_price_by_convenience = df.groupby('X4_number_of_convenience_stores')['Y_house_price_of_unit_area'].mean().reset_index()

# Example: Using IQR method to detect outliers in 'Y_house_price_of_unit_area'
Q1 = df['Y_house_price_of_unit_area'].quantile(0.25)
Q3 = df['Y_house_price_of_unit_area'].quantile(0.75)
IQR = Q3 - Q1

# Define lower and upper bounds for outliers
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Filter out outliers from the dataset
df_no_outliers = df[(df['Y_house_price_of_unit_area'] >= lower_bound) & (df['Y_house_price_of_unit_area'] <= upper_bound)]


# View summary statistics after outlier removal
print("Summary Statistics after Outlier Removal:")
print(df_no_outliers['Y_house_price_of_unit_area'].describe())

# Export the cleaned dataset for further analysis or modeling
df_no_outliers.to_csv('Cleaned_RealEstate_Prices.csv', index=False)

print("Data Wrangling Completed.")
    