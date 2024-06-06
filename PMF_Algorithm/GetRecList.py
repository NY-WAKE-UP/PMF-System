"""
@Time    : 2024/5/28 15:15
@Author  : ningyu
@FileName: GetRecList.py
@Desc    : 
"""
import sys

sys.path.append("/Users/ningyu/PycharmProjects/BiShe/PMF_Algorithm")

# 算法
import numpy as np
import math
from sklearn.model_selection import train_test_split
from data import *
from evaluation import *
from pmf import *
import pickle


def get_rec(user_id: int):
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
    return recommendations[user_id]
