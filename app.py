import pickle
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import uvicorn # Required for local testing, though Render uses the command directly

# --- Model Loading ---
MODEL_PATH = 'aqi_prediction_pipeline.pkl'
try:
    # Load the trained model pipeline
    with open(MODEL_PATH, 'rb') as file:
        model = pickle.load(file)
except Exception as e:
    # This will raise an error on startup if the model file is missing or corrupted
    print(f"ERROR: Could not load the model from {MODEL_PATH}. Exception: {e}")
    model = None

# Initialize FastAPI App
app = FastAPI(
    title="AQI Prediction API",
    description="API for predicting Air Quality Index based on pollutant concentrations.",
    version="1.0.0"
)

# --- Input Data Model (Pydantic) ---
# Defines the structure and data types for the API input
class AQIInput(BaseModel):
    # Note: Using PM2_5 as a valid Python variable name,
    # it will be converted back to 'PM2.5' for the model
    PM2_5: float
    PM10: float
    SO2: float
    O3: float
    NO2: float
    CO: float
    
    # Example values for FastAPI's auto-generated documentation
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
        # Convert Pydantic model to a dictionary
        input_dict = data.model_dump()
        
        # Map the valid Python key (PM2_5) back to the expected feature name ('PM2.5')
        # The other keys already match
        input_data_for_model = {
            'PM2.5': input_dict.pop('PM2_5'),
            'PM10': input_dict['PM10'],
            'SO2': input_dict['SO2'],
            'O3': input_dict['O3'],
            'NO2': input_dict['NO2'],
            'CO': input_dict['CO']
        }

        # Create a Pandas DataFrame (required by scikit-learn pipelines/models)
        input_df = pd.DataFrame([input_data_for_model], 
                                columns=['PM2.5', 'PM10', 'SO2', 'O3', 'NO2', 'CO'])

        # Make prediction
        prediction = model.predict(input_df)

        # Return the prediction (convert numpy float to standard Python float)
        return {
            "predicted_aqi": float(prediction[0]),
            "input_data": input_data_for_model
        }

    except Exception as e:
        # Handle errors during prediction
        raise HTTPException(status_code=500, detail=f"Prediction failed due to an internal error: {e}")

# If you want to test locally, you can uncomment this:
# if __name__ == "__main__":
#     uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
