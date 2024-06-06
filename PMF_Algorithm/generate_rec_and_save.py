#!/usr/bin/env python3

import sys

from tortoise.transactions import in_transaction

from models import MoviesModel, RecommendationsModel

sys.path.append(r'/Users/ningyu/PycharmProjects/BiShe')
sys.path.append(r'/Users/ningyu/PycharmProjects/BiShe/PMF_Algorithm')

# 算法
import numpy as np
import math
from sklearn.model_selection import train_test_split
from data import *
from evaluation import *
from pmf import *
import pickle


async def generate_rec_and_save(user_id: int):
    data_dir = '/Users/ningyu/PycharmProjects/BiShe/PMF_Algorithm/datasets/ml-100k/u.data'
    N, M, data_list, _ = load_data(file_dir=data_dir)
    train_list, test_list = train_test_split(data_list, test_size=0.2)
    train_mat = sequence2mat(sequence=train_list, N=N, M=M)
    test_mat = sequence2mat(sequence=test_list, N=N, M=M)
    K = 20
    # lambda
    lamda_regularizer = 0.1
    # 学习率
    learning_rate = 0.005
    max_iteration = 100
    model = pmf(train_list=train_list,
                test_list=test_list,
                N=N,
                M=M,
                K=K,
                P=None,
                Q=None,
                learning_rate=learning_rate,
                lamda_regularizer=lamda_regularizer,
                max_iteration=max_iteration)
    P, Q, records_array, during = model.train()
    # 保存模型
    with open('/Users/ningyu/PycharmProjects/BiShe/PMF_Algorithm/pmf_model-100k.pkl', 'wb') as f:
        pickle.dump(model, f)
    # 加载模型
    with open('/Users/ningyu/PycharmProjects/BiShe/PMF_Algorithm/pmf_model-100k.pkl', 'rb') as f:
        loaded_model = pickle.load(f)
    r_pred = loaded_model.prediction(loaded_model.P, loaded_model.Q)  # 调用 prediction 方法获取预测评分矩阵
    recommendations = loaded_model.recommendation(r_pred, num_recommendations=10)
    print(recommendations)
    movies = await MoviesModel.all().filter(Q(movie_id__in=recommendations)).order_by('-movie_rating')
    # 保存推荐电影到recommendations表
    async with in_transaction() as conn:
        for movie in movies:
            await RecommendationsModel.filter(user_id=user_id, movie_id=movie.movie_id).update(
                movie_id=movie.movie_id,
                user_id=user_id,
                movie_rating=movie.movie_rating,
                movie_title=movie.movie_title,
                tag_id=movie.genre,
                tag_name=movie.genre
            )
    print("成功更新")
    return recommendations[user_id]


async def main(user_id: int):
    await generate_rec_and_save(user_id)


# 在脚本作为主程序运行时接受命令行参数，并调用 main 函数
if __name__ == "__main__":
    import argparse
    import asyncio

    # 创建解析器
    parser = argparse.ArgumentParser(description='Run PMF Algorithm for user recommendation.')
    # 添加参数
    parser.add_argument('user_id', type=int, help='User ID for recommendation')
    # 解析参数
    args = parser.parse_args()

    # 调用 main 函数
    asyncio.run(main(args.user_id))
