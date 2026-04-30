from datetime import date, datetime

from sqlalchemy.orm import Session
from model import Student

""" 
    step:
    查询学生列表实现分页查询
    Session 会话实现对student表的查询
    过滤条件 is_deleted == 0
    返回值类型 .json
"""


def get_student_information(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Student) \
        .filter(Student.is_deleted == 0) \
        .offset(skip) \
        .limit(limit) \
        .all()


"""
    step:
    查询student表中的学生总数
    Session 会话实现对student表中学生人数的统计
    过滤条件 is_deleted == 0
    返回值 int类型
"""


def get_student_count(db):
    return db.query(Student).filter(Student.is_deleted == 0).count()


"""
    step:
    根据学生id查询单个学生信息
"""


def get_student_by_id(db: Session, student_id: int):
    return db.query(Student) \
        .filter(Student.id == student_id) \
        .filter(Student.is_deleted == 0)\
        .first()


"""
    step:
    根据学生编号student_no查询学生信息
"""


def get_student_by_student_no(db: Session, student_no: str):
    return db.query(Student) \
        .filter(Student.student_no == student_no) \
        .filter(Student.is_deleted == 0)\
        .first()

"""
    获取学生学号
"""
def get_student_by_no(db: Session, student_no: str):
    return db.query(Student).filter(Student.student_no == student_no).first()




"""
    step:
    万能查询学生信息
"""


def get_student_by_many_conditions(
        db: Session,
        id: int | None = None,
        student_no: str | None = None,
        class_id: int | None = None,
        student_name: str | None = None,
        gender: str | None = None,
        age: int | None = None,
        native_place: str | None = None,
        graduate_school: str | None = None,
        major: str | None = None,
        education: str | None = None,
        admission_time: date | None = None,
        graduate_time: date | None = None,
        advisor_id: int | None = None,
):
    # 基础查询
    query = db.query(Student).filter(Student.is_deleted == 0)

    # ========= 所有条件：传了就加，不传就忽略 =========
    if id:
        query = query.filter(Student.id == id)
    if student_no:
        query = query.filter(Student.student_no == student_no)  # 精确
    if class_id:
        query = query.filter(Student.class_id == class_id)
    if student_name:
        query = query.filter(Student.student_name.like(f"%{student_name}%"))  # 模糊
    if gender:
        query = query.filter(Student.gender == gender)
    if age:
        query = query.filter(Student.age == age)
    if native_place:
        query = query.filter(Student.native_place.like(f"%{native_place}%"))
    if graduate_school:
        query = query.filter(Student.graduate_school.like(f"%{graduate_school}%"))
    if major:
        query = query.filter(Student.major == major)
    if education:
        query = query.filter(Student.education == education)
    if admission_time:
        query = query.filter(Student.admission_time == admission_time)
    if graduate_time:
        query = query.filter(Student.graduate_time == graduate_time)
    if advisor_id:
        query = query.filter(Student.advisor_id == advisor_id)

    return query.all()  # 返回所有符合条件的学生


"""
    step:新增学生信息
"""


# def get_student_by_student_no(db: Session, student_no: str):
#     return db.query(Student) \
#         .filter(Student.student_no == student_no) \
#         .first()

def add_student(db: Session, student_data: dict):
    db_student = Student(**student_data)
    db.add(db_student)
    db.commit()
    db_student =get_student_by_id(db, db_student.id)
    return db_student


"""
    step:修改学生信息
"""


# def update_student(db: Session, student_id: int, student_data: dict):
#     student = get_student_by_id(db, student_id)
#     if not student:
#         return None
#
#     for key, value in student_data.items():
#         if value is not None:
#             setattr(student, key, value)
#
#     db.commit()
#     return True


def update_student(db: Session, student_id: int, student_data: dict):
    student = get_student_by_id(db, student_id)
    if not student:
        return None

    # 只更新有值的字段，排除 None
    for key, value in student_data.items():
        if value is not None:
            setattr(student, key, value)

    # 自动更新时间
    student.update_time = datetime.now()

    db.commit()
    db.refresh(student)  # 刷新数据，防止返回旧值
    return True


"""
    step:软删除学生(修改is_deleted =1)
        
"""


def delete_student(db: Session, student_id: int):
    student = get_student_by_id(db, student_id)
    if not student:
        return None
    student.is_deleted = 1
    db.commit()
    return True


def get_over_30_students(db: Session,age:int):
    return (
        db.query(Student)
        .filter(Student.age > age, Student.is_deleted == 0)
        .all()
    )
