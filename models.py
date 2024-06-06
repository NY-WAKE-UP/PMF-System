"""
@Time    : 2024/5/14 16:19
@Author  : ningyu
@FileName: models.py
@Desc    : orm模型
"""

from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator


class MoviesModel(Model):
    movie_id = fields.IntField(pk=True)
    movie_title = fields.CharField(max_length=255, description='电影名', null=True)
    year = fields.IntField(description='发布日期', null=True)
    genre = fields.CharField(max_length=255, description='电影类型', null=True)
    movie_rating = fields.FloatField(description='评分', null=True)
    content = fields.TextField(description='详情', null=True)
    image_url = fields.CharField(max_length=255, description='海报', null=True)

    class Meta:
        table = 'movies'


MoviePydantic = pydantic_model_creator(MoviesModel, name='Movie')


class RecommendationsModel(Model):
    id = fields.IntField(pk=True)
    movie_id = fields.IntField(description='电影id', null=True)
    user_id = fields.IntField(description='用户id', null=True)
    movie_rating = fields.FloatField(description='评分', null=True)
    movie_title = fields.CharField(max_length=255, description='电影名')
    tag_id = fields.CharField(max_length=255, description="电影类型id")
    tag_name = fields.CharField(max_length=255, description="电影标签名")

    class Meta:
        table = 'recommendations'


RecommendationsPydantic = pydantic_model_creator(RecommendationsModel, name='Recommendations')


class UserModel(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=255, description='用户名', null=True)
    password = fields.CharField(max_length=255, description='密码', null=True)
    email = fields.CharField(max_length=255, description='邮箱', null=True)
    avatar = fields.CharField(max_length=255, description='头像', null=True)
    tag_id = fields.CharField(max_length=255, description='喜好标签id', null=True)

    class Meta:
        table = 'users'


UserPydantic = pydantic_model_creator(UserModel, name='User')


class TagModel(Model):
    tag_id = fields.IntField(pk=True)
    tag_name = fields.CharField(max_length=255, description='标签名', null=True)

    class Meta:
        table = 'tags'


TagPydantic = pydantic_model_creator(TagModel, name='Tag')


class RatingModel(Model):
    movie_rating = fields.FloatField(description='评分', null=True)
    user_id = fields.IntField(description='用户id', null=True)
    movie_id = fields.IntField(description='电影id', null=True)

    class Meta:
        table = 'ratings'


RatingsPydantic = pydantic_model_creator(RatingModel, name='Ratings')


class FavoriteModel(Model):
    user_id = fields.IntField(description='用户id', null=True)
    movie_id = fields.IntField(description='电影id', null=True)

    class Meta:
        table = 'favorites'


FavoritesPydantic = pydantic_model_creator(FavoriteModel, name='Favorites')
