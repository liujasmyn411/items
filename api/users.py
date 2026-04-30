import os
from fastapi import APIRouter, Depends, Path, Header, Form, UploadFile, File, HTTPException
from pydantic import Field
from sqlalchemy import and_
from sqlalchemy.orm import Session

# 导入dao层
from dao.users import register_users, get_users, get_user, update_user, get_login_users, delete_user, get_user_pages, \
    get_top5

from model import User

# 导入数据库连接依赖
from database import get_db

# 导入注册请求体
from scheme.users_request import UserRegister, Update, EnumRole

# Token 生成
# from middleware.auth import create_token

# 创建用户模块路由，接口文档标签为：用户模块
users_dao_router = APIRouter(tags=["刘帅-用户模块"])


# -------------------
# if not os.path.exists("static/avatars"):
#     os.mkdir("static/avatars");

# 1. 用户登录接口
@users_dao_router.post("/api/users/login", summary="用户登录接口")
def login_user(db: Session = Depends(get_db),  # 依赖注入：获取数据库连接
               username: str = Form(...),  # 从表单接收用户名（必填）
               password: str = Form(...)  # 从表单接收密码（必填）
               ):
    user = db.query(User).filter(and_(User.username == username, User.is_deleted == 0)).first()
    # 用户不存在
    if not user:
        raise HTTPException(status_code=404, detail="该用户不存在")

        # return False, "该用户不存在"
    try:
        # 调用dao层
        state, message = get_login_users(db, username, password)

        if state:
            # 登录成功
            return {"code": 200, "message": "登录成功"}
        else:
            # 账号或密码错误
            return {"code": 400, "message": "账号或密码错误"}
    except Exception as e:
        # 捕获异常,e为报错信息本身,str(e) 就能拿到文字版错误信息
        raise HTTPException(status_code=400, detail=f"报错信息为{str(e)}")
    finally:
        # 无论成功失败，最终都关闭数据库连接
        db.close()


# 2. 用户注册接口
@users_dao_router.post("/api/users/register", summary="用户注册接口")
def register(username: str = Form(...),
             password: str = Form(...),
             phone: int = Form(None),
             role: EnumRole = Form(...),
             avatar: UploadFile | None = File(None),
             ref_id: int = Form(...),
             db=Depends(get_db)
             ):
    useregister = UserRegister(
        username=username,
        password=password,
        phone=phone,
        role=role,
        ref_id=ref_id
    )

    try:
        # 调用dao层
        status, avatarpaths = register_users(
            useregister,
            avatar,
            db)
        print(status)
        if status == True:
            # 注册成功 注册接口响应模型
            return {
                "code": 200,
                "message": "注册成功"
            }

        else:
            # 注册失败
            return {
                "code": 400,
                "message": "注册失败"
            }

    except Exception as e:
        # 捕获异常,e为报错信息本身,str(e) 就能拿到文字版错误信息
        return {
            "code": 400,
            "message": f"注册失败:{str(e)}"
        }
    finally:
        # 无论成功失败，最终都关闭数据库连接
        db.close()


# 3.查询所有用户接口（登录就能看）
@users_dao_router.get("/api/users/all", summary="查询所有用户信息")
def get_all_users(db=Depends(get_db)):
    all_users = get_users(db)
    db.close()
    return {"code": 200,
            "message": "查询成功",
            "data": all_users
            }


# 4.2页面查询用户接口
@users_dao_router.get("/api/userspages/pages", summary="分页用户信息")
def get_pages(db=Depends(get_db), page: int = 1, page_size: int = 10):
    return get_user_pages(db, page, page_size)


# 4.1按照角色查询用户接口（登录就能看）
@users_dao_router.post("/api/users/roles", summary="按照角色查询用户信息")
def get_role_roles(role: EnumRole = Form(...), db=Depends(get_db)):
    role_users = get_user(db, role)
    db.close()
    return {"code": 200,
            "message": "查询成功",
            "data": role_users
            }


# 5.修改用户接口
@users_dao_router.patch("/api/users/update", summary="修改用户信息接口")
def updateuser(old_username: str = Form(..., min_length=3, description="必传"),
               new_username: str = Form(..., min_length=3, description="必传"),
               password=Form(None),
               phone=Form(None),
               avatar: UploadFile | None = File(None),
               db: Session = Depends(get_db)):
    update = Update(
        old_username=old_username,
        new_username=new_username,
        password=password,
        phone=phone,
    )

    state, message = update_user(db,
                                 update,
                                 avatar
                                 )
    if state:
        # 修改成功，查询最新用户信息并返回
        user = (db.query(User)
                .filter(and_(User.username == update.new_username, User.is_deleted == 0))
                .first())
        return {
            "code": 200,
            "message": "修改成功",
            "data": user
        }
    else:
        # 修改失败
        return {
            "code": 400,
            "message": "修改失败"
        }



# 6 逻辑删除用户功能（只有manager能删）
@users_dao_router.delete("/api/users/delete/{username}", summary="逻辑删除用户接口")
def deleteuser(username: str, db=Depends(get_db)):
    result = delete_user(db, username, )
    try:
        if result:
            return {
                "code": 200,
                "message": "逻辑删除成功"
            }
        else:
            return {
                "code": 400,
                "message": "该用户已被删除"
            }
    except Exception as e:
        return {
            "code": 400,
            "message": f"逻辑删除失败:{str(e)}"
        }
    finally:
        # 关闭数据库连接
        db.close()


# 7 统计就业薪资最高的前五名学生的姓名，班级id和就业时间，就业公司
@users_dao_router.get("/api/topusers", summary="统计就业薪资最高的前五名学生的姓名，班级和就业时间，就业公司")
def top5(db=Depends(get_db)):
    result = get_top5(db)
    return result
