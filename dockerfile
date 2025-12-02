FROM python:3.11-slim

# create app dir
WORKDIR /app

# copy requirements first (for faster rebuilds)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# copy model and app
COPY model.pkl ./model.pkl
COPY app.py ./app.py

# set environment variables
ENV MODEL_PATH=/app/model.pkl
ENV PYTHONUNBUFFERED=1

# expose port
EXPOSE 8000

# Use a production ASGI server with multiple workers
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
