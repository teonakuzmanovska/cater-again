from contextlib import asynccontextmanager

from app.database import Base, engine
from app.routes import router
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Supplier Catalog",
    docs_url="/suppliers/docs",
    openapi_url="/suppliers/openapi.json",
    lifespan=lifespan
)

app.include_router(router)