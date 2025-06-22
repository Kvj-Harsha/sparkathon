import requests

# Location: San Francisco, CA
latitude = 37.7749
longitude = -122.4194

# Time range: past 3 months
start_date = "2024-05-31"
end_date = "2025-05-31"
filename = f"usa_weather_fixed_{start_date}_to_{end_date}.csv"

# Valid hourly parameters for historical API
url = (
    "https://archive-api.open-meteo.com/v1/archive"
    f"?latitude={latitude}&longitude={longitude}"
    f"&start_date={start_date}&end_date={end_date}"
    "&hourly=temperature_2m,precipitation,wind_speed_10m"
    "&timezone=America%2FLos_Angeles"
    "&format=csv"
)

# Make request
response = requests.get(url)

if response.status_code == 200:
    with open(filename, "wb") as f:
        f.write(response.content)
    print(f"✅ Weather CSV saved as: {filename}")
else:
    print(f"❌ Failed to download. Status code: {response.status_code}")
    print(response.text)
