"""
@Time    : 2024/5/5 20:11
@Author  : ningyu
@FileName: signin.py
@Desc    : 登录页面
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from tortoise.exceptions import DoesNotExist
from models import UserModel

signin_router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserLogin(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    email: EmailStr
    username: str


@signin_router.post("", summary="用户登录", response_model=UserResponse)
async def signin(user_login: UserLogin):
    username = user_login.username
    email = user_login.email
    password = user_login.password

    try:
        # 检查用户是否存在于数据库中
        user_data = await UserModel.get(username=username, email=email)

        # 验证密码
        if not pwd_context.verify(password, user_data.password):
            raise HTTPException(status_code=401, detail="Incorrect email or password")

        # 如果存在，返回用户信息（除了密码）
        return {"email": user_data.email, "username": user_data.username}

    except DoesNotExist:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
