from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

#   数据库的地址
DATABASE = 'mysql+pymysql://root:123456@127.0.0.1:3306/wolin0323'

# 基于数据库地址来创建引擎
engine = create_engine(DATABASE, pool_size=5)

# 声明ORM模型基类（所有表模型都要继承这个Base）
Base = declarative_base()
# 自动提交 = 关闭 自动刷新 = 关闭
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 定义会话函数
# 创建会话对象 db，后续所有增删改查都用 db 操作
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


