from fastapi import FastAPI
from app.routers.allergene import router as router_allergene
from app.routers.ingredient import router as router_ingredient
from app.routers.plat import router as router_plat


app = FastAPI()

app.include_router(router_allergene, prefix="/allergenes", tags=["Allergenes"])
app.include_router(router_ingredient, prefix="/ingredients", tags=["Ingredients"])
app.include_router(router_plat, prefix="/plats", tags=["Plats"])


@app.get("/health")
def health():
    return {"status": "ok"}