from starlette.staticfiles import StaticFiles

from api.settings import settings_router
from api.home import home_router
from api.signin import signin_router
from api.signup import signup_router
from api.movies import movies_router
from api.account import account_router
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from config import DB_ORM_CONFIG
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(settings_router, prefix="/settings", tags=["settings"])
app.include_router(home_router, prefix="/home", tags=["home"])
app.include_router(signin_router, prefix="/signin", tags=["signin"])
app.include_router(signup_router, prefix="/signup", tags=["signup"])
app.include_router(account_router, prefix="/account", tags=["account"])
app.include_router(movies_router, prefix="/movies", tags=["movies"])

# fastapi一旦启动，就运行 实现监控
register_tortoise(
    app=app,
    db_url='mysql://root:66666666@127.0.0.1:3306/RecSys',
    modules={'models': ['models']},
    # generate_schemas=True,
    # add_exception_handlers=True,
)
origins = ['http://127.0.0.1:5173', "http://localhost:5173","https://api.wmdb.tv"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



