from typing import Optional
from enum import Enum

from fastapi import UploadFile
from pydantic import BaseModel, Field, field_validator


# -------------------


class EnumRole(str, Enum):
    manager = "manager"
    teacher = "teacher"
    student = "student"


# 请求体：注册请求体信息
class UserRegister(BaseModel):
    username: str = Field(..., min_length=1, description="必传")
    password: str = Field(..., min_length=3, max_length=16, description="必传")
    phone: Optional[int] = Field(None)
    role: str = Field(...)
    # role: Optional[str] = Field(None)
    ref_id: int = Field(...)

    # @field_validator('role')
    # def validate_role(cls, v):
    #     roles = ["student", "teacher"]
    #     if v not in roles:
    #         raise ValueError("角色只能是student/teacher")
    #     return v


class Update(BaseModel):
    old_username: str
    new_username: str
    password: str | None = None
    phone: int | None = None
