from shortener import generate_random_slug
from database.crud import add_slug_to_db

async def generate_short_url(
        long_url: str
):
    slug = generate_random_slug()
    await add_slug_to_db(
        slug, long_url
    )
    return slug