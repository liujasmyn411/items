from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional

# 正确绝对导入（直接用 dao.xxx）
from database import get_db
import dao.teacher_dao as dao
from scheme.teacher_request import TeacherCreateRequest, TeacherUpdateRequest, GenderEnum
from scheme.teacher_response import TeacherResponse

router = APIRouter(prefix="/teacher", tags=["黄家胤-老师管理"])

@router.get("/get",summary="获取所有老师信息")
def get_all_teachers(db: Session = Depends(get_db)):
    return dao.get_all_teachers(db)

@router.get("/limit_get",summary="截取获取老师信息")
def teacher_limit_get(start: int = 1, end: int = 2, db: Session = Depends(get_db)):
    return dao.get_teachers_by_page(db, start, end)

@router.get("/page_get",summary="页面获取老师信息")
def teacher_page_get(page: int = 1, size: int = 5, db: Session = Depends(get_db)):
    return dao.get_teachers_page(db, page, size)

@router.post("/add",summary="添加老师信息")
def teacher_add(req: TeacherCreateRequest, db: Session = Depends(get_db)):
    dao.create_teacher(db, req)
    return {"message": "添加成功"}

@router.post("/add_photo",summary="添加老师信息（照片上传）")
def teacher_add_photo(
    teacher_name: str = Form(...),
    gender: GenderEnum = Form(...),
    phone: str = Form(...),
    photo: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    dao.create_teacher_with_photo(db, teacher_name, gender, phone, photo)
    return {"message": "添加成功（照片上传）"}

@router.delete("/delete",summary="删除老师信息（物理)（已无法使用，强关联多）")
def teacher_delete(teacher_id: int, db: Session = Depends(get_db)):
    dao.delete_teacher(db, teacher_id)
    return {"message": "删除成功"}

@router.patch("/update",summary="修改老师信息")
def teacher_update(
    teacher_id: int = Form(...),
    teacher_name: Optional[str] = Form(None),
    gender: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    is_deleted: Optional[bool] = Form(None),
    photo: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    req = TeacherUpdateRequest(
        teacher_name=teacher_name,
        gender=gender,
        phone=phone,
        is_deleted=is_deleted
    )
    dao.update_teacher(db, teacher_id, req, photo)
    return {"message": "修改成功"}

@router.get("/search", response_model=list[TeacherResponse],summary="多条件查询老师信息")
def search(
    teacher_id: Optional[int] = None,
    teacher_name: Optional[str] = None,
    gender: Optional[str] = None,
    phone: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return dao.search_teachers(db, teacher_id, teacher_name, gender, phone)