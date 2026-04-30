# 数据库的增删改查
from fastapi import HTTPException
from sqlalchemy import func, case

from model import ClassInfo as Class, Teacher, Student
from scheme.class_request import Class_update, Class_add


# 查看所有班级
def get_all_class(db):
    return db.query(Class).all()


# 查看指定条数班级
def getclass(db, skip: int, limit: int):  # 想从第几条查看，想看几条
    return db.query(Class).filter(Class.is_deleted == 0).offset(skip - 1).limit(limit).all()


# 按班级id查看指定班级
def show_class_id(db, class_id: int):
    return db.query(Class).filter(Class.class_id == class_id, Class.is_deleted == 0).first()


# 按照班级id查看指定班级的班主任和授课老师信息
def show_class_teacher(db, class_id: int):
    class_ojb = show_class_id(db, class_id)
    if not class_ojb:
        raise HTTPException(status_code=404, detail="班级不存在")
    head_teacher = db.query(Teacher).filter(Teacher.teacher_id == class_ojb.head_teacher_id,
                                            Teacher.is_deleted == 0).first()
    lecturer = db.query(Teacher).filter(Teacher.teacher_id == class_ojb.lecturer_id, Teacher.is_deleted == 0).first()
    return {
        "class_id": class_id,
        "class_name": class_ojb.class_name,
        "start_time": class_ojb.start_time.strftime("%Y-%m-%d") if class_ojb.start_time else None,
        "head_teacher": {
            "teacher_id": head_teacher.teacher_id if head_teacher else None,
            "teacher_name": head_teacher.teacher_name if head_teacher else None,
            "gender": head_teacher.gender if head_teacher else None,
            "phone": head_teacher.phone if head_teacher else None
        } if head_teacher else {"msg": "暂无班主任信息"},
        "lecturer": {
            "teacher_id": lecturer.teacher_id if lecturer else None,
            "teacher_name": lecturer.teacher_name if lecturer else None,
            "gender": lecturer.gender if lecturer else None,
            "phone": lecturer.phone if lecturer else None
        } if lecturer else {"msg": "暂无授课老师信息"}
    }


# 统计分析
# 统计每个班级的人数以及男生女生的人数
def count_classstudent(db):
    result = (db.query(Class.class_id, Class.class_name, func.count(Student.id).label("count_student"),
                       func.sum(case((Student.gender == "男", 1), else_=0)).label("count_man"),
                       func.sum(case((Student.gender == "女", 1), else_=0)).label("count_woman")).
              outerjoin(Student, (Class.class_id == Student.class_id) & (Class.is_deleted == 0)).
              filter(Class.is_deleted == 0).
              group_by(Class.class_id, Class.class_name).
              order_by(Class.class_id).
              all())
    a = []
    for class_id, class_name, count_student, count_man, count_woman in result:
        a.append({"班级id": class_id,
                  "班级名字": class_name,
                  "总人数": count_student if count_student else 0,
                  "男生人数": count_man if count_man else 0,
                  "女生人数": count_woman if count_woman else 0})
    return a


# 定义一个函数校验老师id是否存在
def check_teacher(db, teacher_id: int):
    if teacher_id is None:  # 如果teacher_id为None，则返回True
        return True
    return db.query(Teacher).filter(Teacher.teacher_id == teacher_id, Teacher.is_deleted == 0).first() is not None


# 添加班级
def create_class(db, new_class: Class_add):
    if new_class.head_teacher_id is not None:
        if not check_teacher(db, new_class.head_teacher_id):
            raise HTTPException(status_code=404, detail="班主任id不存在")
    if new_class.lecturer_id is not None:
        if not check_teacher(db, new_class.lecturer_id):
            raise HTTPException(status_code=404, detail="授课老师id不存在")
    result = Class(class_name=new_class.class_name,
                   start_time=new_class.start_time,
                   head_teacher_id=new_class.head_teacher_id,
                   lecturer_id=new_class.lecturer_id,
                   is_deleted=0)
    db.add(result)
    db.commit()
    db.refresh(result)
    return new_class


# 删除班级,逻辑删除：is_deleted=1
def deleteclass(db, calss_id: int):
    cls = show_class_id(db, calss_id)
    if not cls:
        raise HTTPException(status_code=404, detail="班级不存在")
    cls.is_deleted = 1
    db.commit()
    db.refresh(cls)
    return cls


# 修改班级信息
def updateclass(db, class_id: int, new_class: Class_update):
    cls = show_class_id(db, class_id)
    if not cls:
        raise HTTPException(status_code=404, detail="班级不存在")
    if new_class.head_teacher_id is not None:
        if not check_teacher(db, new_class.head_teacher_id):
            raise HTTPException(status_code=404, detail="班主任id不存在")
    if new_class.lecturer_id is not None:
        if not check_teacher(db, new_class.lecturer_id):
            raise HTTPException(status_code=404, detail="授课老师id不存在")
    if new_class.class_name is not None:
        cls.class_name = new_class.class_name
    if new_class.start_time is not None:
        cls.start_time = new_class.start_time
    if new_class.head_teacher_id is not None:
        cls.head_teacher_id = new_class.head_teacher_id
    if new_class.lecturer_id is not None:
        cls.lecturer_id = new_class.lecturer_id
    db.commit()
    db.refresh(cls)
    return cls
