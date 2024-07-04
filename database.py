# coding=utf-8
import sqlalchemy.orm
from typing import *


# do other things
_engine: Optional[sqlalchemy.Engine] = None
class OrmBase(sqlalchemy.orm.DeclarativeBase):
    #所有的数据库操作都要基于这个类
    pass


def init():
    global _engine
    _engine = sqlalchemy.create_engine(
        'sqlite:///example.db',
        pool_size=5,  # 保持的连接数
        max_overflow=5,  # 临时的额外连接数
        pool_timeout=3,  # 连接数达到最大时获取新连接的超时时间
        # pool_pre_ping=True,  # 获取连接时先检测是否可用
        pool_recycle=60 * 60,  # 回收超过1小时的连接，防止数据库服务器主动断开不活跃的连接
        # echo=cfg.debug,  # 输出SQL语句
    )
    OrmBase.metadata.create_all(_engine)
    # print('1')

def get_session() -> sqlalchemy.orm.Session:
    return sqlalchemy.orm.Session(_engine)
