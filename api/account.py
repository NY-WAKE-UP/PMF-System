"""
@Time    : 2024/5/5 20:10
@Author  : ningyu
@FileName: account.py
@Desc    : 账户相关
"""
import os
import shutil

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel, EmailStr
from tortoise.exceptions import DoesNotExist

from api.signin import pwd_context
from models import *

account_router = APIRouter()


# 通过name查一个
@account_router.get("/{username}")
async def get_account_by_name(username: str):
    try:
        user = await UserModel.get(username=username)
        print(user)
        return user
    except Exception as e:
        print("Error:", e)
        return {"message": "User not found"}


# 删
@account_router.delete("/{account_id}")
async def delete_account(account_id: int):
    return {"message": f"删除id={account_id}的用户"}


class UserUpdate(BaseModel):
    id: int
    username: str
    password: str
    email: str
    avatar: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    avatar: str


# # 改
# UPLOAD_DIRECTORY = "/Users/ningyu/PycharmProjects/BiShe/RecSysFrontend/src/assets/avatar"
#
#
# @account_router.put("/update", summary="Update user", response_model=UserResponse)
# async def update_account(
#         id: int = Form(...),
#         username: str = Form(...),
#         password: str = Form(...),
#         email: str = Form(...),
#         file: UploadFile = File(None)
# ):
#     old_user = await UserModel.get_or_none(id=id)
#     if not old_user:
#         raise HTTPException(status_code=404, detail="User not found")
#
#     avatar_url = old_user.avatar
#     if file:
#         file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
#         os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
#         with open(file_location, "wb") as f:
#             f.write(await file.read())
#         avatar_url = f"/assets/avatar/{file.filename}"
#
#     await old_user.update_from_dict({
#         "username": username,
#         "password": password,
#         "email": email,
#         "avatar": avatar_url
#     })
#     await old_user.save()
#
#     updated_user = await UserModel.get(id=id)
#     return UserResponse(
#         id=updated_user.id,
#         username=updated_user.username,
#         email=updated_user.email,
#         avatar=updated_user.avatar,
#     )

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    avatar: str


@account_router.put("/update", summary="Update user", response_model=UserResponse)
async def update_account(
        id: int = Form(...),
        username: str = Form(...),
        email: EmailStr = Form(...),
        password: str = Form(None),
        file: UploadFile = File(None)
):
    try:
        old_user = await UserModel.get(id=id)

        if password:
            hashed_password = pwd_context.hash(password)
            old_user.password = hashed_password

        old_user.email = email
        old_user.username = username

        if file:
            file_location = f"/Users/ningyu/PycharmProjects/BiShe/RecSysFrontend/src/assets/avatar/{file.filename}"
            with open(file_location, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            old_user.avatar = "http://localhost:5173/src/assets/avatar/"+file.filename

        await old_user.save()

        return UserResponse(
            id=old_user.id,
            username=old_user.username,
            email=old_user.email,
            avatar=old_user.avatar,
        )
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")
