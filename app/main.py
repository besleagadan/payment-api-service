from fastapi import FastAPI
from app.api.v1 import api_router

app = FastAPI()

@app.get("/health")
def healthcheck():
    return {"status": "ok"}

app.include_router(api_router, prefix="/api/v1")
