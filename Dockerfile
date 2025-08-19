# Imagen preconfigurada de face-recognition (con dlib preinstalado)
FROM facerecognition/face_recognition:latest

# Instalar Python y herramientas
RUN apt-get update && apt-get install -y python3-pip

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos del proyecto
COPY . .

# Instalar tus dependencias (excepto face_recognition y dlib que ya están)
RUN pip install --no-cache-dir -r requirements.txt --no-deps

# Exponer puerto
EXPOSE 10000

# Ejecutar FastAPI
CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=10000"]