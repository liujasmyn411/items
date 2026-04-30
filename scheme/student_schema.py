from datetime import date,datetime
from pydantic import BaseModel
from typing import Any, Optional, List


# 新增 / 修改 请求体
class ModifyStudentRequest(BaseModel):
    class_id: Optional[int] = None
    student_name: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    native_place: Optional[str] = None
    graduate_school: Optional[str] = None
    major: Optional[str] = None
    education: Optional[str] = None
    admission_time: Optional[date] = None
    graduate_time: Optional[date] = None
    advisor_id: Optional[int] = None


class AddStudentRequest(BaseModel):
    student_no: Optional[str] = None
    class_id: Optional[int] = None
    student_name: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    native_place: Optional[str] = None
    graduate_school: Optional[str] = None
    major: Optional[str] = None
    education: Optional[str] = None
    admission_time: Optional[date] = None
    graduate_time: Optional[date] = None
    advisor_id: Optional[int] = None


# 单条学生 响应体（ORM转JSON）
class StudentResponse(BaseModel):
    id: int
    student_no: str
    class_id: Optional[int]
    student_name: str
    gender: Optional[str]
    age: Optional[int]
    native_place: Optional[str]
    graduate_school: Optional[str]
    major: Optional[str]
    education: Optional[str]
    admission_time: Optional[date]
    graduate_time: Optional[date]
    advisor_id: Optional[int]
    is_deleted: int
    create_time: Optional[datetime]
    update_time: Optional[datetime]= None



# 列表分页响应
class StudentListResponse(BaseModel):
    records: List[StudentResponse]
    total: int



# 统一返回模板
class ResultModel(BaseModel):
    code: int
    message: str
    data:Optional[Any] = None
