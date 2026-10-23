from contextlib import asynccontextmanager

from fastapi import Body, FastAPI

from database.db import engine
from database.models import Base

from service import generate_short_url

@asynccontextmanager # later put alembic
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)


@app.post("/short_url")
async def generate_slug(
    long_url: str = Body(embed=True),
):
    new_slug = await generate_short_url(long_url)
    return {"data": new_slug}


# @app.get("/{slug}")
# async def redirect_to_url(slug: str):
#     return ...

