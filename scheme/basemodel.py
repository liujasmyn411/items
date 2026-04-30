from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator

#查
class get_Student(BaseModel):
    student_no: str = Field(...) # 学号
    student_name: Optional[str] # 姓名
    class_id: Optional[int]
    gender: Optional[str]
    age: Optional[int]
    native_place: Optional[str]
    graduate_school: Optional[str]
    major: Optional[str]
    education: Optional[str]
    admission_time: Optional[date]=None
    graduate_time: Optional[date]=None
    advisor_id: Optional[int]
    #防止默认值替代原有值
    @field_validator("student_no","class_id", "advisor_id","student_name","gender",
                     "age","native_place","graduate_school","major","education")

    def convert_zero_to_none(cls, v):
        if v == 0 or v == "string":
            return None
        return v


#增
class Add_Student(BaseModel):
    student_no: str=Field(...)  # 学号
    student_name: str=Field(...)  # 姓名
    class_id:int
    gender:str
    age:int
    native_place:str
    graduate_school:str
    major:str
    education:str
    admission_time:date
    graduate_time:date
    advisor_id:int
    #防止默认值代替实值
    @field_validator("class_id", "advisor_id", "student_name", "gender",
                     "age", "native_place", "graduate_school", "major", "education")
    def convert_zero_to_none(cls, v):
        if v == 0 or v == "string":
            return None
        return v
    @field_validator("admission_time", "graduate_time")
    def ignore_today(cls, v):
        if v == date.today():
            return None
        return v

#删
class Del_Student(BaseModel):
    student_no: str = Field(...)

#改
class upda_Student(BaseModel):
    student_name: Optional[str] # 姓名
    class_id: Optional[int]
    gender: Optional[str]
    age: Optional[int]
    native_place: Optional[str]
    graduate_school: Optional[str]
    major: Optional[str]
    education: Optional[str]
    admission_time: Optional[date]=None
    graduate_time: Optional[date]=None
    advisor_id: Optional[int]
    #防止默认值替代原有值
    @field_validator("class_id", "advisor_id","student_name","gender",
                     "age","native_place","graduate_school","major","education")

    def convert_zero_to_none(cls, v):
        if v == 0 or v == "string":
            return None
        return v
    @field_validator("admission_time", "graduate_time")
    def ignore_today(cls, v):
        if v == date.today():
            return None
        return v











