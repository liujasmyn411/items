from fastapi import Depends, FastAPI, Response, HTTPException
from sqlalchemy import and_, func

from model import Student
from scheme import basemodel
app = FastAPI()

#查
#查全部   #还要看是否删除
# from pprint import pprint
# student = db.query(Student).first()
# print('\n'.join(f"{k} : {v}" for k, v in student.to_dict().items()))


#分页查询
def get_stus(db, page: int = 1, size: int = 10):
    skip = (page - 1) * size
    query = db.query(Student).filter(Student.is_deleted == 0)
    total = query.count()
    if skip >= total:        #判断总查询结果存不存在
        return []
    stus = query.offset(skip).limit(size).all()
    return  stus           # 数据列表
#按id/学号/姓名
def get_stus2(db,id,sno):
    if id:
        student = db.query(Student).filter(Student.id == id).first()
        if student:
            return student.to_dict()
        return None  # 没找到返回None

        # 2. 按学号查
    if sno:
        student = db.query(Student).filter(Student.student_no == sno).first()
        if student:
            return student.to_dict()
        return None
#查询删除数据
def get_del(db):
    a = db.query(Student).filter(Student.is_deleted == 1).all()
    return a

#增
def add_stu(stu,db):
    stu1 = Student(student_no= stu.student_no # 学号
    ,student_name=stu.student_name  # 姓名
    ,class_id = stu.class_id
    ,gender = stu.gender
    ,age = stu.age
    ,native_place = stu.native_place
    ,graduate_school = stu.graduate_school
    ,major = stu.major
    ,education = stu.education
    ,admission_time = stu.admission_time
    ,graduate_time = stu.graduate_time
    ,advisor_id = stu.advisor_id)
    db.add(stu1)
    db.flush()
    db.refresh(stu1)
    return stu1
#恢复删除学员
def recover_stu(sno, db):
    # 1. 查询已删除的学生
    result = db.query(Student).filter(
        and_(Student.student_no == sno,
        Student.is_deleted == 1)
    ).first()
    if not result:
        raise HTTPException(status_code=404, detail="该学员不存在或未被删除")
    # 2. 恢复
    result.is_deleted = 0
    db.commit()
    db.refresh(result)
    # 3. 统一格式返回
    return {
        "message": "恢复成功",
        "data": result.to_dict()
    }

#删
def del_stu(sno,db):
    result = db.query(Student).filter(Student.student_no == sno,
                                           Student.is_deleted==0).first()
    if not result:
        raise ValueError("该学员不存在或已删除")
    result.is_deleted = 1
    db.commit()
    return result.to_dict()


#改
def upda_stu(sno,stu,db):
    stu1 = db.query(Student).filter(Student.student_no == sno,
                                           Student.is_deleted == 0).first()
    if not stu1:
        raise ValueError("学生不存在货已删除")
    upda_stu = stu.dict()
    upda_stu = {k: v for k, v in upda_stu.items() if v is not None}     #过滤值为空的字段
    for k,v in upda_stu.items():
        setattr(stu1, k, v)                      #动态赋值
    db.commit()
    db.refresh(stu1)
    return stu1.to_dict()
#统计
#1年龄区间学员
def get_30(db,age_min,age_max):
    # 查询年龄区间，且未被删除的学生
    stu= db.query(Student).filter(and_(Student.age >= age_min,
                                            Student.age <= age_max,
                                            Student.is_deleted == 0)).all()
    return stu
#2.按班级统计人数
def get_class_stats(db):
    stats = db.query(
        Student.class_id,
        func.count(Student.id),  # 总人数

        # 男生统计（最兼容写法）
        func.sum(func.if_(Student.gender == "男", 1, 0)),
        # 女生统计
        func.sum(func.if_(Student.gender == "女", 1, 0))

    ).filter(
        Student.is_deleted == 0
    ).group_by(
        Student.class_id
    ).all()

    result = []
    for row in stats:
        result.append({
            "class_id": row[0],
            "total": row[1],
            "male": row[2],
            "female": row[3]
        })
    return result




