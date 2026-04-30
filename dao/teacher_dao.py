from sqlalchemy import null
from sqlalchemy.orm import Session
from fastapi import HTTPException
import os

# 统一导入
from model import Teacher
from scheme.teacher_request import TeacherCreateRequest, TeacherUpdateRequest


# 查所有老师
def get_all_teachers(db: Session):
    return db.query(Teacher).all()

# 分页查询
def get_teachers_by_page(db: Session, start: int = 1, end: int = 2):
    if start > end or start <= 0 or end <= 0:
        raise HTTPException(status_code=400, detail="请输入正确页面参数")
    limit = end - start + 1
    return db.query(Teacher).offset(start-1).limit(limit).all()

def get_teachers_page(db: Session, page: int = 1, size: int = 5):
    if page <= 0 or size <= 0:
        raise HTTPException(status_code=400, detail="请输入正确页面参数")
    skip = (page - 1) * size
    return db.query(Teacher).offset(skip).limit(size).all()

# 新增老师（无图）
def create_teacher(db: Session, req: TeacherCreateRequest):
    if req.gender not in ["男", "女"]:
        raise HTTPException(status_code=400, detail="性别只能是 男 或 女")
    exist = db.query(Teacher).filter(
        Teacher.teacher_name == req.teacher_name,
        Teacher.phone == req.phone
    ).first()
    if exist:
        raise HTTPException(status_code=409, detail="用户已存在")
    new_teacher = Teacher(
        teacher_name=req.teacher_name,
        gender=req.gender,
        phone=req.phone,
        photo=req.photo
    )
    db.add(new_teacher)
    db.commit()
    return new_teacher

# 新增老师（带图）
def create_teacher_with_photo(db: Session, teacher_name, gender, phone, photo):
    exist = db.query(Teacher).filter(
        Teacher.teacher_name == teacher_name,
        Teacher.phone == phone
    ).first()
    if exist:
        raise HTTPException(status_code=409, detail="用户已存在")

    photo_path = None
    if photo:
        if not os.path.exists("photos"):
            os.mkdir("photos")
        photo_path = f"photos/{photo.filename}"
        with open(photo_path, "wb") as f:
            f.write(photo.file.read())

    new_teacher = Teacher(
        teacher_name=teacher_name,
        gender=gender,
        phone=phone,
        photo=photo_path
    )
    db.add(new_teacher)
    db.commit()
    return new_teacher

# 删除老师
def delete_teacher(db: Session, teacher_id: int):
    teacher = db.query(Teacher).filter(Teacher.teacher_id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="没有这个用户")
    db.delete(teacher)
    db.commit()
    return True

# 修改老师
def update_teacher(db: Session, teacher_id: int, req: TeacherUpdateRequest, photo=None):
    if req.gender is not None and req.gender not in ["男", "女"]:
        raise HTTPException(status_code=400, detail="性别只能是 男 或 女")
    teacher = db.query(Teacher).filter(Teacher.teacher_id == teacher_id).first()
    if teacher.is_deleted==1:
        raise HTTPException(status_code=404, detail="没有这个用户")

    if req.teacher_name is not None and req.teacher_name != "":
        teacher.teacher_name = req.teacher_name
    if req.gender is not None and req.gender != "":
        teacher.gender = req.gender
    if req.phone is not None and req.phone != "":
        teacher.phone = req.phone
    if req.is_deleted is not None:
        teacher.is_deleted = req.is_deleted

    if photo:
        if not os.path.exists("photos"):
            os.mkdir("photos")
        photo_path = f"photos/{photo.filename}"
        with open(photo_path, "wb") as f:
            f.write(photo.file.read())
        teacher.photo = photo_path

    db.commit()
    return teacher

# 条件搜索老师
def search_teachers(db: Session, teacher_id=None, teacher_name=None, gender=None, phone=None):
    query = db.query(Teacher).filter(Teacher.is_deleted==0)
    if teacher_id is not None:
        query = query.filter(Teacher.teacher_id == teacher_id)
    if teacher_name is not None:
        query = query.filter(Teacher.teacher_name == teacher_name)
    if gender is not None:
        query = query.filter(Teacher.gender == gender)
    if phone is not None:
        query = query.filter(Teacher.phone == phone)

    result = query.all()

    for teacher in result:
        class_list=[]
        for c in teacher.head_classes:
            data={**c.__dict__,"role":"班主任"}
            class_list.append(data)

        for d in teacher.lecturer_classes:
            data={**d.__dict__,"role":"任课老师"}
            class_list.append(data)

        teacher.class_list=class_list
    if not result:
        raise HTTPException(status_code=404, detail="没有这个用户")

    return result