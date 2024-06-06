"""
@Time    : 2024/5/14 16:18
@Author  : ningyu
@FileName: config.py
@Desc    : 配置文件
"""
DB_ORM_CONFIG = {
    "connections": {
        "default": {
            'engine': 'tortoise.backends.mysql',
            "credentials": {
                'host': '127.0.0.1',
                'user': 'root',
                'password': '66666666',
                'port': 3306,
                'database': 'RecSys',
            }
        },
    },
    "apps": {
        "models": {
            "models": ["recsys", "aerich.models"],
            "default_connection": {
                'engine': 'tortoise.backends.mysql',
                "credentials": {
                    'host': '127.0.0.1',
                    'user': 'root',
                    'password': '66666666',
                    'port': 3306,
                    'database': 'RecSys',
                    'echo': True
                }
            },
        },
        'use_tz': False,
        'timezone': 'Asia/Shanghai'
    }
}
