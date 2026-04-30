# """
# 鉴权中间件 - JWT Token 验证
# """
# from fastapi import Request, HTTPException
# from fastapi.responses import JSONResponse
# from starlette.middleware.base import BaseHTTPMiddleware
# import jwt
#
# # JWT 配置
# SECRET_KEY = "wolin_secret_key_2026"
# ALGORITHM = "HS256"
#
# # 白名单：不需要登录就能访问的路径
# EXCLUDE_PATHS = [
#     "/",  # 根路径
#     "/docs",  # Swagger 文档
#     "/redoc",  # ReDoc 文档
#     "/openapi.json",  # OpenAPI 规范
#     "/api/users/login",  # 登录接口
#     "/api/users/register",  # 注册接口
#     "/static",  # 静态资源
# ]
#
# # 需要鉴权的 HTTP 方法（增删改查）
# AUTH_METHODS = ["POST", "PUT", "DELETE", "PATCH"]
#
#
# class AuthMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         path = request.url.path
#
#         # 1. 白名单直接放行
#         for exclude_path in EXCLUDE_PATHS:
#             if path.startswith(exclude_path):
#                 return await call_next(request)
#
#         # 2. 只对增删改查操作进行鉴权（GET 查询可以放行）
#         if request.method not in AUTH_METHODS:
#             return await call_next(request)
#
#         # 3. 获取 Token
#         auth_header = request.headers.get("Authorization")
#         if not auth_header:
#             return JSONResponse(
#                 status_code=401,
#                 content={"code": 401, "message": "未登录，请先登录"}
#             )
#
#         if not auth_header.startswith("Bearer"):
#             return JSONResponse(
#                 status_code=401,
#                 content={"code": 401, "message": "Token 格式错误"}
#             )
#
#         token = auth_header.split(" ")[1]
#
#         # 4. 验证 Token
#         try:
#             payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#             # 将用户信息挂载到 request.state，全局可用
#             request.state.user = payload
#         except jwt.ExpiredSignatureError:
#             return JSONResponse(
#                 status_code=401,
#                 content={"code": 401, "message": "Token 已过期"}
#             )
#         except jwt.InvalidTokenError:
#             return JSONResponse(
#                 status_code=401,
#                 content={"code": 401, "message": "Token 无效"}
#             )
#
#         # 5. 放行
#         return await call_next(request)
#
#
# def create_token(data: dict) -> str:
#     """生成 JWT Token"""
#     import time
#     payload = {
#         **data,
#         "exp": int(time.time()) + 86400  # 24小时过期
#     }
#     return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
