"""
就业模块模型 - 就业信息表
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Employment(Base):
    """就业信息表"""
    __tablename__ = 'employment'
    __table_args__ = {'extend_existing': True}

    employment_id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')
    student_no = Column(String(50), ForeignKey("student.student_no"), nullable=False, comment='外键，学生学号')
    job_open_time = Column(DateTime, nullable=False, comment='加入工作时间')
    offer_send_time = Column(DateTime, nullable=False, comment='offer发放时间')
    company_name = Column(String(100), nullable=False, comment='公司名称')
    salary = Column(Integer, nullable=False, comment='薪资')

    is_deleted = Column(Integer, default=0, comment='0未删除，1已删除')
    create_time = Column(DateTime, nullable=False, default=datetime.now, comment='创建时间')
    update_time = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    # 关系
    student = relationship("Student", back_populates="employments")
