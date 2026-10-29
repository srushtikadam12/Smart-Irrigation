# Smart Irrigation – Real-Time ML on IoT/Edge

**Use case:** Smart Agriculture. Sensors (soil moisture, temperature, humidity, light, rainfall) → ML model decides if irrigation is needed.

## Workflow
Simulated sensor (simulator.py) → FastAPI edge service (api.py) → MLflow-registered RandomForest → alert + SQLite log → Streamlit dashboard (dashboard.py)

## Run (4 terminals, in this folder)
    pip install -r requirements.txt
    python generate_data.py        # makes dataset.csv (5000 rows)
    python train.py                # trains + registers model in MLflow (alias: production)
    uvicorn api:app --port 8000    # edge inference API
    python simulator.py            # fake IoT sensor, 1 reading/sec
    streamlit run dashboard.py     # live dashboard
    mlflow ui --backend-store-uri sqlite:///mlflow.db   # model registry UI (screenshot this)

## Result
RandomForest: accuracy 0.96, F1 0.94 on 20% hold-out.

## Report outline
1. Problem & use case  2. Architecture diagram  3. Dataset (features, simulation logic)
4. Model training & metrics  5. MLflow tracking/registry (versions, alias)  6. API integration
7. Simulation  8. Dashboard & alerts  9. Screenshots  10. Conclusion & future work (real ESP32/Raspberry Pi, MQTT, model drift monitoring)
