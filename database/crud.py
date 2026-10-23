from database.db import new_session
from database.models import ShortURL

async def add_slug_to_db(
        slug: str,
        long_url: str,
):
    async with new_session() as session:
        new_slug = ShortURL(
            slug = slug, 
            long_url = long_url
        )
        session.add(new_slug)
        await session.commit()
        