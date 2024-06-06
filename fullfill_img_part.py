"""
@Time    : 2024/5/26 16:12
@Author  : ningyu
@FileName: fullfill_img_part.py
@Desc    : 
"""

import os
import pymysql

# 连接到数据库
conn = pymysql.connect(host='localhost', user='root', password='66666666', database='RecSys')
cursor = conn.cursor()

# 获取电影数据
cursor.execute("SELECT movie_id, movie_title, year FROM movies")
movies = cursor.fetchall()

# 遍历电影数据
for movie in movies:
    movie_id, movie_title, year = movie
    # 根据电影信息获取海报图片链接（这里假设图片文件名与电影 ID 对应）
    img_url = f"http://localhost:5173/src/assets/img/{movie_id}.jpg"  # 本地文件系统示例
    # 更新数据库记录
    cursor.execute("UPDATE movies SET image_url=%s WHERE movie_id=%s", (img_url, movie_id))

# 提交事务并关闭连接
conn.commit()
conn.close()


