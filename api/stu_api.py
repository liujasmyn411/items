from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from pymysql import MySQLError
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from dao import stu_dao
from scheme import basemodel,response
import database

stu_router = APIRouter(tags=["者俊-学生管理"])

#查
#分页查询
@stu_router.get("/get_stus"
    , summary="学生信息分页查询",response_model = response.get_listu
                )
def get_stus(db = Depends(database.get_db),page:int=1,size:int=10):
    stu1 = stu_dao.get_stus(db, page, size)
    if not stu1:
        raise HTTPException(status_code=404,detail="所查页高于总页数或暂无数据")
    return {"message":"查询成功","data":stu1}
#根据学号/id查询
@stu_router.get("/get_name"
    , summary="按学号/id查询",response_model = response.get_stu)
def get_name(db = Depends(database.get_db), id: Optional[int] =None, sno:Optional[str]=None):
    if not id and not sno:
        if not id and not sno:
            raise HTTPException(status_code=400,detail="请传入 id 或 sno")
    stu_data = stu_dao.get_stus2(db,id,sno)
    if not stu_data:
        raise HTTPException(status_code=404,detail="学生不存在")
    return {"message": "查询成功", "data": stu_data}
#查删除项
@stu_router.get("/get_del"
    , summary="查询删除数据",response_model = response.get_listu)
def get_del(db = Depends(database.get_db)):
    stu1 = stu_dao.get_del(db)
    if not stu1:
        raise HTTPException(status_code=404,detail="暂无已删除的学生数据")
    return {"message": "查询成功", "data": stu1}
#增
@stu_router.post("/add_stu"
    , summary="学生添加",response_model = response.add_student
                 )
def add_stu(stus:List[basemodel.Add_Student],db = Depends(database.get_db)):
    stus_data = []
    try:
        for stu in stus:
            stu1 = stu_dao.add_stu(stu, db)
            stus_data.append(stu1)
        db.commit()
    except IntegrityError as e:
        db.rollback()
            # 捕获数据库唯一键重复异常（学号重复）
        if isinstance(e.orig, MySQLError) and e.orig.args[0] == 1062:
            raise HTTPException(status_code=400, detail=f"学号已存在，不可重复添加,未添加任何数据")
            # 其他数据库异常
        raise HTTPException(status_code=400, detail=f"添加失败：数据错误{str(e)},未添加任何数据")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"服务器错误：{str(e)},未添加任何数据")
    return {"message":"添加成功","data":stus_data}
#恢复删除项
@stu_router.get("/recov_stu"
    , summary="学生数据恢复",response_model = response.get_stu
                 )
def recov_stu(sno:str=Query(...),db = Depends(database.get_db)):
    try:
        result = stu_dao.recover_stu(sno,db)
        return result
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"服务器错误：{str(e)}")

#删
@stu_router.delete("/del_stu"
    ,summary="学生删除"
    ,response_model=response.get_stu,description="根据学生学号进行软删除，并非真删除，只是标记is_deleted=1")
def del_stu(sno:str=Query(...),db = Depends(database.get_db)):
    try:
        result = stu_dao.del_stu(sno,db)
        return {"message":"删除成功","data":result}
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"服务器错误：{str(e)}")

#改
@stu_router.put("/update_stu"
    ,summary="学生修改",response_model = response.get_stu)
def upda_stu(sno:str,stu:basemodel.upda_Student,db = Depends(database.get_db)):
    try:
        result = stu_dao.upda_stu(sno,stu, db)
        return {"message": "修改成功", "data": result}
        # 捕获学号重复/数据错误
    except IntegrityError as e:
        db.rollback()
        # 数据库错误：重复、非空、约束
        if isinstance(e.orig, MySQLError) and e.orig.args[0] == 1062:
            raise HTTPException(status_code=400, detail="唯一项重复，修改失败")
        raise HTTPException(status_code=400, detail="数据错误，修改失败")
    # 学生不存在
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))
    # 服务器异常
    except Exception as e:
        db.rollback()
        # 未知错误：代码崩了、服务挂了
        raise HTTPException(status_code=500, detail=f"服务器错误：{str(e)}")
#统计
#1.不同年龄段学员信息
@stu_router.get("/over_30",
    summary="年龄区间的学员信息",response_model = response.get_listu)
def get_over_30(db=Depends(database.get_db),age_min:int=30,age_max:int=30):
    data = stu_dao.get_30(db,age_min,age_max)
    if not data:
        raise HTTPException(status_code=404,detail="该年龄区间没有学员")
    return {"message":"查询成功","data":data}

#2.按班级统计人数
@stu_router.get("/class_stats",
    summary="按班级统计人数、男生、女生")
def get_class_stats(db=Depends(database.get_db)):
    data = stu_dao.get_class_stats(db)
    return {"message": "统计成功","data": data}


