from datetime import datetime
from users.exceptions import EmailTaken
from users.services import get_user_by_email
from users.schemas import User


async def valid_user_create(user: User) -> User:
    if await get_user_by_email(user.email):
        raise EmailTaken()

    return user
