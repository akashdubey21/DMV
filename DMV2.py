!pip install requests pandas matplotlib seaborn geopandas folium

import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import folium
from datetime import datetime

API_KEY = '0d301a8ea3e07204503213f0ffd60098' 

location = 'Pune,IN'  # Specify your location (City, Country code)
url = f'http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={API_KEY}&units=metric'

response = requests.get(url)
weather_data = response.json()

data_list = weather_data['list']
weather_df = pd.DataFrame([{
    'datetime': datetime.fromtimestamp(item['dt']),
    'temperature': item['main']['temp'],
    'humidity': item['main']['humidity'],
    'wind_speed': item['wind']['speed'],
    'weather_description': item['weather'][0]['description']
} for item in data_list])

weather_df['datetime'] = pd.to_datetime(weather_df['datetime'])
weather_df.set_index('datetime', inplace=True)

weather_df['temp_max'] = weather_df['temperature'].rolling(window=3).max()
weather_df['temp_min'] = weather_df['temperature'].rolling(window=3).min()
weather_df['temp_avg'] = weather_df['temperature'].rolling(window=3).mean()

plt.figure(figsize=(12, 6))
sns.lineplot(data=weather_df, x=weather_df.index, y='temperature', label='Temperature (°C)')
sns.lineplot(data=weather_df, x=weather_df.index, y='humidity', label='Humidity (%)')
plt.title('Temperature and Humidity Over Time')
plt.xlabel('Date and Time')
plt.ylabel('Value')
plt.legend()
plt.show()

daily_weather = weather_df.resample('D').agg({
    'temperature': ['mean', 'max', 'min'],
    'humidity': 'mean',
    'wind_speed': 'mean'
})
daily_weather.columns = ['_'.join(col).strip() for col in daily_weather.columns.values]

plt.figure(figsize=(12, 6))
sns.barplot(data=daily_weather.reset_index(), x='datetime', y='temperature_mean')
plt.title('Daily Average Temperature')
plt.xlabel('Date')
plt.ylabel('Average Temperature (°C)')
plt.xticks(rotation=45)
plt.show()


# Assuming latitude and longitude are available for the location
latitude, longitude = weather_data['city']['coord']['lat'], weather_data['city']['coord']['lon']

map_weather = folium.Map(location=[latitude, longitude], zoom_start=10)
folium.Marker([latitude, longitude], popup=f'Weather in {location}').add_to(map_weather)
map_weather
