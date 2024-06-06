import os
import time
from typing import List

import pandas as pd
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette.background import BackgroundTasks
from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.expressions import Q
from tortoise.transactions import in_transaction

from PMF_Algorithm import GetRecList
from models import *  # 导入电影模型

import sys
import random

sys.path.append("/Users/ningyu/PycharmProjects/BiShe/PMF_Algorithm")

movies_router = APIRouter()


# external_api_base_url = "https://api.wmdb.tv"

class Movie(BaseModel):
    movie_id: int
    movie_title: str
    year: int
    genre: str
    movie_rating: float
    img_url: str


class Rating(BaseModel):
    movie_id: int
    username: str
    rating: float


@movies_router.get("/content/{movieTitle}", summary='description for movies')
async def get_content(movieTitle: str):
    movie_content = await MoviesModel.get(movie_title=movieTitle)
    return movie_content.content


# 搜索
@movies_router.get("/search/{movieTitle}", summary="movie searching")
async def get_content(movieTitle: str):
    movies = await MoviesModel.all().filter(Q(movie_title__contains=movieTitle))
    movie_list = [Movie(
        movie_id=movie.movie_id,
        movie_title=movie.movie_title,
        year=movie.year,
        genre=movie.genre,
        movie_rating=movie.movie_rating,
        img_url=movie.image_url
    ) for movie in movies]
    return movie_list


@movies_router.post("/ratings", summary='rating')
async def create_rating(rating: Rating):
    try:
        user = await UserModel.get(username=rating.username)
        user_id = user.id
        # 创建评分对象并保存到数据库中
        created_rating = await RatingModel.update_or_create(
            defaults={"movie_rating": rating.rating},
            user_id=user_id,
            movie_id=rating.movie_id
        )
        # 将评分记录写入 u.data 文件
        timestamp = int(time.time())
        with open("/Users/ningyu/PycharmProjects/BiShe/PMF_Algorithm/datasets/ml-100k/u.data", 'a') as file:
            file.write(f"{user_id + 943}\t{rating.movie_id}\t{rating.rating}\t{timestamp}\n")

        return created_rating
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to create rating")


@movies_router.get("/random", response_model=List[Movie], summary='random movies for rating')
async def get_random_movies():
    movies = await MoviesModel.all()
    total_movies = len(movies)
    random_indices = random.sample(range(total_movies), 10)
    random_movies = [movies[i] for i in random_indices]
    movie_list = [
        Movie(
            movie_id=movie.movie_id,
            movie_title=movie.movie_title,
            year=movie.year,
            genre=movie.genre,
            movie_rating=movie.movie_rating,
            img_url=movie.image_url
        )
        for movie in random_movies
    ]

    return movie_list


@movies_router.get("/popular", response_model=List[Movie], summary='popular movies top 10')
async def get_movies():
    # 读取和解析 u.data 文件
    df = pd.read_csv("/Users/ningyu/PycharmProjects/BiShe/PMF_Algorithm/datasets/ml-100k/u.data", sep='\t',
                     names=['user_id', 'item_id', 'rating', 'timestamp'])

    # 统计每个电影的评分次数
    rating_counts = df['item_id'].value_counts().to_dict()

    # 按评分次数排序并获取前十
    sorted_movie_ids = sorted(rating_counts, key=rating_counts.get, reverse=True)[:10]

    # 查询排序后的电影数据
    movies = await MoviesModel.filter(movie_id__in=sorted_movie_ids)

    # 将查询结果转换为字典，以便后续排序
    movies_dict = {movie.movie_id: movie for movie in movies}

    # 按照 sorted_movie_ids 的顺序构建结果列表
    movie_list = [Movie(
        movie_id=movies_dict[movie_id].movie_id,
        movie_title=movies_dict[movie_id].movie_title,
        year=movies_dict[movie_id].year,
        genre=movies_dict[movie_id].genre,
        movie_rating=movies_dict[movie_id].movie_rating,
        img_url=movies_dict[movie_id].image_url
    ) for movie_id in sorted_movie_ids if movie_id in movies_dict]

    return movie_list


