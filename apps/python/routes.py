from datetime import date
from fastapi import APIRouter
from db import save_user, get_user, User

router = APIRouter()


@router.put("/hello/{username}")
async def save_user_handler(username: str, date_of_birth: str):
    # Validate username
    if not username.isalpha():
        return {"message": "Username must contain only letters."}

    # Validate date_of_birth
    try:
        birth_date = date.fromisoformat(date_of_birth)
        if birth_date >= date.today():
            return {"message": "Invalid date of birth. It must be before today's date."}
    except ValueError:
        return {"message": "Invalid date format. It should be in YYYY-MM-DD format."}

    save_user(username, date_of_birth)
    return {"message": "User saved/updated successfully."}


@router.get("/hello/{username}")
async def get_user_handler(username: str):
    user = get_user(username)
    if user is None:
        return {"message": "User not found."}

    today = date.today()
    if today.month == user.date_of_birth.month and today.day == user.date_of_birth.day:
        message = f"Hello, {username}! Happy birthday!"
    else:
        days = (user.date_of_birth - today).days
        message = f"Hello, {username}! Your birthday is in {days} day(s)"

    return {"message": message}
