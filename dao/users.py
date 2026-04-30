# 导入加密模块
import hashlib
from fastapi import HTTPException, UploadFile, File
from sqlalchemy import and_, null
from sqlalchemy.orm import Session
# 导入Base模块
from model import User, Employment, ClassInfo, Student
from scheme.users_request import EnumRole


# from scheme.users_request import UserRegister, Update


# -------------------

# 1.用户登录查询
def get_login_users(db: Session, username: str, password: str):
    # 查询：用户名匹配 + 未被逻辑删除的用户
    user = db.query(User).filter(and_(User.username == username, User.is_deleted == 0)).first()
    # 用户不存在
    if not user:
        return False, "该用户不存在"
    # 用户如果存在，验证密码是否相等
    md5_password = hashlib.md5(password.encode("utf-8")).hexdigest()
    if md5_password == user.password:
        return True, "密码正确"
    else:
        return False, "密码输入错误"


# 2.用户注册功能
def register_users(useregister, avatar, db):
    # 查询数据库中是否已存在相同用户
    user = db.query(User).filter(
        and_(User.ref_id == useregister.ref_id, User.role == useregister.role, User.is_deleted == 0)).first()
    # 用户已存在，无法注册
    if user:
        raise HTTPException(status_code=409, detail="该用户名已被注册")

    # 用户名不存在，进行注册
    # 异常判断创建 avatars 目录会报错
    try:
        avatar_filename = avatar.filename
        avatarpaths = f"static/avatars/{avatar_filename}"

        with open(avatarpaths, "wb") as f:
            # 将读取到的文件二进制数据写入本地，完成文件保存
            f.write(avatar.file.read())

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"头像上传失败：{str(e)}")

    try:
        # 密码加密存储
        md5_1password = hashlib.md5(useregister.password.encode("utf-8")).hexdigest()
        # 创建新用户
        new_user = User(
            username=useregister.username,
            password=md5_1password,
            avatar=avatarpaths,
            is_deleted=0,  # 0=未删除，1=已删除
            phone=useregister.phone,
            role=useregister.role,
            ref_id=useregister.ref_id
        )
        # 添加到数据库会话
        db.add(new_user)
        db.commit()
        # 返回成功结果和头像路径

        result = [True, avatarpaths]
        return result

    # 捕获异常
    except Exception as e:
        # 出错回滚，保证数据安全

        db.rollback()
        # 返回错误信息
        result = [False, f"注册失败：{str(e)}"]
        return result


# 3.查询所有用户功能
def get_users(db: Session):
    # 查询未删除的所有用户，只查需要的字段
    all_users = (db.query(User.username.label("username"), User.avatar.label("avatar"), User.role.label("role"))
                 .filter(User.is_deleted == 0)
                 .all())

    return [{
        "username": i.username,
        "avatar": i.avatar,
        "role": i.role}
        for i in all_users]


# 4.1按照角色查询用户功能
def get_user(db, role):
    role_user = (db.query(User.username.label("username"), User.avatar.label("avatar"), User.role.label("role"))
                 .filter(and_(User.role == role, User.is_deleted == 0))
                 .all())
    if not role_user:
        return {
            "code": 404,
            "message": "该角色不存在",
            "data": null}

    return [{
        "username": i.username,
        "avatar": i.avatar,
        "role": i.role}
        for i in role_user]


# 4.2分页查询用户功能
def get_user_pages(db: Session, page: int, page_size: int):
    if page <= 0 or page_size <= 0:
        raise HTTPException(status_code=400, detail="页面输入错误，不能小于0")
    skip = (page - 1) * page_size
    return db.query(User).where(User.is_deleted == 0).offset(skip).limit(page_size).all()


# 5 修改用户功能
# 支持：用户名、密码、手机号、头像修改
def update_user(db: Session, update, avatar):
    # 根据用户名查询用户是否存在
    user = (db.query(User)
            .filter(and_(User.username == update.old_username, User.is_deleted == 0))
            .first())

    # 用户不存在
    if not user:
        return False, "用户不存在"

    try:
        # 存在则开始修改
        user.username = update.new_username

        # 选择密码、手机号、头像进行修改，不修改不覆盖
        if update.password:
            md5_password = hashlib.md5(update.password.encode("utf-8")).hexdigest()
            user.password = md5_password
        if update.phone:
            user.phone = update.phone
        if avatar:
            try:
                avatar_filename = avatar.filename
                avatarpaths = f"static/avatars/{avatar_filename}"

                with open(avatarpaths, "wb") as f:
                    # 将读取到的文件二进制数据写入本地，完成文件保存
                    f.write(avatar.file.read())
                user.avatar = avatarpaths
            except Exception as e:
                return False, f"用户不存在{str(e)}"

        # 提交修改
        db.commit()
        # 刷新对象，同步数据库最新数据
        db.refresh(user)
        return True, "修改成功"

    except Exception as e:
        # 回滚 刚才的数据库操作
        db.rollback()
        return False, f"修改失败：{str(e)}"


# 6 逻辑删除用户功能
def delete_user(db: Session, username: str):
    # 查询要删除的用户（未删除状态）
    user = db.query(User).filter(and_(User.username == username, User.is_deleted == 0)).first()
    if not user:
        return False
    try:
        user.is_deleted = 1
        db.commit()
        db.refresh(user)
        return True
    except Exception as e:
        db.rollback()
        return False


# 7 统计就业薪资最高的前五名学生的姓名，班级和就业时间，就业公司
def get_top5(db: Session):
    top = (
        db.query(
            Student.student_name,
            Student.class_id,
            Employment.company_name,
            Employment.salary,
            Employment.offer_send_time
        )
        .select_from(Student)  # 放最前面！
        .join(Employment, Student.student_no == Employment.student_no)  # 明确写关联！
        .filter(Student.is_deleted == 0)
        .order_by(Employment.salary.desc())
        .limit(5)
        .all()
    )
    result = []

    for i in top:
        result.append({
            "student_name": i.student_name,
            "class_id": i.class_id,
            "company_name": i.company_name,
            "salary": i.salary,
            "offer_send_time": i.offer_send_time
        })

    return result
