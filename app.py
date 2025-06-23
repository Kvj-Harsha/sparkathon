import streamlit as st
import pandas as pd
import requests
import pydeck as pdk
import numpy as np
import math
import os
from collections import Counter

# Replace with your API keys
ORS_API_KEY = "5b3ce3597851110001cf6248c1ed620634934d4d8df158492af5aae3"
OWM_API_KEY = "2f5c6d9dee99bf305443fa425b29cde5"
HEADERS = {"User-Agent": "weather-route-app/1.0"}

st.set_page_config(page_title="🚣️ Route Weather", layout="wide")
st.title("🚣️ Route Weather Checker")

# --- Get user input ---
source = st.text_input("Enter Source Location", "Hyderabad")
destination = st.text_input("Enter Destination Location", "Bangalore")
save_csv = st.checkbox("Save route + weather data to CSV")

# --- Helper: Get coordinates from city name ---
def get_coords(city_name):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": city_name, "format": "json", "limit": 1}
    res = requests.get(url, params=params, headers=HEADERS)
    data = res.json()
    if data:
        return float(data[0]["lat"]), float(data[0]["lon"])
    return None

# --- Helper: Get place name from lat/lon ---
def get_place_name(lat, lon):
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {"lat": lat, "lon": lon, "format": "json"}
    res = requests.get(url, params=params, headers=HEADERS)
    data = res.json()
    return data.get("address", {}).get("city") or data.get("display_name", "Unknown")

# --- Helper: Get forecast for a point ---
def get_forecast(lat, lon):
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {"lat": lat, "lon": lon, "appid": OWM_API_KEY, "units": "metric"}
    res = requests.get(url, params=params)
    if res.ok:
        data = res.json()
        times = [entry["dt_txt"] for entry in data["list"][:16]]
        temps = [entry["main"]["temp"] for entry in data["list"][:16]]
        return pd.DataFrame({"Time": times, "Temperature (°C)": temps})
    return None

# --- ETA Calculation ---
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) * math.sin(dlon/2)**2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

# --- Simple rule-based risk classifier ---
def compute_risk(temp, wind, desc):
    desc = desc.lower()
    if "storm" in desc or wind > 40:
        return "High"
    elif wind > 25 or temp < 0 or "fog" in desc or "rain" in desc:
        return "Medium"
    return "Low"

# --- Main logic ---
if source and destination:
    coords_a = get_coords(source)
    coords_b = get_coords(destination)

    if coords_a and coords_b:
        st.success(f"📍 Route: {source} → {destination}")

        # Step 1: Fetch route from ORS
        ors_url = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"
        route_body = {"coordinates": [[coords_a[1], coords_a[0]], [coords_b[1], coords_b[0]]],}
        ors_headers = {"Authorization": ORS_API_KEY}

        route_res = requests.post(ors_url, json=route_body, headers=ors_headers)
        response_json = route_res.json()

        if "features" in response_json:
            feature = response_json["features"][0]
            geometry = feature["geometry"]["coordinates"]
            total_distance_km = feature["properties"]["segments"][0]["distance"] / 1000

            st.write(f"🧽 Total Distance: {total_distance_km:.2f} km")

            # ETA
            car_eta = total_distance_km / 60
            bike_eta = total_distance_km / 40
            air_eta = total_distance_km / 800
            st.info(f"Estimated Time: Car: {car_eta:.1f} h | Bike: {bike_eta:.1f} h | Air: {air_eta:.1f} h")

            # Step 2: Sample every ~50 km
            sample_stride = max(1, int(len(geometry) / (total_distance_km / 50)))
            sampled_points = geometry[::sample_stride]

            weather_data = []
            for i, (lon, lat) in enumerate(sampled_points):
                weather_url = "https://api.openweathermap.org/data/2.5/weather"
                weather_params = {"lat": lat, "lon": lon, "appid": OWM_API_KEY, "units": "metric"}
                weather_res = requests.get(weather_url, params=weather_params)
                place_name = get_place_name(lat, lon)
                if weather_res.ok:
                    weather_json = weather_res.json()
                    temp = weather_json["main"]["temp"]
                    wind = weather_json["wind"]["speed"]
                    desc = weather_json["weather"][0]["description"].capitalize()
                    risk = compute_risk(temp, wind, desc)
                    status = "Safe" if risk == "Low" else "Not Safe"
                    weather_data.append({
                        "Segment": f"{i+1}",
                        "Place": place_name,
                        "lat": lat,
                        "lon": lon,
                        "temp": temp,
                        "wind": wind,
                        "desc": desc,
                        "risk": risk,
                        "status": status
                    })

            # Final risk summary
            risks = [w["risk"] for w in weather_data]
            risk_counts = Counter(risks)
            if risk_counts["High"] > 0:
                overall_status = "High Risk"
            elif risk_counts["Medium"] > 0:
                overall_status = "Moderate Risk"
            else:
                overall_status = "Low Risk"

            st.warning(f"📊 Overall Route Risk Level: **{overall_status}**")

            # Save CSV if selected
            df = pd.DataFrame(weather_data)
            if save_csv:
                filename = f"route_weather_{source}_{destination}.csv".replace(" ", "_")
                df.to_csv(filename, index=False)
                st.success(f"Saved route weather data to {filename}")

            # Step 3: Map
            st.subheader("📻 Route with Weather Conditions")

            route_df = pd.DataFrame([{"path": geometry}])
            
            route_layer = pdk.Layer(
                "PathLayer",
                data=route_df,
                get_path="path",
                get_width=4,
                get_color=[0, 0, 255],  # blue
                width_scale=1,
                width_min_pixels=2,
                pickable=False
            )

            weather_layer = pdk.Layer(
                "ScatterplotLayer",
                data=df,
                get_position='[lon, lat]',
                get_radius=30000,
                get_fill_color='[200, 30, 0, 160]',
                pickable=True
            )

            view = pdk.ViewState(latitude=np.mean(df["lat"]), longitude=np.mean(df["lon"]), zoom=6)
            st.pydeck_chart(pdk.Deck(
                layers=[route_layer, weather_layer],
                initial_view_state=view,
                tooltip={"text": "{Place}: {temp}°C, {desc}, Risk: {risk}, Status: {status}"}
            ))

            st.subheader("🌧️ Weather Conditions Along Route")
            st.dataframe(df)

            # Step 4: Forecasts for start, mid, end
            st.subheader("🌀 2-Day Forecasts")
            a_forecast = get_forecast(*coords_a)
            b_forecast = get_forecast(*coords_b)
            mid_index = len(geometry) // 2
            mid_lat, mid_lon = geometry[mid_index][1], geometry[mid_index][0]
            mid_forecast = get_forecast(mid_lat, mid_lon)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"**{source} Forecast**")
                if a_forecast is not None:
                    st.line_chart(a_forecast.set_index("Time"))
            with col2:
                st.markdown("**Midpoint Forecast**")
                if mid_forecast is not None:
                    st.line_chart(mid_forecast.set_index("Time"))
            with col3:
                st.markdown(f"**{destination} Forecast**")
                if b_forecast is not None:
                    st.line_chart(b_forecast.set_index("Time"))

        else:
            st.error("❌ Could not fetch route from OpenRouteService")
            st.json(response_json)
    else:
        st.error("❌ Failed to get coordinates for source or destination")
