from typing import List, Optional
from scheme.class_request import Class_add, Class_update
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from dao.class_dao import create_class, getclass, get_all_class, show_class_id, deleteclass, \
    updateclass, show_class_teacher, count_classstudent
from database import get_db
from scheme.class_response import Classresponse

router = APIRouter(prefix="/class", tags=["王文祥-班级管理"])


@router.get("/get_class", response_model=List[Classresponse] | Classresponse, summary="查询班级（全部/单个）")
def get_class(
    class_id:   Optional[int] = Query(None, ge=1, description="班级ID，不填则查全部"),
    db=Depends(get_db)):
    # 如果传了 class_id → 查单个
    if class_id is not None:
        cls = show_class_id(db, class_id)
        if not cls:
            raise HTTPException(status_code=404, detail="班级不存在")
        return cls  # 返回单个班级
    # 没传 class_id → 返回所有班级
    return get_all_class(db)


# 查看指定条数班级
@router.get("/class", response_model=List[Classresponse], summary="查看指定条数班级")
def get_class(skip: int = Query(..., ge=1, description="从第几条查看"),
              limit: int = Query(..., ge=1, description="想看几条"), db=Depends(get_db)):
    return getclass(skip=skip, limit=limit, db=db)


# 按照班级id查看指定班级的班主任和授课老师信息
@router.get("/get_class_teacher/{class_id}", summary="按照班级id查看指定班级的班主任和授课老师信息")
def showclass_teacher(class_id: int = Path(..., ge=1, description="班级id"), db=Depends(get_db)):
    result = show_class_teacher(db, class_id)
    if not result:
        raise HTTPException(status_code=404, detail="班级不存在")
    return result


##统计分析
# 统计每个班级的人数以及男生女生的人数
@router.get("/count_class_student", summary="统计每个班级的人数以及男生女生的人数")
def count_class_student(db=Depends(get_db)):
    try:
        result = count_classstudent(db)
        return {"message": "统计成功", "result": result}
    except Exception as e:
        return {"message": f"统计失败:{str(e)}"}


# 添加班级
@router.post("/add_class", summary="添加班级")
def add_class(new_class: Class_add, db=Depends(get_db)):
    result = create_class(db, new_class)
    return {"message": "添加成功", "result": result}


# 删除班级信息
@router.delete("/get_class/{class_id}", summary="删除班级信息")
def delete_class(class_id: int = Path(..., ge=1, description="班级id"), db=Depends(get_db)):
    result = deleteclass(db, class_id)
    if not result:
        raise HTTPException(status_code=404, detail="班级不存在")
    return {"message": "删除成功"}


# 修改班级信息
@router.put("/update_class/{class_id}", response_model=Classresponse, summary="修改班级信息")
def update_class(class_id: int, new_class: Class_update, db=Depends(get_db)):
    result = updateclass(db, class_id, new_class)
    if not result:
        raise HTTPException(status_code=404, detail="班级不存在")
    return result



