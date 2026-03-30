# Base Python leve
FROM python:3.9-slim-bullseye

# Instala as dependências de sistema para FFT e processamento de áudio
# fftw3 é a biblioteca mais rápida do mundo para FFT
RUN apt-get update && apt-get install -y \
    gcc \
    gfortran \
    libatlas-base-dev \
    libfftw3-dev \
    libasound2-dev \
    python3-pyaudio \
    gstreamer1.0-tools \
    gstreamer1.0-plugins-base \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instala as bibliotecas Python de elite para áudio
# numpy: matemática vetorial pura
# scipy: processamento de sinal avançado (FFT, filtros)
# librosa: a melhor biblioteca para análise musical
RUN pip install --no-cache-dir numpy scipy librosa pydantic fastapi 'uvicorn[standard]'

COPY . .

CMD ["python", "main.py"]
