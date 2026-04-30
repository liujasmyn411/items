# 启动fastapi的代码写在这里
import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from api import score_api, stu_api, class_api, teacher_api
from api.employment_api import employment_router
from api.student_api import student_router
# 子路由
from api.users import users_dao_router
# 鉴权中间件
# from middleware.auth import AuthMiddleware

app = FastAPI(title="学生管理系统")

# 注册鉴权中间件
# app.add_middleware(AuthMiddleware)

@app.get("/")
def first_menu():
    return {"message": "欢迎来到学生管理系统"}


app.mount("/static", StaticFiles(directory="static"), name="static")

# 刘帅子路由
app.include_router(users_dao_router)
# 钱铠子路由
app.include_router(score_api.score_router)
# 者俊子路由
app.include_router(stu_api.stu_router, prefix='/stus')
# 习老师子路由
app.include_router(employment_router)
# 杨征昊子路由
app.include_router(student_router)
# 王总子路由
app.include_router(class_api.router)
# 黄家胤子路由
app.include_router(teacher_api.router)

if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8080)
