from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.api.endpoints import usuarios, eventos  # ✅ Importar routers

# ✅ Crear las tablas en la base de datos si no existen
Base.metadata.create_all(bind=engine)

# ✅ Instanciar la app FastAPI
app = FastAPI(title="API Biométrica")

# ✅ Configurar CORS (desarrollo + producción)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",       # Vite local
        "http://127.0.0.1:5173",       # Alternativa local
        "https://tusitio.vercel.app",  # (opcional) dominio de Vercel si lo usas
        "*",                           # ⚠️ OPCIONAL: permitir desde cualquier origen (solo si lo deseas)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Incluir los routers
app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(eventos.router, prefix="/eventos", tags=["Eventos"])