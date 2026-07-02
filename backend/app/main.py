from fastapi import FastAPI
from app.routers.allergene import router as router_allergene
from app.routers.ingredient import router as router_ingredient
from app.routers.plat import router as router_plat
from app.routers.restaurant import router as router_restaurant
from app.routers.auth import router as router_auth


app = FastAPI()

app.include_router(router_allergene, prefix="/allergenes", tags=["Allergenes"])
app.include_router(router_ingredient, prefix="/ingredients", tags=["Ingredients"])
app.include_router(router_plat, prefix="/plats", tags=["Plats"])
app.include_router(router_restaurant, prefix="/restaurants", tags=["Restaurants"])
app.include_router(router_auth, prefix="/auth", tags=["Authentificiation"])

@app.get("/health")
def health():
    return {"status": "ok"} 