import matplotlib
matplotlib.use("TkAgg")  # Set the backend to TkAgg to avoid PyCharm issues

import requests
import pandas as pd
import matplotlib.pyplot as plt

# ONS CPIH dataset endpoint
url = "https://api.beta.ons.gov.uk/v1/datasets/cpih01/editions/time-series/versions/6/observations"
params = {
    "time": "*",
    "geography": "K02000001",       # UK
    "aggregate": "cpih1dim1A0"      # Aggregate CPIH
}

# Fetch data from ONS API
response = requests.get(url, params=params)
response.raise_for_status()
data = response.json()

# Normalize the JSON to a flat table
observations = pd.json_normalize(data["observations"])

# Rename for clarity
observations["time"] = observations["dimensions.Time.label"]
observations["value"] = pd.to_numeric(observations["observation"], errors="coerce")

# Drop missing values
observations = observations.dropna(subset=["time", "value"])

# Sort by time using a custom date parser
# Convert time like "May-04" to datetime format
observations["parsed_time"] = pd.to_datetime(observations["time"], format="%b-%y", errors="coerce")

# Drop rows where date couldn't be parsed
observations = observations.dropna(subset=["parsed_time"])

# Sort by parsed time
observations = observations.sort_values("parsed_time")

# Plot the data
plt.figure(figsize=(12, 6))
plt.plot(observations["parsed_time"], observations["value"], marker='o', linestyle='-')
plt.title("UK CPIH (Consumer Prices Index including Housing Costs) Over Time")
plt.xlabel("Date")
plt.ylabel("CPIH Index Value")
plt.grid(True)
plt.tight_layout()

# Save the plot as an image (PNG)
plt.savefig("cpi_plot.png")

# Optionally show the plot (if you want to see it in a window)
# plt.show()
