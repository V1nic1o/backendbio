from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.api.endpoints import usuarios, eventos  # ✅ Importar routers existentes

# ✅ Crear las tablas en la base de datos si no existen
Base.metadata.create_all(bind=engine)

# ✅ Crear la app FastAPI
app = FastAPI(title="API Biométrica")

# ✅ Configurar CORS para permitir solicitudes desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Incluir routers de endpoints
app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(eventos.router, prefix="/eventos", tags=["Eventos"])