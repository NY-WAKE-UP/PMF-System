"""
@Time    : 2024/5/29 18:21
@Author  : ningyu
@FileName: fullfill_avatar_part.py
@Desc    : 
"""
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
cursor.execute("SELECT username FROM users")
users = cursor.fetchall()

# 遍历电影数据
for user in users:
    username = user[0]
    # 根据电影信息获取海报图片链接（这里假设图片文件名与电影 ID 对应）
    avatar = f"http://localhost:5173/src/assets/avatar/{username}.png"  # 本地文件系统示例
    #   更新数据库记录
    cursor.execute("UPDATE users SET avatar=%s WHERE username=%s", (avatar, username))

# 提交事务并关闭连接
conn.commit()
conn.close()
