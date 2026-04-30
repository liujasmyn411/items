from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel


class get_students(BaseModel):
    id: int
    student_no: str
    class_id: Optional[int] = None
    student_name: str
    gender: Optional[str] = None
    age: Optional[int] = None
    native_place: Optional[str] = None
    graduate_school: Optional[str] = None
    major: Optional[str] = None
    education: Optional[str] = None
    admission_time: Optional[date] = None
    graduate_time: Optional[date] = None
    advisor_id: Optional[int] = None
    is_deleted: int
    create_time: datetime
    update_time: datetime
class get_listu(BaseModel):
    message:str
    data:List[get_students]
class get_stu(BaseModel):
    message:str
    data:get_students

#增加响应体
class add_stu(BaseModel):
    id:int
    student_no:str
    class_id: Optional[int] = None
    student_name:str
    gender: Optional[str] = None
    age: Optional[int] = None
    native_place: Optional[str] = None
    graduate_school: Optional[str] = None
    major: Optional[str] = None
    education: Optional[str] = None
    admission_time:Optional[date] = None
    graduate_time:Optional[date] = None
    advisor_id: Optional[int] = None
    is_deleted:int
    create_time:datetime
    update_time:datetime
class add_student(BaseModel):
    message:str
    data:List[add_stu]

