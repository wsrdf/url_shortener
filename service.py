from shortener import generate_random_slug
from database.crud import add_slug_to_db, get_long_url_by_slug_from_db
from exceptions import NoLongUrlFoundError, SlugAlreadyExistsError

from sqlalchemy.ext.asyncio import AsyncSession

async def generate_short_url(
        long_url: str,
        session: AsyncSession,
):
    async def _generate_slug_and_add_to_db() -> str: # rewrite with deco retry
        slug = generate_random_slug()    
        await add_slug_to_db(
            slug, long_url, session
        )
        return slug
    
    for attempt in range(5):
        try:
            slug = await _generate_slug_and_add_to_db()
            return slug
        except SlugAlreadyExistsError as e:
            if attempt == 4:
                raise SlugAlreadyExistsError from e


async def get_url_by_slug(slug: str) -> str:
    long_url = await get_long_url_by_slug_from_db(slug)
    if not long_url:
        raise NoLongUrlFoundError()
    return long_url
