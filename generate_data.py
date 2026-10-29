"""Create simulated agriculture sensor dataset (dataset.csv)."""
import numpy as np, pandas as pd
rng = np.random.default_rng(42)
N = 5000
df = pd.DataFrame({
    "soil_moisture": rng.uniform(5, 80, N),     # %
    "temperature":   rng.uniform(15, 45, N),    # C
    "humidity":      rng.uniform(20, 95, N),    # %
    "light":         rng.uniform(100, 1000, N), # lux-ish
    "rainfall_24h":  rng.exponential(2, N).clip(0, 30),  # mm
})
# Rule-based ground truth + noise: irrigate when dry, hot, low humidity, no rain
score = (35 - df.soil_moisture) * 0.12 + (df.temperature - 30) * 0.08 \
        + (50 - df.humidity) * 0.03 - df.rainfall_24h * 0.15 + rng.normal(0, 0.4, N)
df["irrigate"] = (score > 0).astype(int)
df.to_csv("dataset.csv", index=False)
print(df.irrigate.value_counts())
