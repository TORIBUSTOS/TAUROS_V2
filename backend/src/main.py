from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.models.movement import init_db

app = FastAPI(
    title="TORO_Prime API",
    description="Motor de análisis financiero inteligente",
    version="0.1.0",
    openapi_url="/docs"
)

# CORS para frontend en localhost:7000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:7000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar DB
init_db()

@app.get("/")
def read_root():
    return {"message": "TORO_Prime API v0.1.0", "status": "ready"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000, reload=True)
