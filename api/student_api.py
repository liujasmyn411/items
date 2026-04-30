from datetime import date, datetime

from sqlalchemy.orm import Session

from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from dao import student_dao
from scheme.student_schema import StudentResponse, StudentListResponse, ModifyStudentRequest, AddStudentRequest
from scheme.student_schema import ResultModel

student_router = APIRouter(tags=['杨征昊-学生管理'])

"""
    查询学生信息api接口
    分页查询
"""


@student_router.get("/students/list", summary="学生信息分页查询", response_model=ResultModel)
async def get_student_list(skip: int = 0, limit: int = 10, db=Depends(get_db)):
    students = student_dao.get_student_information(db, skip, limit)
    records = [StudentResponse(**s.__dict__) for s in students]
    total = student_dao.get_student_count(db)
    return ResultModel(
        code=200,
        message='查询成功',
        data=StudentListResponse(records=records, total=total))


"""
    查询学生信息api接口
    stu_id查询
"""


@student_router.get("/students/v1/{stu_id}", summary="学生id信息查询", response_model=ResultModel)
def get_student_detail(stu_id: int, db: Session = Depends(get_db)):
    stu = student_dao.get_student_by_id(db, stu_id)
    if not stu:
        raise HTTPException(status_code=404, detail="学生不存在")
    data = StudentResponse(**stu.__dict__)
    return ResultModel(code=200, message="查询成功", data=data)


"""
    查询学生信息api接口
    student_no查询
"""


@student_router.get("/students/v2/{student_no}", summary="学生编号信息查询", response_model=ResultModel)
def get_student_detail(student_no: str, db: Session = Depends(get_db)):
    stu = student_dao.get_student_by_student_no(db, student_no)
    if not stu:
        raise HTTPException(status_code=404, detail="学生不存在")
    data = StudentResponse(**stu.__dict__)
    return ResultModel(code=200, message="查询成功", data=data)


"""
    查询学生信息api接口
    万能查询
"""


@student_router.get("/students/search", summary="多条件学生信息查询", response_model=ResultModel)
def search_students(
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
        db: Session = Depends(get_db)
):
    students = student_dao.get_student_by_many_conditions(
        db=db,
        id=id,
        student_no=student_no,
        class_id=class_id,
        student_name=student_name,
        gender=gender,
        age=age,
        native_place=native_place,
        graduate_school=graduate_school,
        major=major,
        education=education,
        admission_time=admission_time,
        graduate_time=graduate_time,
        advisor_id=advisor_id
    )

    if not students:
        raise HTTPException(status_code=404, detail="未查询到学生信息")
    data = [StudentResponse(**stu.__dict__) for stu in students]
    return ResultModel(
        code=200,
        message="查询成功",
        data=data
    )


"""
    删除学生信息api接口
"""


@student_router.delete("/delete/{stu_id}", summary="删除学生信息", response_model=ResultModel)
def del_student(stu_id: int, db: Session = Depends(get_db)):
    try:
        stu = student_dao.delete_student(db, stu_id)
        if not stu:
            raise HTTPException(status_code=400, detail="删除失败,未查询到学生信息")
        return ResultModel(code=200, message="删除成功")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"服务器异常：{str(e)}")


"""
    修改学生信息api接口
"""


@student_router.put("/update/{stu_id}", summary="修改学生信息", response_model=ResultModel)
def update_student(stu_id: int, item: ModifyStudentRequest, db: Session = Depends(get_db)):
    try:
        stu = student_dao.update_student(db, stu_id, item.dict())
        if not stu:
            raise HTTPException(status_code=400, detail="修改失败,未查询到学生信息")
        return ResultModel(code=200, message="修改成功")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"服务器异常：{str(e)}")


"""
    添加学生信息api接口
"""


@student_router.post("/add", summary="添加学生信息", response_model=ResultModel)
def add_student(item: AddStudentRequest, db: Session = Depends(get_db)):
    try:
        exists_stu = student_dao.get_student_by_no(db, item.student_no)
        if exists_stu:
            return ResultModel(code=400, message="学号已存在，无法添加", data=None)
        stu = student_dao.add_student(db, item.dict())
        data = StudentResponse(**stu.__dict__)
        return ResultModel(code=200, message="添加成功", data=data)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"服务器异常：{str(e)}")


"""
    统计分析
"""


@student_router.get("/over-age", summary="年龄区间学生查询", response_model=ResultModel)
def get_over_age(age: int, db: Session = Depends(get_db)):
    try:
        students = student_dao.get_over_30_students(db, age)
        data = [StudentResponse(**stu.__dict__) for stu in students]
        total = len(data)
        return ResultModel(code=200, message="查询成功", data=StudentListResponse(total=total, records=data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
