"""Streamlit live dashboard reading predictions stored by the API."""
import sqlite3, pandas as pd, streamlit as st
from streamlit_autorefresh import st_autorefresh
st.set_page_config(page_title="Smart Irrigation", layout="wide")
st_autorefresh(interval=2000)
st.title("🌱 Smart Irrigation – Real-Time Edge ML Dashboard")
try:
    df = pd.read_sql("SELECT * FROM readings ORDER BY ts DESC LIMIT 200", sqlite3.connect("readings.db"))
except Exception:
    df = pd.DataFrame()
if df.empty:
    st.info("Waiting for sensor data... start simulator.py"); st.stop()
last = df.iloc[0]
(st.error if last.irrigate else st.success)(
    f"{'🚨 IRRIGATION NEEDED' if last.irrigate else '✅ Soil OK'} (confidence {last.probability:.0%})")
c = st.columns(5)
for col, (k, u) in zip(c, [("soil_moisture","%"),("temperature","°C"),("humidity","%"),("light","lux"),("rainfall_24h","mm")]):
    col.metric(k.replace("_"," ").title(), f"{last[k]:.1f} {u}")
d = df.sort_values("ts").set_index(pd.to_datetime(df.sort_values("ts").ts, unit="s"))
st.subheader("Soil moisture & irrigation probability"); st.line_chart(d[["soil_moisture","probability"]])
st.subheader("Temperature & humidity"); st.line_chart(d[["temperature","humidity"]])
st.metric("Irrigation alerts (last 200)", int(df.irrigate.sum()))
st.dataframe(df.head(15))
