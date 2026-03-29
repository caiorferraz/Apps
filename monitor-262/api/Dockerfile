FROM python:3.9-slim
RUN apt-get update && apt-get install -y iputils-ping && rm -rf /var/lib/apt/lists/*
RUN pip install fastapi uvicorn
WORKDIR /app
COPY main.py .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
