import pandas as pd
import numpy as np

# Generate synthetic weather feature data
np.random.seed(42)  # For reproducibility
n_rows = 8500

data = {
    "temperature": np.random.uniform(low=-5, high=40, size=n_rows).round(1),      # °C
    "precipitation": np.random.uniform(low=0, high=20, size=n_rows).round(1),     # mm
    "wind_speed": np.random.uniform(low=0, high=50, size=n_rows).round(1)         # km/h
}

df_features = pd.DataFrame(data)

# Save to CSV on your local machine
file_path = "weather_features.csv"  # Saves in the current working directory
df_features.to_csv(file_path, index=False)

print(f"CSV saved to: {file_path}")
