from typing import List

from fastapi import APIRouter, Depends, Path, Query, HTTPException
import database
from scheme.score_scheme import ScoreCreate,SelectScore,ScoreUpdate,ScoreDelete,Score_state,ScoreAm,SelectScore1,ScoreEighty
from dao.score_dao import return_scores,return_first_score,return_student_no_score,add_scores,patch_score,delete_score,return_avg_score,return_thirdscores,select_eighty_score



score_router = APIRouter(
    prefix="/score",  # 必须以 / 开头
    tags=["钱铠-成绩管理"]  # 搭配文档分组，推荐一起用
)

# ------------------------------
#1.分页查询学生成绩(成绩ID,学号，姓名，考核序次，成绩)
# ------------------------------
@score_router.get("/get_scs/{page}/{limit}",response_model=list[SelectScore],summary="分页查询学生成绩")
def get_scs(page:int=Path(...,ge=1),limit:int=Path(...,ge=1),db = Depends(database.get_db)):
    # 创建会话窗口对象
    result =return_scores(db)
    end=page*limit
    page=page-1
    start=page*limit
    return result[start:end]


# ------------------------------
#2.根据id查询返回单个学生成绩(成绩ID,学号，姓名，考核序次，成绩)
# ------------------------------
@score_router.get("/get_first_sc/{score_id}",response_model=list[SelectScore],summary="返回单个学生成绩信息")
def get_first_sc(score_id:int=Path(...,ge=1),db = Depends(database.get_db)):
    # 创建会话窗口对象
    result =return_first_score(score_id,db)
    return result

#2.根据学号查询返回单个学生成绩(成绩ID,学号，姓名，考核序次，成绩)
# ------------------------------
@score_router.get("/get_student_no_sc/{student_no}",response_model=list[SelectScore],summary="返回单个学生成绩信息")
def get_student_no_sc(student_no:str=Path(...),db = Depends(database.get_db)):
    # 创建会话窗口对象
    result =return_student_no_score(student_no,db)
    return result
# ------------------------------
#3.添加单(多)个学生的成绩信息(学号，考核序次，成绩)
#Union允许一个变量 / 参数 是 多种类型中的任意一种
# ------------------------------
@score_router.post("/post_sc",summary="添加单(多)个学生的成绩信息")
def post_sc(scorescrate:List[ScoreCreate],db = Depends(database.get_db)):
    print(scorescrate)
    # 创建会话窗口对象
    try:
        result = add_scores(scorescrate, db)
    except Exception as e:
        return {
        "code": 500,
        "msg": f"操作失败：{str(e)}"
        }
    return {"data":result}


    # if result=="studentNO_error":
    #     raise HTTPException(status_code=400,detail="学生学号不存在，无法添加成绩！")
    # elif result=="error":
    #     raise HTTPException(status_code=400, detail="该学生该次成绩已存在！")



# ------------------------------
#4.修改单个学生的成绩信息,根据(成绩ID，考核序次)
# ------------------------------
@score_router.patch("/patch_sc",summary="修改单个学生的成绩")
def patch_sc(scoreupdate:ScoreUpdate,db = Depends(database.get_db)):
    # 创建会话窗口对象
    result =patch_score(scoreupdate,db)
    if result=="error":
        raise HTTPException(status_code=409, detail="找不到该学生的成绩序次！")
    return {"message":"修改成功"}

# ------------------------------
#5.删除单个学生的成绩信息(逻辑)(根据成绩ID)
# ------------------------------
@score_router.delete("/delete_sc",summary="删除单个学生的成绩")
def delete_sc(scoredelete:ScoreDelete,db = Depends(database.get_db)):
    # 创建会话窗口对象
    result =delete_score(scoredelete,db)
    if result=="error":
        raise HTTPException(status_code=409, detail="找不到该学生的成绩序次！")
    return {"message":"删除成功"}

# ------------------------------
#6.查询每次考试成绩都在80分以上的学生,返回(编号，姓名，成绩)
# ------------------------------
@score_router.get("/get_eighty",response_model=list[ScoreEighty],summary="查询每次考试成绩都在80分以上的学生")
def get_eighty(db = Depends(database.get_db)):
    result =select_eighty_score(db)
    return result


# ------------------------------
#7.不同考核序次班级的分数avg,max,min,返回(考核序次，班级,成绩)
# ------------------------------
@score_router.get("/get_avg_sc",response_model=list[ScoreAm],summary="返回不同考核序次班级的的分数avg,max,min")
def get_avg_sc(state: Score_state=Query(...),db = Depends(database.get_db)):
    result =return_avg_score(state.state.value,db)
    return result


# ------------------------------
#8.返回前三的学生成绩(成绩ID,学号，姓名，考核序次，成绩)
# ------------------------------
@score_router.get("/get_third_scs",response_model=list[SelectScore1],summary="返回前三的学生成绩")
def get_third_scs(db = Depends(database.get_db)):
    # 创建会话窗口对象
    result =return_thirdscores(db)
    return result



