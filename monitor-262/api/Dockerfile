FROM python:3.9-slim
RUN apt-get update && apt-get install -y iputils-ping && rm -rf /var/lib/apt/lists/*
WORKDIR /app
# 1. Copiamos primeiro APENAS a lista de dependências
COPY requirements.txt .
# 2. Instalamos as bibliotecas (incluindo as novas do banco de dados)
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
