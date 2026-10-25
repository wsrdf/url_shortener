from contextlib import asynccontextmanager
from typing import AsyncGenerator, Annotated

from fastapi import Body, Depends, FastAPI, status, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import HttpUrl

from database.db import engine, new_session
from database.models import Base

from exceptions import NoLongUrlFoundError, SlugAlreadyExistsError
from service import generate_short_url, get_url_by_slug


@asynccontextmanager # later put alembic
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with new_session() as session:
        yield session


@app.post("/short_url")
async def generate_slug( 
    session: Annotated[AsyncSession, Depends(get_session)],
    long_url: HttpUrl = Body(embed=True),
):
    try:
        new_slug = await generate_short_url(str(long_url), session)
    except SlugAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to generate slug",
        )
    return {"data": new_slug}


@app.get("/{slug}")
async def redirect_to_url(
    slug: str, 
    session: Annotated[AsyncSession, Depends(get_session)],
):
    try:
        long_url = await get_url_by_slug(slug, session)
    except NoLongUrlFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return RedirectResponse(url=long_url, status_code=status.HTTP_302_FOUND)

