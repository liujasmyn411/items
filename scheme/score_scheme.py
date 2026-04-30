from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from enum  import Enum


# ------------------------------
# 1. 基础模型：包含所有字段（查询、详情用）
# ------------------------------
class ScoreBase(BaseModel):
    id: Optional[int] = Field(None, description="成绩ID")
    student_no: str = Field(..., description="学生学号")
    exam_order: Optional[int] = Field(None, description="考核序次")
    score: Optional[float] = Field(None, description="考核成绩")
    is_deleted: Optional[int] = Field(0, description="逻辑删除 0-未删除 1-已删除")
    create_time: Optional[datetime] = Field(None, description="创建时间")
    update_time: Optional[datetime] = Field(None, description="更新时间")

    # 让 Pydantic 支持 ORM 对象（必须加！）
    class Config:
        from_attributes = True

# ------------------------------
# 2.查询成绩模型(响应体)
# ------------------------------
class SelectScore(BaseModel):
    id:int= Field(description="成绩ID")
    student_no: str = Field(description="学生学号")
    student_name: str = Field(description="考核成绩")
    exam_order: Optional[int] = Field(description="考核序次")
    score: Optional[float] = Field(description="考核成绩")

# ------------------------------
# 3. 创建成绩模型(请求体)
# ------------------------------
class ScoreCreate(BaseModel):
    student_no: str = Field(..., description="学生学号")
    exam_order: Optional[int] = Field(...,ge=1,description="考核序次")
    score: Optional[float] = Field(...,le=100,ge=0,description="考核成绩")


# ------------------------------
# 4. 更新成绩模型(请求体)
# ------------------------------
class ScoreUpdate(BaseModel):
    id: int = Field(...,description="成绩ID")
    score: Optional[float] = Field(..., ge=0, description="考核成绩")

# ------------------------------
# 5. 删除成绩模型(请求体)
# ------------------------------
class ScoreDelete(BaseModel):
    id: int = Field(...,description="成绩ID")


# ------------------------------
# 6. 每次考试成绩都在80分以上的学生
# ------------------------------
class ScoreEighty(BaseModel):
    student_no: str = Field(description="学生学号")
    student_name: str = Field(description="考核成绩")
    score: Optional[float] = Field(description="考核成绩")

# ------------------------------
# 7. get每个序次分数成绩模型(响应体)
# ------------------------------
class ScoreAm(BaseModel):
    exam_order: Optional[int] = Field(description="考核序次")
    class_name: str = Field(description="班级名称")
    score:Optional[float] = Field(description="分数avg,max,min")


class ScoreStatType(str, Enum):
    AVG = "avg"
    MAX = "max"
    MIN = "min"

#请求体
class Score_state(BaseModel):
    state:ScoreStatType

# ------------------------------
# 8.#返回前三的学生成绩(成绩ID,学号，姓名，考核序次，成绩)(响应体)
# ------------------------------
class SelectScore1(SelectScore):
    rk: Optional[int] = Field(description="排名")