"""
@Time    : 2024/5/26 16:12
@Author  : ningyu
@FileName: update_content_part_of_mysql.py
@Desc    :
"""

import pandas as pd
import pymysql

# 连接到MySQL数据库
conn = pymysql.connect(host='localhost', user='root', password='66666666', database='RecSys')

# 读取处理后的 CSV 文件
df = pd.read_csv('movies_processed.csv', header=None)
df.dropna(inplace=True)
# 遍历DataFrame，逐行更新数据库中的content列
for index, row in df.iterrows():
    movie_title = row[1]
    description = row[5]  # 假设第六列是description
    cursor = conn.cursor()
    # 使用UPDATE语句更新movies表的content列，根据movie_title匹配
    cursor.execute("UPDATE movies SET content = %s WHERE movie_title = %s", (description, movie_title))
    conn.commit()  # 提交更改

# 关闭数据库连接
conn.close()
