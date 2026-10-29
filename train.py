"""Train model and register it in the MLflow Model Registry."""
import mlflow, mlflow.sklearn, pandas as pd
from mlflow.models import infer_signature
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("smart-irrigation")
MODEL_NAME = "irrigation-model"

df = pd.read_csv("dataset.csv")
X, y = df.drop(columns="irrigate"), df["irrigate"]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

with mlflow.start_run():
    params = {"n_estimators": 100, "max_depth": 8, "random_state": 42}
    model = RandomForestClassifier(**params).fit(Xtr, ytr)
    pred = model.predict(Xte)
    acc, f1 = accuracy_score(yte, pred), f1_score(yte, pred)
    mlflow.log_params(params)
    mlflow.log_metrics({"accuracy": acc, "f1": f1})
    mlflow.sklearn.log_model(model, name="model", signature=infer_signature(Xtr, pred),
                             registered_model_name=MODEL_NAME,
                             serialization_format="cloudpickle")
    print(f"accuracy={acc:.3f} f1={f1:.3f}")

client = mlflow.MlflowClient()
latest = max(int(v.version) for v in client.search_model_versions(f"name='{MODEL_NAME}'"))
client.set_registered_model_alias(MODEL_NAME, "production", str(latest))
print(f"Registered {MODEL_NAME} v{latest} -> alias 'production'")
