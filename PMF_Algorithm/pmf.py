import numpy as np
import random
from data import *
from evaluation import *


class pmf():
    def __init__(self,
                 train_list,  # train_list: train data
                 test_list,  # test_list: test data
                 N,  # N:the number of user
                 M,  # M:the number of item
                 P,
                 Q,
                 K=10,  # K: the number of latent factor
                 learning_rate=0.001,  # learning_rate: the learning rata
                 lamda_regularizer=0.1,  # lamda_regularizer: regularization parameters
                 max_iteration=50  # max_iteration: the max iteration
                 ):
        self.train_list = train_list
        self.test_list = test_list
        self.N = N
        self.M = M
        self.K = K
        self.learning_rate = learning_rate
        self.lamda_regularizer = lamda_regularizer
        self.max_iteration = max_iteration
        self.P = P
        self.Q = Q

    def train(self):
        self.P = np.random.normal(0, 0.1, (self.N, self.K))
        self.Q = np.random.normal(0, 0.1, (self.M, self.K))

        train_mat = sequence2mat(sequence=self.train_list, N=self.N, M=self.M)
        test_mat = sequence2mat(sequence=self.test_list, N=self.N, M=self.M)

        records_list = []
        # 早停
        pre_rmse = 100.0
        endure_count = 3
        patience = 0
        start = time.time()
        for step in range(self.max_iteration):
            los = 0.0
            for data in self.train_list:
                u, i, r = data
                self.P[u], self.Q[i], ls = self.update(self.P[u], self.Q[i], r=r,
                                                       learning_rate=self.learning_rate,
                                                       lamda_regularizer=self.lamda_regularizer)
                los += ls
            pred_mat = self.prediction(self.P, self.Q)
            mae, rmse, recall, precision = evaluation(pred_mat, train_mat, test_mat)
            records_list.append(np.array([los, mae, rmse, recall, precision]))
            F_value = 2 * recall * precision / (recall + precision)

            if step % 10 == 0:
                print(' step:%d \n loss:%.4f,mae:%.4f,rmse:%.4f,recall:%.4f,precision:%.4f,F-value:%.4f'
                      % (step, los, mae, rmse, recall, precision, F_value))
            if rmse < pre_rmse:  # 早停
                pre_rmse = rmse
                patience = 0
            else:
                patience += 1
            if patience >= endure_count:
                print(' step:%d \n loss:%.4f,mae:%.4f,rmse:%.4f,recall:%.4f,precision:%.4f,F-value:%.4f'
                      % (step, los, mae, rmse, recall, precision, F_value))
                break

        print(' end. \n loss:%.4f,mae:%.4f,rmse:%.4f,recall:%.4f,precision:%.4f'
              % (
                  records_list[-1][0], records_list[-1][1], records_list[-1][2], records_list[-1][3],
                  records_list[-1][4]))
        end = time.time()
        during = end - start
        return self.P, self.Q, np.array(records_list), during

    # def train(self, batch_size=16):
    #     P = np.random.normal(0, 0.1, (self.N, self.K))
    #     Q = np.random.normal(0, 0.1, (self.M, self.K))

    #     train_mat = sequence2mat(sequence=self.train_list, N=self.N, M=self.M)
    #     test_mat = sequence2mat(sequence=self.test_list, N=self.N, M=self.M)

    #     records_list = []
    #     for step in range(self.max_iteration):
    #         los = 0.0
    #         for batch_start in range(0, len(self.train_list), batch_size):
    #             batch_end = min(batch_start + batch_size, len(self.train_list))
    #             batch_data = self.train_list[batch_start:batch_end]
    #             batch_loss = 0.0
    #             for data in batch_data:
    #                 u, i, r = data
    #                 P[u], Q[i], ls = self.update(P[u], Q[i], r=r,
    #                                             learning_rate=self.learning_rate,
    #                                             lamda_regularizer=self.lamda_regularizer)
    #                 batch_loss += ls
    #             los += batch_loss / len(batch_data)

    #         pred_mat = self.prediction(P, Q)
    #         mae, rmse, recall, precision = evaluation(pred_mat, train_mat, test_mat)
    #         records_list.append(np.array([los, mae, rmse, recall, precision]))

    #         if step % 10 == 0:
    #             print(' step:%d \n loss:%.4f,mae:%.4f,rmse:%.4f,recall:%.4f,precision:%.4f'
    #                 % (step, los, mae, rmse, recall, precision))

    #     print(' end. \n loss:%.4f,mae:%.4f,rmse:%.4f,recall:%.4f,precision:%.4f'
    #         % (records_list[-1][0], records_list[-1][1], records_list[-1][2], records_list[-1][3], records_list[-1][4]))
    #     return P, Q, np.array(records_list)

    def update(self, p, q, r, learning_rate=0.001, lamda_regularizer=0.1):  # 随机梯度下降
        error = r - np.dot(p, q.T)
        p = p + learning_rate * (error * q - lamda_regularizer * p)
        q = q + learning_rate * (error * p - lamda_regularizer * q)
        loss = 0.5 * (error ** 2 + lamda_regularizer * (np.square(p).sum() + np.square(q).sum()))
        return p, q, loss

    def prediction(self, P, Q):
        N, K = P.shape
        M, K = Q.shape

        rating_list = []
        for u in range(N):
            u_rating = np.sum(P[u, :] * Q, axis=1)
            rating_list.append(u_rating)
        r_pred = np.array(rating_list)
        return r_pred

    def print_rec_list(self):
        r_pred = self.prediction(self.P, self.Q)  # 调用 prediction 方法获取预测评分矩阵
        recommendations = self.recommendation(r_pred, num_recommendations=5)
        print(recommendations)

    # def recommendation(self, r_pred, num_recommendations=5):
    #     # 获取预测评分矩阵的形状
    #     N, M = r_pred.shape
    #
    #     # 存储推荐列表的字典，键为用户索引，值为推荐的物品索引列表
    #     recommendations = {}
    #
    #     # 对每个用户生成推荐列表
    #     for u in range(N):
    #         # 获取用户 u 的预测评分
    #         user_ratings = r_pred[u]
    #
    #         # 找出评分最高的 num_recommendations 个物品的索引
    #         top_indices = np.argsort(user_ratings)[::-1][:num_recommendations]
    #
    #         # 将推荐列表存储到字典中
    #         recommendations[u] = top_indices.tolist()
    #
    #     return recommendations
    def recommendation(self, r_pred, num_recommendations=5):
        # 获取预测评分矩阵的形状
        N, M = r_pred.shape

        # 存储推荐列表的字典，键为用户索引，值为推荐的物品索引列表
        recommendations = {}

        # 集合用于跟踪已处理的用户索引
        user_set = set()

        # 对每个用户生成推荐列表
        for u in range(N):
            # 检查是否已有重复用户
            if u in user_set:
                print(f"Duplicate user found: {u}")
                continue

            # 将用户添加到集合中
            user_set.add(u)

            # 获取用户 u 的预测评分
            user_ratings = r_pred[u]

            # 找出评分最高的 num_recommendations 个物品的索引
            top_indices = np.argsort(user_ratings)[::-1][:num_recommendations]

            # 将推荐列表存储到字典中
            recommendations[u] = top_indices.tolist()

        # 打印总用户数和推荐字典中的用户数
        print(f"Total unique users: {len(user_set)}")
        print(f"Total recommendations: {len(recommendations)}")

        return recommendations
