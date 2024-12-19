from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, EmailStr, validator
import re

app = FastAPI()


class UserRegistration(BaseModel):
    first_name: str = Field(..., min_length=2, regex="^[A-Za-zА-Яа-я]+$", description="Має містити лише літери.")
    last_name: str = Field(..., min_length=2, regex="^[A-Za-zА-Яа-я]+$", description="Має містити лише літери.")
    email: EmailStr = Field(..., description="Валідна електронна адреса.")
    password: str = Field(..., min_length=8, description="Пароль повинен бути складним.")
    phone_number: str = Field(..., regex="^\\+?[0-9]{10,15}$", description="Мобільний номер у міжнародному форматі.")

    @validator('password')
    def validate_password(cls, value):
        if not re.search(r'[A-Z]', value):
            raise ValueError("Пароль повинен містити хоча б одну велику літеру.")
        if not re.search(r'[a-z]', value):
            raise ValueError("Пароль повинен містити хоча б одну маленьку літеру.")
        if not re.search(r'[0-9]', value):
            raise ValueError("Пароль повинен містити хоча б одну цифру.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValueError("Пароль повинен містити хоча б один спеціальний символ.")
        return value


@app.post("/register")
async def register_user(user: UserRegistration):
    if user.email == "existing_user@example.com":
        raise HTTPException(status_code=400, detail="Користувач з таким email вже існує.")

    return {"message": "Користувач успішно зареєстрований!", "user": user.dict()}
