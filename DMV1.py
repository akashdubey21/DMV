import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load CSV file
df_csv = pd.read_csv('sales_data.csv' )

# Load Excel file
df_excel = pd.read_excel('sales_data.xls')

# Load JSON file
df_json = pd.read_json('sales_data.json')

print("CSV Data:")
print(df_csv.head())
print(df_csv.info())

print("\nExcel Data:")
print(df_excel.head())
print(df_excel.info())

print("\nJSON Data:")
print(df_json.head())
print(df_json.info())
print(df_json.columns)

# Forward fill for missing values in the CSV data
df_csv.ffill(inplace=True)  # Using the recommended method

# Remove duplicates in Excel data
df_excel.drop_duplicates(inplace=True)

# Drop rows with missing values in 'Quantity' (or any relevant column) in JSON data
df_json.dropna(subset=['Quantity'], inplace=True)  # Adjust the column name if necessary

print("CSV DataFrame after cleaning:")
print(df_csv.head())

print("Excel DataFrame after cleaning:")
print(df_excel.head())

print("JSON DataFrame after cleaning:")
print(df_json.head())

# Concatenate all dataframes into a single dataframe
df_combined = pd.concat([df_csv, df_excel, df_json], ignore_index=True)
print(df_combined.columns)

# Deriving a new variable for total sales
df_combined['Total Sales'] = df_combined['QUANTITYORDERED'] * df_combined['PRICEEACH']
# Check the original DataFrame
print(df_combined.head())

# Check if the Total Sales column exists and is calculated correctly
print(df_combined[['Total Sales']].head())

print(sales_by_category.isnull().sum())


# Descriptive statistics
print("\nDescriptive Statistics:")
print(df_combined.describe())

# Descriptive statistics
print("\nDescriptive Statistics:")
print(df_combined.describe())

# Make sure 'Total Sales' column exists and is correctly calculated
df_combined['Total Sales'] = df_combined['Quantity'] * df_combined['Sales']

# Then aggregate by category
sales_by_category = df_combined.groupby('Category')['Total Sales'].sum().reset_index()


# Display the aggregated sales by category
print("\nSales by Category:")
print(sales_by_category)

plt.figure(figsize=(10, 6))
sns.barplot(data=sales_by_category, x='Category', y='Total Sales', palette='viridis')
plt.title('Total Sales by Product Category')
plt.xlabel('Product Category')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Pie chart for sales distribution
plt.figure(figsize=(8, 8))
plt.pie(sales_by_category['Total Sales'], labels=sales_by_category['Category'], autopct='%1.1f%%', startangle=140)
plt.title('Sales Distribution by Product Category')
plt.axis('equal')  # Equal aspect ratio ensures that pie chart is circular.
plt.show()
