#响应体，后端反给前端的格式
from datetime import datetime,date
from pydantic import BaseModel
from typing import Optional
class Classresponse(BaseModel):
    class_id:int
    class_name:str
    start_time:Optional[date]
    head_teacher_id:Optional[int]
    lecturer_id:Optional[int]
    create_time:datetime
    update_time:datetime

    class Config:
        from_attributes = True