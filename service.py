from shortener import generate_random_slug
from database.crud import add_slug_to_db

async def generate_short_url(
        long_url: str # add validation w Pydanric
):
    # 1. Generate slug
    # 2. Commit to db
    # 3. Return to client
    slug = generate_random_slug()
    await add_slug_to_db(
        slug, long_url
    )
    return slug