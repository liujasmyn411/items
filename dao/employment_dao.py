from datetime import datetime
from sqlalchemy import and_
from sqlalchemy.orm import Session
from model import Employment, Student



#根据接口id查询就业信息
def get_employment_by_employmentid(db:Session,id:int):
    try:
        result=db.query(Employment,Student.student_name)\
            .join(Student,Employment.student_no==Student.student_no)\
            .filter(and_(Employment.employment_id==id,Employment.is_deleted==0)).first()
        if not result:
            raise None
        emp_info,student_name= result
        emp_info.student_name=student_name
        return emp_info
    except Exception as e:
        print('查询出错',e)
        return None
#删除学生信息
def delete_employment_by_employmentid(db:Session,id:int):
    try:
        result=db.query(Employment).filter(and_(Employment.employment_id==id,Employment.is_deleted==0)).first()
        if not result:
            return None
        result.is_deleted=1
        db.commit()
            #刷新数据
        db.refresh(result)
        return result
    except Exception as e :
        print('删除出错',e)
        db.rollback()
        return  None
#新增就业信息
def add_employment(db:Session,data):
    try:
     new_date=Employment(
        student_no=data.student_no,
        company_name=data.company_name,
        salary=data.salary,
        job_open_time=data.job_open_time,
        offer_send_time=data.offer_send_time,
        create_time=datetime.now(),
        update_time=datetime.now())
     db.add(new_date)
     db.commit()
     db.refresh(new_date)
     return new_date
    except Exception as e:
        print('新增出错',e)
        db.rollback()
        return None
def  uddataemployment(db:Session,id:int,data):
    try:
        result=db.query(Employment).filter(
            and_(Employment.employment_id==id,Employment.is_deleted==0)
        ).first()

        if not result:
            return None
        if data.salary is not None:
            result.salary=data.salary
        if data.company_name is not None:
            result.company_name=data.company_name
        if data.job_open_time is not None:
            result.job_open_time=data.job_open_time
        if data.offer_send_time is not None:
            result.offer_send_time=data.offer_send_time
        result.update_time=datetime.now()
        db.commit()
        db.refresh(result)


        return result
    except Exception as e:
        print('修改失败',e)
        db.rollback()
        return None
#多条件查询
def  emp_search_page(db: Session,
                     name: str = None,
                     company: str = None,
                     min_sal: int = None,
                     ):
    try:
        query=db.query(Employment,Student.student_name).join(Student,Employment.student_no==Student.student_no).\
            filter(Employment.is_deleted==0)
        if name:
            query=query.filter(Student.student_name.like(f"%{name}%"))
        if company:
            query=query.filter(Employment.company_name.like(f"%{company}%"))
        if min_sal:
            query=query.filter(Employment.salary>=min_sal)
        total = query.count()
        data_list = query.all()
        # 4. 组装返回格式（只循环一次！）
        result = []
        for emp, stu_name in data_list:
            result.append({
                "student_no": emp.student_no,
                "student_name": stu_name,  # 直接返回学生姓名
                "company_name": emp.company_name,
                "salary": emp.salary,
                "job_open_time": emp.job_open_time,
                "offer_send_time": emp.offer_send_time,
                "create_time": emp.create_time,
            })
        return {
            "total": total,
            "items": result
        }
    except Exception as e:
        print("出错：", e)
        return {
            "total": 0,
            "items": []
        }


def search_salary(db:Session,page:int=1,size:int=5):
    skip=(page-1)*size
    total = db.query(Employment).count()
    emp_list=db.query(Employment).offset(skip).limit(size).all()
    data=[]
    for emp in emp_list:
        data.append({
            "学生学号": emp.student_no,
            "学生姓名": emp.student.student_name,  # ✅ 关系
            "班级名称": emp.student.class_info.class_name,  # ✅ 关系
            "公司名称": emp.company_name,
            "薪资": emp.salary,
            "入职时间": emp.job_open_time
        })
    return {
        "total": total,  # 总条数
        "page": page,  # 当前页
        "size": size,  # 每页条数
        "list": data  # 当前页数据
    }