async def update_recommendations(user_id: int, user_id_offset: int):
    # 生成新的推荐结果
    new_recommendations = GetRecList.get_rec(user_id=user_id_offset)
    # 清除旧的推荐结果
    # await RecommendationsModel.filter(user_id=user_id).delete()
    # 插入新的推荐结果
    async with in_transaction() as conn:
        for movie_id in new_recommendations:
            movie = await MoviesModel.get(movie_id=movie_id)
            await RecommendationsModel.update_or_create(
                movie_id=movie.movie_id,
                user_id=user_id,
                movie_rating=movie.movie_rating,
                movie_title=movie.movie_title,
                tag_id=movie.genre,
                tag_name=movie.genre
            )
    print("update success")


@movies_router.get("/recommend/{user_id}", response_model=List[Movie], summary='recommend movie')
async def get_movie_recommendation(user_id: int, background_tasks: BackgroundTasks):
    user_id_offset = user_id + 942
    recommendations_exist = await RecommendationsModel.filter(user_id=user_id).exists()

    if recommendations_exist:
        # 如果推荐结果已存在，从recommendations表中获取推荐电影
        recommendations = await RecommendationsModel.filter(user_id=user_id)
        movie_ids = [rec.movie_id for rec in recommendations]
    else:
        # 如果没有推荐结果，生成新的推荐结果
        recommendations = GetRecList.get_rec(user_id=user_id_offset)  # 十部电影的id
        movie_ids = recommendations

    # 查询电影数据
    movies = await MoviesModel.filter(movie_id__in=movie_ids).order_by('-movie_rating')

    # 构建电影列表
    movie_list = [
        Movie(
            movie_id=movie.movie_id,
            movie_title=movie.movie_title,
            year=movie.year,
            genre=movie.genre,
            movie_rating=movie.movie_rating,
            img_url=movie.image_url
        )
        for movie in movies
    ]

    # 无论推荐结果是否存在，后台任务都进行推荐结果更新
    background_tasks.add_task(update_recommendations, user_id, user_id_offset)

    return movie_list


@movies_router.get("/rated/{user_id}", summary='get rated movies', response_model=List[Movie])
async def get_movie_rated(user_id: int):
    ratings = await RatingModel.all().filter(Q(user_id=user_id)).order_by('-movie_id')
    movie_ratings = [rating.movie_rating for rating in ratings]
    movie_ids = [movie.movie_id for movie in ratings]

    movies = await MoviesModel.filter(Q(movie_id__in=movie_ids)).order_by('-movie_id')

    movie_list = []
    for movie, rating in zip(movies, movie_ratings):
        movie_list.append(Movie(
            movie_id=movie.movie_id,
            movie_title=movie.movie_title,
            year=movie.year,
            genre=movie.genre,
            movie_rating=rating,
            img_url=movie.image_url
        ))

    movie_list.sort(key=lambda movie: movie.movie_rating, reverse=True)

    return movie_list


# 新的路由，用于获取特定类型的电影
@movies_router.get("/genre/{genre}", response_model=List[Movie], summary='get movies by genre')
async def get_movies_by_genre(genre: str):
    movies = await MoviesModel.all().filter(Q(genre__contains=genre)).order_by('-movie_rating')
    movie_list = [Movie(
        movie_id=movie.movie_id,
        movie_title=movie.movie_title,
        year=movie.year,
        genre=movie.genre,
        movie_rating=movie.movie_rating,
        img_url=movie.image_url
    ) for movie in movies]
    return movie_list


@movies_router.post("/")
async def add_movie(movie: Movie):
    movie_obj = await MoviesModel.create(**movie.dict())
    return await MoviesModel.get(id=movie_obj.id)


@movies_router.delete("/{movie_id}")
async def delete_movie(movie_id: int):
    deleted_count = await MoviesModel.filter(id=movie_id).delete()
    if not deleted_count:
        raise HTTPNotFoundError(detail="Movie not found")
    return {"msg": f"Movie with id={movie_id} deleted successfully"}


@movies_router.put("/{movie_id}")
async def update_movie(movie_id: int, movie: Movie):
    await MoviesModel.filter(id=movie_id).update(**movie.dict(exclude_unset=True))
    return await MoviesModel.get(id=movie_id)


@movies_router.get("/details/{movie_id}", summary='get movie details')
async def get_movie(movie_id: int):
    movie = await MoviesModel.get(movie_id=movie_id)
    if movie is None:
        raise HTTPNotFoundError(detail="Movie not found")
    return movie
