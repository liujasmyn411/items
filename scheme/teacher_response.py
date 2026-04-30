from pydantic import BaseModel
from typing import Optional, List


class Classresponse2(BaseModel):
    class_id: int
    class_name: Optional[str] = None
    role:str


    class Config:
        from_attributes = True


class TeacherResponse(BaseModel):
    teacher_id: int
    teacher_name: str
    gender: str
    phone: str
    photo: Optional[str] = None

    class_list: List[Classresponse2] = []

    class Config:
        from_attributes = True