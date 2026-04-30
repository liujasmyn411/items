"""
共用模型层 - 所有模块共享的基础表模型
Teacher: 教师表
Student: 学生表
ClassInfo: 班级表
"""
from datetime import datetime
from sqlalchemy import Integer, Column, String, ForeignKey, DateTime, Date, SmallInteger
from sqlalchemy.orm import relationship
from database import Base


class Teacher(Base):
    """教师表"""
    __tablename__ = 'teacher'
    __table_args__ = {'extend_existing': True}

    teacher_id = Column(Integer, primary_key=True, autoincrement=True, comment="教师ID")
    teacher_name = Column(String(50), nullable=False, comment="教师姓名")
    gender = Column(String(10), nullable=True, comment="性别")
    phone = Column(String(20), nullable=True, comment="手机号")
    photo = Column(String(255), nullable=True, comment="教师照片")
    head_classes = relationship("ClassInfo",foreign_keys="ClassInfo.head_teacher_id")
    lecturer_classes = relationship("ClassInfo",foreign_keys="ClassInfo.lecturer_id")

    is_deleted = Column(SmallInteger, default=0, comment="0未删除 1已删除")
    create_time = Column(DateTime, default=datetime.now, comment="创建时间")
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

class Student(Base):
    """学生表"""
    __tablename__ = 'student'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    student_no = Column(String(50), unique=True, nullable=False, comment="学号")

    # 外键：班级ID
    class_id = Column(Integer, ForeignKey("class_info.class_id"), nullable=True, comment="班级ID")
    # 外键：顾问老师ID
    advisor_id = Column(Integer, ForeignKey("teacher.teacher_id"), nullable=True, comment="辅导员ID")

    # 基本信息
    student_name = Column(String(50), nullable=False, comment="学生姓名")
    gender = Column(String(10), nullable=True, comment="性别")
    age = Column(Integer, nullable=True, comment="年龄")

    # 籍贯/毕业院校
    native_place = Column(String(100), nullable=True, comment="籍贯")
    graduate_school = Column(String(100), nullable=True, comment="毕业院校")
    major = Column(String(100), nullable=True, comment="专业")
    education = Column(String(20), nullable=True, comment="学历")

    # 时间
    admission_time = Column(Date, nullable=True, comment="入学时间")
    graduate_time = Column(Date, nullable=True, comment="毕业时间")

    # 通用字段
    is_deleted = Column(SmallInteger, default=0, comment="是否删除 0=未删 1=已删")
    create_time = Column(DateTime, default=datetime.now, comment="创建时间")
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    # 关系
    class_info = relationship("ClassInfo", foreign_keys=[class_id], back_populates="students")
    advisor = relationship("Teacher", foreign_keys=[advisor_id])
    scores = relationship("Score", back_populates="student")
    employments = relationship("Employment", back_populates="student")

    def to_dict(self):
        return {
            "id": self.id,
            "student_no": self.student_no,
            "class_id": self.class_id,
            "student_name": self.student_name,
            "gender": self.gender,
            "age": self.age,
            "native_place": self.native_place,
            "graduate_school": self.graduate_school,
            "major": self.major,
            "education": self.education,
            "admission_time": str(self.admission_time) if self.admission_time else None,
            "graduate_time": str(self.graduate_time) if self.graduate_time else None,
            "advisor_id": self.advisor_id,
            "is_deleted": self.is_deleted,
            "create_time": str(self.create_time) if self.create_time else None,
            "update_time": str(self.update_time) if self.update_time else None
        }


class ClassInfo(Base):
    """班级表"""
    __tablename__ = 'class_info'
    __table_args__ = {'extend_existing': True}

    class_id = Column(Integer, primary_key=True, autoincrement=True, comment="班级ID")
    class_name = Column(String(100), nullable=False, comment="班级名称")
    start_time = Column(Date, nullable=True, comment="开班时间")

    # 外键：班主任ID
    head_teacher_id = Column(Integer, ForeignKey("teacher.teacher_id",ondelete="SET NULL"), nullable=True, comment="班主任ID")
    # 外键：授课老师ID
    lecturer_id = Column(Integer, ForeignKey("teacher.teacher_id",ondelete="SET NULL"), nullable=True, comment="讲师ID")

    is_deleted = Column(SmallInteger, default=0, comment="0未删除 1已删除")
    create_time = Column(DateTime, default=datetime.now, comment="创建时间")
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    # 关系
    head_teacher = relationship("Teacher", foreign_keys=[head_teacher_id])
    lecturer = relationship("Teacher", foreign_keys=[lecturer_id])
    students = relationship("Student", back_populates="class_info")
