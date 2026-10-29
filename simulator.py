"""Simulate an IoT sensor node sending readings to the edge API every second."""
import requests, random, time
URL = "http://127.0.0.1:8000/predict"
moisture = 50.0
while True:
    moisture = max(5, min(80, moisture + random.uniform(-6, 3)))  # drifts drier over time
    if moisture < 12: moisture = random.uniform(50, 70)            # "irrigation happened"
    data = {"soil_moisture": round(moisture, 1), "temperature": round(random.uniform(20, 42), 1),
            "humidity": round(random.uniform(25, 90), 1), "light": round(random.uniform(150, 950), 1),
            "rainfall_24h": round(random.expovariate(0.5), 1)}
    try:
        print(data, "->", requests.post(URL, json=data, timeout=3).json())
    except Exception as e:
        print("API not reachable:", e)
    time.sleep(1)
