"""
成绩模块模型 - 成绩表
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Score(Base):
    """成绩表"""
    __tablename__ = "score"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    student_no = Column(String(50), ForeignKey("student.student_no"), nullable=False, comment="学号")
    exam_order = Column(Integer, nullable=False, comment="考试轮次")
    score = Column(Integer, nullable=False, comment="分数")

    is_deleted = Column(Integer, default=0, comment="0未删除 1已删除")
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # 关系
    student = relationship("Student", back_populates="scores")
