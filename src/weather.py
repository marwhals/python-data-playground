import os
import requests
import matplotlib.pyplot as plt
from datetime import datetime

# TODO add other apis and compare readings

# London coordinates
LAT, LON = 51.5074, -0.1278
FOLDER_NAME = 'weather_plots'
os.makedirs(FOLDER_NAME, exist_ok=True)

# Yr.no API URL
url = f'https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={LAT}&lon={LON}'
headers = {
    'User-Agent': 'YourAppName/1.0 your.email@example.com'  # Required by Yr.no API
}

response = requests.get(url, headers=headers)
data = response.json()

# Extract next 12 hours of temperature data
times = []
temps = []
for i in range(24):
    entry = data['properties']['timeseries'][i]
    dt = datetime.fromisoformat(entry['time'].replace('Z', '+00:00'))
    temp = entry['data']['instant']['details']['air_temperature']
    times.append(dt.strftime('%I %p'))
    temps.append(temp)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(times, temps, marker='o', linestyle='-', color='royalblue')
plt.title('Hourly Temperature Forecast (Next 12 Hours) - London')
plt.xlabel('Time')
plt.ylabel('Temperature (°C)')
plt.grid(True)
plt.xticks(rotation=45)

# Save + show
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
filename = f"{FOLDER_NAME}/uk_hourly_forecast_{timestamp}.png"
plt.tight_layout()
plt.savefig(filename)
plt.show()
