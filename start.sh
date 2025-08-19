#!/bin/bash

# Activar entorno virtual si no usas uno gestionado por Render
# source venv/bin/activate

# Ejecutar FastAPI con Uvicorn
exec uvicorn main:app --host=0.0.0.0 --port=10000