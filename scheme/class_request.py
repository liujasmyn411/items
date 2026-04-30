#请求体，前端传给后端的格式
from datetime import date
from pydantic import BaseModel, Field
from typing import Optional #Optional可以为空也可以填写
class Class_add(BaseModel):#新增班级
    class_name:str=Field(...,min_length=1,max_length=30,description="新增班级名称") #新增班级名称
    start_time:Optional[date]=None #新增开课时间
    head_teacher_id:Optional[int]=Field(None,description="新增班主任id") #新增班主任id
    lecturer_id:Optional[int]=Field(None,description="新增授课老师id") #新增授课老师id

class Class_update(BaseModel):#修改班级
    class_name:str=Field(...,min_length=1,max_length=30,description="修改班级名称")
    start_time:Optional[date]=None
    head_teacher_id:Optional[int]=Field(None,description="修改班主任id")
    lecturer_id:Optional[int]=Field(None,description="修改授课老师id")
