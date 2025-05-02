import os
import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np
from scipy.interpolate import CubicSpline

# TODO add other APIs and compare readings

# London coordinates (replace with any UK city coordinates)
LAT, LON = 51.5074, -0.1278
FOLDER_NAME = 'weather_plots'
os.makedirs(FOLDER_NAME, exist_ok=True)

# Yr.no (Met.no) API URL
url = f'https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={LAT}&lon={LON}'
headers = {
    'User-Agent': 'YourAppName/1.0 your.email@example.com'  # Required by Yr.no API
}

# Fetch weather data from API
response = requests.get(url, headers=headers)
data = response.json()

# Extract next X hours of temperature data
next_x_hours: int = 24
times = []
temps = []
for i in range(next_x_hours):
    entry = data['properties']['timeseries'][i]
    dt = datetime.fromisoformat(entry['time'].replace('Z', '+00:00'))
    temp = entry['data']['instant']['details']['air_temperature']
    times.append(dt)
    temps.append(temp)

# Convert time to a numeric value (e.g., number of hours from the first point)
time_nums = np.array([(t - times[0]).total_seconds() / 3600 for t in times])

# Cubic Spline Interpolation
cs = CubicSpline(time_nums, temps)

# Generate smoothed values over a finer set of points (500 points for a smooth curve)
fine_time_nums = np.linspace(time_nums[0], time_nums[-1], 500)
smoothed_temps_spline = cs(fine_time_nums)

# Interpolated times for the smooth curve (finer grid)
fine_times = [times[0] + timedelta(seconds=int(t * 3600)) for t in fine_time_nums]

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(fine_times, smoothed_temps_spline, color='royalblue', linestyle='-', label='Smoothed')
plt.scatter(times, temps, color='red', label='Actual', zorder=5)
plt.title(f'Cubic Spline Smoothed Hourly Temperature Forecast (Next {next_x_hours} Hours) - London')
plt.xlabel('Time')
plt.ylabel('Temperature (°C)')
plt.grid(True)
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()

# Save and show the plot
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
filename = f"{FOLDER_NAME}/uk_hourly_forecast_smooth_{timestamp}.png"
plt.savefig(filename)
plt.show()
