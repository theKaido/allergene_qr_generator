from fastapi import FastAPI
from app.routers.allergene import router as router_allergene


app = FastAPI()

app.include_router(router_allergene, prefix="/allergenes", tags=["Allergenes"])

@app.get("/health")
def health():
    return {"status": "ok"}