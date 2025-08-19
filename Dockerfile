# Imagen base con Python y herramientas de compilación
FROM python:3.10-slim

# Instala dependencias del sistema necesarias para compilar dlib
RUN apt-get update && apt-get install -y \
    cmake \
    g++ \
    make \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    libboost-all-dev \
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . .

# Instala las dependencias de Python
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto en el que se ejecutará la app
EXPOSE 10000

# Comando para ejecutar la app
CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=10000"]