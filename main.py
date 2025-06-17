from fastapi import FastAPI
from routers.users import router
from routers.products import product
# FastAPI App
app = FastAPI()
app.include_router(router,tags=["User"])
app.include_router(product,tags=["Admin"])

# Routes
