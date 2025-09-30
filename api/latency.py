from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
import json

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

# Pydantic model for request body
class LatencyRequest(BaseModel):
    regions: list
    threshold_ms: int

# Load telemetry data (adjust path to your CSV or JSON bundle)
data = pd.read_csv("telemetry_sample.csv")  # e.g., columns: region, latency_ms, uptime

@app.post("/latency")
def get_metrics(req: LatencyRequest):
    result = {}
    for region in req.regions:
        df = data[data["region"] == region]
        avg_latency = df["latency_ms"].mean()
        p95_latency = np.percentile(df["latency_ms"], 95)
        avg_uptime = df["uptime"].mean()
        breaches = (df["latency_ms"] > req.threshold_ms).sum()
        result[region] = {
            "avg_latency": float(round(avg_latency, 2)),
            "p95_latency": float(round(p95_latency, 2)),
            "avg_uptime": float(round(avg_uptime, 2)),
            "breaches": int(breaches)
        }
    return result
