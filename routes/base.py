#base route
#default route can be used for health check
from fastapi import FastAPI, APIRouter
import os

base_router=APIRouter(
    prefix="/api/v1",
    tags=["NLP","RAG"],
)
@base_router.get("/")
async def welcome():
    app_name=os.getenv("APP_NAME")
    app_version=os.getenv("APP_VERSION")
    return {
        "App_Name ": app_name,
        "App_version":app_version,
    }