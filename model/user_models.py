"""
用户模块模型 - 用户表
"""
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from database import Base


class User(Base):
    """用户表"""
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True, comment="用户id")
    username = Column(String(30), nullable=False, comment="登录名")
    password = Column(String(50), nullable=False, comment="用户密码")
    avatar = Column(String(255), nullable=True, comment="头像")
    phone = Column(String(20), nullable=True, comment="手机号")
    role = Column(String(20), nullable=False, comment="登录角色")
    ref_id = Column(Integer, nullable=False, comment="关联ID（teacher或student的ID）")
    is_deleted = Column(Integer, default=0, comment="逻辑删除：默认0")
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
