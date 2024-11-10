import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from scipy import stats

df = pd.read_csv('Telecom_Customer_Churn.csv')


print("First five rows of the dataset:")
print(df.head())
print("\nDataset information:")
print(df.info())
print("\nSummary statistics:")
print(df.describe())

# Check column names
print("\nColumn names in the dataset:")
df.columns = df.columns.str.strip()  # Normalize column names by stripping whitespace
print(df.columns.tolist())

# Check for missing values
missing_values = df.isnull().sum()
print("\nMissing values in each column:")
print(missing_values)

# Assuming we drop rows with missing target values, fill others with mean
if 'Churn Category' in df.columns:  # Check for the correct target column
    df.dropna(subset=['Churn Category'], inplace=True)  # Drop rows where 'Churn Category' is missing
    df.fillna(df.mean(numeric_only=True), inplace=True)  # Fill other numeric missing values with mean
else:
    print("Column 'Churn Category' not found in the dataset. Please check the column names.")
    
print("\nNumber of duplicate records before removal:", df.duplicated().sum())
df.drop_duplicates(inplace=True)
print("Number of duplicate records after removal:", df.duplicated().sum())

# Example: Standardizing categorical variables
df['Gender'] = df['Gender'].str.strip().str.lower()
df['Internet Service'] = df['Internet Service'].str.strip().str.lower()  # Use the correct column name


if 'Churn Category' in df.columns:
    df['Churn Category'] = df['Churn Category'].map({'Yes': 1, 'No': 0})
    
        
# Simple outlier detection using Z-score
z_scores = np.abs(stats.zscore(df.select_dtypes(include=[np.number])))
outliers = (z_scores > 3).any(axis=1)
print("\nNumber of outliers detected:", outliers.sum())
df = df[~outliers]  # Remove outliers

# Example: Create a new feature for total charges
df['TotalCharges'] = df['Monthly Charge'] * df['Tenure in Months']

from sklearn.preprocessing import StandardScaler

# Check for missing values before scaling
print("\nMissing values before scaling:")
print(df.isnull().sum())

# Fill any remaining NaN values with mean or drop them
df.fillna(df.mean(numeric_only=True), inplace=True)

# Verify that there are no missing values
print("\nMissing values after filling:")
print(df.isnull().sum())

# Select numeric columns for scaling
numeric_cols = df.select_dtypes(include=[np.float64, np.int64]).columns
scaler = StandardScaler()

# Apply scaling
scaled_features = scaler.fit_transform(df[numeric_cols])

# Updating the DataFrame with scaled features
scaled_df = pd.DataFrame(scaled_features, columns=numeric_cols)
df = pd.concat([df.select_dtypes(exclude=[np.float64, np.int64]), scaled_df], axis=1)

X = df.drop('Churn Category', axis=1, errors='ignore')  # Features
y = df['Churn Category']  # Target variable
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


df.to_csv('Cleaned_Telecom_Customer_Churn.csv', index=False)

print("\nData cleaning and preparation completed. Cleaned dataset saved as 'Cleaned_Telecom_Customer_Churn.csv'.")        