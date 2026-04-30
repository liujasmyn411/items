from typing import Optional

from pydantic import BaseModel


# -------------------

# 响应体：登录用户信息
class UserLogin(BaseModel):
    code: int
    message: str
    username: Optional[str] = None
    avatar: Optional[str] = None

    class Config:
        from_attributes = True


# 响应体：修改用户信息
class UpdateUser(BaseModel):
    code: int
    message: str
    username: Optional[str] = None
    avatar: Optional[str] = None

    class Config:
        from_attributes = True
