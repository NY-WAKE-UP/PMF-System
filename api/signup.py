from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, validator
from passlib.context import CryptContext
from email_validator import validate_email, EmailNotValidError
from tortoise.exceptions import DoesNotExist

from models import UserModel

signup_router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserSignUp(BaseModel):
    username: str
    email: str
    password: str

    @validator('email')
    def email_must_be_valid(cls, v):
        try:
            validate_email(v)
        except EmailNotValidError:
            raise ValueError('无效的电子邮件地址')
        return v

@signup_router.post("", summary="注册接口")
async def signup(form_data: UserSignUp):
    """
    拿到前端传来的数据
    校验看是否已经存在
    保存到数据库
    给前端相应信息
    :return:
    """
    username = form_data.username
    email = form_data.email
    password = form_data.password
    if not username or not email or not password:
        raise HTTPException(status_code=400, detail="用户名、电子邮件或密码不能为空")

    # 检查用户名是否已存在
    try:
        user_by_username = await UserModel.get(username=username)
        if user_by_username:
            raise HTTPException(status_code=400, detail="用户名已存在")
    except DoesNotExist:
        pass

    # 检查电子邮件是否已存在
    try:
        user_by_email = await UserModel.get(email=email)
        if user_by_email:
            raise HTTPException(status_code=400, detail="电子邮件已存在")
    except DoesNotExist:
        pass

    # 在存储之前对密码进行哈希处理
    hashed_password = pwd_context.hash(password)

    # 创建新用户
    await UserModel.create(username=username, email=email, password=hashed_password,avatar="http://localhost:5173/src/assets/avatar/"+username+".png")
    return {"message": "用户创建成功"}
