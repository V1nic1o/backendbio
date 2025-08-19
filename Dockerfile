# Imagen base oficial
FROM python:3.10-slim

# Instalar dependencias necesarias del sistema para compilar dlib
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    libboost-all-dev \
    libssl-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos del proyecto
COPY . .

# Actualizar pip e instalar dependencias
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto que usas en FastAPI
EXPOSE 10000

# Ejecutar la app
CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=10000"]