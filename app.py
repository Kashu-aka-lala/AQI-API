import pickle
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware # Import CORS middleware
from pydantic import BaseModel
import pandas as pd
import uvicorn 

# --- Model Loading ---
MODEL_PATH = 'aqi_prediction_pipeline.pkl'
try:
    # Load the trained model pipeline
    with open(MODEL_PATH, 'rb') as file:
        model = pickle.load(file)
except Exception as e:
    print(f"ERROR: Could not load the model from {MODEL_PATH}. Exception: {e}")
    model = None

# Initialize FastAPI App
app = FastAPI(
    title="AQI Prediction API",
    description="API for predicting Air Quality Index based on pollutant concentrations.",
    version="1.0.0"
)

# --- CORS Configuration ---
# 1. Define origins (domains) allowed to access the API. 
# We use ["*"] to allow all origins, which is common for public APIs or testing.
origins = [
    "*", 
    # If you later want to restrict access, replace "*" with the domain of your frontend:
    # "https://yourfrontendapp.com" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # Allows the origins defined above
    allow_credentials=True,       # Allows cookies/authorization headers
    allow_methods=["*"],          # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],          # Allows all headers
)
# --------------------------

# --- Input Data Model (Pydantic) ---
class AQIInput(BaseModel):
    PM2_5: float
    PM10: float
    SO2: float
    O3: float
    NO2: float
    CO: float
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "PM2_5": 80.5,
                    "PM10": 120.0,
                    "SO2": 15.2,
                    "O3": 45.1,
                    "NO2": 30.0,
                    "CO": 0.8
                }
            ]
        }
    }


# --- API Endpoints ---

@app.get("/", tags=["Health Check"])
def read_root():
    """A simple health check endpoint."""
    return {"message": "AQI Prediction API is running. Access /docs for API documentation."}


@app.post("/predict", tags=["Prediction"])
def predict_aqi(data: AQIInput):
    """
    Accepts concentrations of six air pollutants and returns the predicted AQI value.
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model is unavailable. Check server logs for load errors.")

    try:
        input_dict = data.model_dump()
        
        # Map PM2_5 back to 'PM2.5' for the model
        input_data_for_model = {
            'PM2.5': input_dict.pop('PM2_5'),
            'PM10': input_dict['PM10'],
            'SO2': input_dict['SO2'],
            'O3': input_dict['O3'],
            'NO2': input_dict['NO2'],
            'CO': input_dict['CO']
        }

        # Create a Pandas DataFrame
        input_df = pd.DataFrame([input_data_for_model], 
                                columns=['PM2.5', 'PM10', 'SO2', 'O3', 'NO2', 'CO'])

        # Make prediction
        prediction = model.predict(input_df)

        return {
            "predicted_aqi": float(prediction[0]),
            "input_data": input_data_for_model
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed due to an internal error: {e}")
