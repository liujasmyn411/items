from datetime import datetime
from pydantic import BaseModel, field_serializer, Field, validator

class employment_id(BaseModel):
    student_no: str
    student_name: str
    company_name: str
    salary: int = Field(..., ge=0)
    job_open_time: datetime
    offer_send_time: datetime
    create_time: datetime

    @field_serializer('job_open_time', 'offer_send_time', 'create_time')
    def serialize_all_datetime(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%d %H:%M:%S")

    model_config = {"from_attributes": True}

# 创建
class Createmployment(BaseModel):
    student_no: str = Field(...)
    salary: int = Field(..., ge=0)
    company_name: str = Field(..., min_length=2, max_length=50)
    job_open_time: datetime = Field(...)
    offer_send_time: datetime = Field(...)

    @validator('job_open_time', 'offer_send_time', pre=True)
    def parse_date(cls, v):
        if isinstance(v, str):
            v = v.replace("Z", "")  # 去掉 Z
            dt = datetime.fromisoformat(v)  # 解析 ISO 格式
            return dt.date()  # 只保留 年-月-日
        return v

# 修改
class Updateemployment(BaseModel):
    salary: int | None = None
    company_name: str | None = None
    job_open_time: datetime | None = None
    offer_send_time: datetime | None = None

    @validator('job_open_time', 'offer_send_time', pre=True)
    def parse_date(cls, v):
        if v is None:
            return v
        if isinstance(v, str):
            v = v.replace("Z", "")
            dt = datetime.fromisoformat(v)
            return dt.date()
        return v





