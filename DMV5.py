import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("AirQuality.csv", sep=';')

print(df.head())
print(df.info())

df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)  # Convert date column to datetime for easier plotting
print(df.columns)

# Convert pollutant levels to numeric, coercing errors to NaN
pollutant_columns = ['CO(GT)', 'PT08.S1(CO)', 'NMHC(GT)', 'C6H6(GT)', 
                        'PT08.S2(NMHC)', 'NOx(GT)', 'PT08.S3(NOx)', 
                        'NO2(GT)', 'PT08.S4(NO2)', 'PT08.S5(O3)']

for col in pollutant_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Calculate AQI based on CO (you can add calculations for other pollutants similarly)
def calculate_aqi(row):
    co_level = row['CO(GT)']
    if pd.isna(co_level):  # Check if co_level is NaN
        return None  # Or handle as needed
    if co_level <= 4.4:
        return 0  # Good
    elif co_level <= 9.4:
        return 50  # Moderate
    elif co_level <= 12.4:
        return 100  # Unhealthy for sensitive groups
    else:
        return 150  # Unhealthy

# Apply the AQI calculation
df['AQI'] = df.apply(calculate_aqi, axis=1)

plt.figure(figsize=(10, 6))
plt.plot(df['Date'], df['AQI'], label='AQI', color='b')
plt.title('Overall AQI Trend Over Time')
plt.xlabel('Date')
plt.ylabel('AQI')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()  # Adjust layout to fit labels
plt.show()

# Check the columns in your DataFrame
print(df.columns)

# Now update the plotting code accordingly
# Replace 'PM2.5', 'PM10', and 'CO' with the correct names from your DataFrame if needed
plt.figure(figsize=(10, 6))
plt.plot(df['Date'], df['CO(GT)'], label='CO', color='y')  # Replace with actual column names
# Add any other relevant pollutants here, if they exist in your DataFrame
plt.title('Pollutant Levels Over Time')
plt.xlabel('Date')
plt.ylabel('Concentration')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Task 6: Use a bar plot to compare AQI values across different dates (or time periods)
df['Month'] = df['Date'].dt.to_period('M')  # Group by month for better visualization
avg_aqi_per_month = df.groupby('Month')['AQI'].mean().reset_index()

plt.figure(figsize=(10,6))
plt.bar(avg_aqi_per_month['Month'].astype(str), avg_aqi_per_month['AQI'], color='c')
plt.title('Average AQI per Month')
plt.xlabel('Month')
plt.ylabel('AQI Value')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Check the columns in your DataFrame
print(df.columns)

# Now, create box plots using the available columns
# Update this section with actual names of the pollutants you want to analyze
plt.figure(figsize=(10, 6))
# Replace 'PM2.5', 'PM10', and 'CO' with the actual names from df.columns
sns.boxplot(data=df[['CO(GT)', 'NOx(GT)', 'C6H6(GT)']], palette="Set3")  
plt.title('Distribution of Pollutant Levels')
plt.ylabel('Pollutant Levels')
plt.show()

plt.figure(figsize=(10, 6))
plt.scatter(df['CO(GT)'], df['AQI'], color='r', alpha=0.6)  
plt.title('Scatter Plot: AQI vs CO Levels')
plt.xlabel('CO Levels')
plt.ylabel('AQI')
plt.show()
