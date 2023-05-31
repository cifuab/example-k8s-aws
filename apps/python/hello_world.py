from fastapi import FastAPI, HTTPException
from datetime import date
from pydantic import BaseModel
from db import create_user, get_user
import uvicorn

app = FastAPI()


class UserInput(BaseModel):
    dateOfBirth: str


@app.put("/hello/{username}", status_code=204)
def create_or_update_user(username: str, user_input: UserInput):
    if not username.isalpha():
        raise HTTPException(
            status_code=400,
            detail="Username must contain only letters.",
        )

    today = date.today()
    if date.fromisoformat(user_input.dateOfBirth) >= today:
        raise HTTPException(
            status_code=400,
            detail="Invalid date of birth. It must be a date before today.",
        )

    create_user(username, user_input.dateOfBirth)
    return None


def calculate_days_to_birthday(date_of_birth: str) -> int:
    dob = date.fromisoformat(date_of_birth)
    today = date.today()
    next_birthday = date(today.year, dob.month, dob.day)
    if next_birthday < today:
        next_birthday = date(today.year + 1, dob.month, dob.day)

    days_to_birthday = (next_birthday - today).days
    return days_to_birthday


@app.get("/hello/{username}", status_code=200)
def get_birthday_message(username: str):
    user = get_user(username)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )

    days_to_birthday = calculate_days_to_birthday(user["dateOfBirth"])

    if days_to_birthday == 0:
        message = f"Hello, {username}! Happy birthday!"
    else:
        message = f"Hello, {username}! Your birthday is in {days_to_birthday} day(s)."

    return {"message": message}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
