# 🌫️ Air Quality Index (AQI) Prediction API

This repository contains a simple, production-ready RESTful API built with **FastAPI** to predict the Air Quality Index (AQI) based on concentrations of key air pollutants.

The prediction is powered by a pre-trained machine learning model pipeline (`aqi_prediction_pipeline.pkl`).

## 🚀 Features

  * **FastAPI Backend:** A modern, high-performance Python web framework.
  * **Prediction Endpoint:** A robust `/predict` endpoint for AQI calculation.
  * **Pydantic Validation:** Ensures data integrity for all incoming requests.
  * **Production Ready:** Configured for easy deployment on platforms like Render using Gunicorn and Uvicorn.
  * **Self-Documenting:** Automatic interactive API documentation available at the `/docs` path (Swagger UI).

## 📁 Repository Structure

```
.
├── aqi_prediction_pipeline.pkl  # The pre-trained scikit-learn model pipeline
├── app.py                       # The FastAPI application
├── requirements.txt             # Project dependencies
└── README.md                    # This file
```

## 🛠️ Local Setup and Installation

Follow these steps to get a local copy of the project running.

### Prerequisites

  * Python 3.8+
  * `pip` (Python package installer)

### Steps

1.  **Clone the Repository:**

    ```bash
    git clone <YOUR_REPO_URL>
    cd <your-repo-name>
    ```

2.  **Create a Virtual Environment (Recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use: venv\Scripts\activate
    ```

3.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the API Server:**

    ```bash
    uvicorn app:app --host 0.0.0.0 --port 8000 --reload
    ```

    The API will now be running at `http://127.0.0.1:8000`.

## 💻 API Usage

The main endpoint for making predictions is `/predict`.

### 1\. Endpoint Details

  * **URL:** `/predict`
  * **Method:** `POST`
  * **Description:** Accepts pollutant concentrations and returns the predicted AQI.

### 2\. Request Body

The request must be a JSON object containing the following six pollutant concentrations as floating-point numbers:

| Field   | Data Type | Description                              |
| :------ | :-------- | :--------------------------------------- |
| `PM2_5` | `float`   | Particulate Matter (2.5 µm)              |
| `PM10`  | `float`   | Particulate Matter (10 µm)               |
| `SO2`   | `float`   | Sulfur Dioxide concentration             |
| `O3`    | `float`   | Ozone concentration                      |
| `NO2`   | `float`   | Nitrogen Dioxide concentration           |
| `CO`    | `float`   | Carbon Monoxide concentration            |

**Example Request (`JSON`):**

```json
{
    "PM2_5": 80.5,
    "PM10": 120.0,
    "SO2": 15.2,
    "O3": 45.1,
    "NO2": 30.0,
    "CO": 0.8
}
```

### 3\. Response

A successful response (Status Code `200`) will return the predicted AQI value:

**Example Response (`JSON`):**

```json
{
    "predicted_aqi": 125.45,
    "input_data": {
        "PM2.5": 80.5,
        "PM10": 120.0,
        "SO2": 15.2,
        "O3": 45.1,
        "NO2": 30.0,
        "CO": 0.8
    }
}
```

## ☁️ Deployment on Render (or other PaaS)

This application is designed for easy deployment on platforms like **Render** or Heroku.

### Render Configuration

When setting up your Web Service on Render, use the following configuration:

| Setting         | Value                                                              |
| :-------------- | :----------------------------------------------------------------- |
| **Runtime** | `Python 3`                                                         |
| **Build Command** | `pip install -r requirements.txt`                                  |
| **Start Command** | `gunicorn app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT` |
