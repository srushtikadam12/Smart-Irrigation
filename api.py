"""FastAPI service: loads the 'production' model from MLflow registry, serves predictions."""
import mlflow, pandas as pd, sqlite3, time
from fastapi import FastAPI
from pydantic import BaseModel

mlflow.set_tracking_uri("sqlite:///mlflow.db")
model = mlflow.sklearn.load_model("models:/irrigation-model@production")
app = FastAPI(title="Smart Irrigation Edge API")

DB = "readings.db"
with sqlite3.connect(DB) as c:
    c.execute("""CREATE TABLE IF NOT EXISTS readings(ts REAL, soil_moisture REAL, temperature REAL,
                 humidity REAL, light REAL, rainfall_24h REAL, irrigate INT, probability REAL)""")

class Reading(BaseModel):
    soil_moisture: float
    temperature: float
    humidity: float
    light: float
    rainfall_24h: float

@app.post("/predict")
def predict(r: Reading):
    X = pd.DataFrame([r.model_dump()])
    p = float(model.predict_proba(X)[0][1])
    irrigate = int(p >= 0.5)
    with sqlite3.connect(DB) as c:
        c.execute("INSERT INTO readings VALUES (?,?,?,?,?,?,?,?)",
                  (time.time(), *r.model_dump().values(), irrigate, p))
    return {"irrigate": irrigate, "probability": round(p, 3),
            "alert": "IRRIGATION NEEDED" if irrigate else "OK"}

@app.get("/health")
def health(): return {"status": "up"}
