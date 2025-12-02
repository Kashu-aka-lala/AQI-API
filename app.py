 from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import os
import numpy as np

# Change MODEL_PATH if needed
MODEL_PATH = os.environ.get("MODEL_PATH", "model.pkl")

app = FastAPI(title="My Model API")

# Example input schema: adjust fields/types to match your model's expected features
class PredictRequest(BaseModel):
    # if model expects a list of features: use list[float]
    features: list[float]

class PredictResponse(BaseModel):
    prediction: float
    # optionally: probabilities: list[float]

@app.on_event("startup")
def load_model():
    global model
    try:
        # If you used joblib.dump to save, use joblib.load
        # For large numpy arrays inside the model, consider mmap_mode='r' (see notes)
        model = joblib.load(MODEL_PATH)
        # optionally, run a small warmup predict to instantiate internals
        # model.predict([np.zeros(n)])  # only if you know n
    except Exception as e:
        # FastAPI logs will show this; raising prevents app startup
        raise RuntimeError(f"Failed to load model: {e}")

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    try:
        features = np.array(req.features).reshape(1, -1)
        pred = model.predict(features)
        # handle classifier probability output if necessary: model.predict_proba
        return {"prediction": float(pred[0])}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
