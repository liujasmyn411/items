"""
Model 模块统一导出
- 共用模型: Teacher, Student, ClassInfo
- 独有模型: Score, Employment, User
"""
from model.base_models import Teacher, Student, ClassInfo
from model.score_models import Score
from model.employment_models import Employment
from model.user_models import User

__all__ = [
    'Teacher',
    'Student',
    'ClassInfo',
    'Score',
    'Employment',
    'User',
]
