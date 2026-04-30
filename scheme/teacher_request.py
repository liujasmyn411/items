from pydantic import BaseModel
from typing import Optional
from enum import Enum
class GenderEnum(str, Enum):
    MALE = "男"
    FEMALE = "女"
class TeacherCreateRequest(BaseModel):
    teacher_name: str
    gender: str
    phone: str
    photo: Optional[str] = None



class TeacherUpdateRequest(BaseModel):
    teacher_name: Optional[str] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    is_deleted: Optional[bool] = None
    photo: Optional[str] = None



