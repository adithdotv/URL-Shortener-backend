from fastapi import FastAPI

from app.database.connection import Base, engine
from app.models.url_model import URL  # noqa: F401  (registers the model with Base)
from app.routes.url_routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)
