from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from dao.employment_dao import add_employment, search_salary, get_employment_by_employmentid, \
    delete_employment_by_employmentid, uddataemployment, emp_search_page
from scheme.employment_schemas import employment_id, Createmployment, Updateemployment

employment_router = APIRouter(prefix='/employment', tags=["习宇龙-就业管理"])  # 创建子路由


@employment_router.get('/detail/{id}', response_model=employment_id, summary="根据ID查询就业信息",
                       description="根据就业记录ID单条查询就业信息，只返回必要字段")
def get_employment(id: int, db: Session = Depends(get_db)):
    result = get_employment_by_employmentid(db, id)
    if not result:
        raise HTTPException(status_code=404, detail='未找到就业信息')
    return result


@employment_router.delete('/remove/{id}', summary="根据ID删除就业信息",
                          description="根据就业记录ID删除就业记录")
def delete_emp(id: int, db: Session = Depends(get_db)):
    result = delete_employment_by_employmentid(db, id)
    if not result:
        raise HTTPException(status_code=404, detail='未找到就业信息')
    return {
        'code': 200,
        'message': '删除成功'
    }


@employment_router.post('/add', summary="新增就业信息",
                        description="新增就业信息，写必要字段")
def add_emp(emp: Createmployment, db: Session = Depends(get_db)):
    result = add_employment(db, emp)
    if not result:
        raise HTTPException(status_code=400, detail='新增失败')
    return {
        'code': 200,
        'message': '新增成功'
    }


@employment_router.patch('/update/{id}', summary='修改就业信息')
def change_employment(id: int, emp: Updateemployment, db: Session = Depends(get_db)):
    result = uddataemployment(db, id, emp)
    if not result:
        raise HTTPException(status_code=400, detail='修改失败')
    return {
        'code': 200,
        'message': '修改成功'
    }


@employment_router.get('/search', summary='多条件查询，空值返回全部')
def search_emp_info(
        name: str | None = None,
        company: str | None = None,
        min_sal: int | None = None,
        db: Session = Depends(get_db)
):
    return emp_search_page(
        db=db,
        name=name,
        company=company,
        min_sal=min_sal,
    )


@employment_router.get('/salary/list', summary='查询薪资')
def salray_sea(page: int = 1,
               size: int = 5,
               db: Session = Depends(get_db)):
    result = search_salary(db, page, size)
    if not result["list"]:
        return {
            "code": 200,
            "message": "暂无数据",
            "data": result
        }
    return {
        'code': 200,
        'message': '查询成功',
        "data": result
    }
