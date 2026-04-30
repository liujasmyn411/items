

from sqlalchemy import and_, func, or_, desc

from database import SessionLocal
from model import Score, Student, ClassInfo

db=SessionLocal()

# ------------------------------
#返回全部学生成绩(成绩ID,学号，姓名，考核序次，成绩)
# ------------------------------
def return_scores(db):
    result = db.query( Score.id
                      ,Score.student_no
                      ,Student.student_name
                      ,Score.exam_order
                      ,Score.score).select_from(Student).join(Score).where(Score.is_deleted==0).all()
    return result

# ------------------------------
#根据id返回单个学生成绩(成绩ID,学号，姓名，考核序次，成绩)
# ------------------------------
def return_first_score(sid,db):
    result = db.query( Score.id
                      ,Score.student_no
                      ,Student.student_name
                      ,Score.exam_order
                      ,Score.score).select_from(Student).join(Score).where(
                        and_(Score.is_deleted==0,Score.id==sid)).all()
    return result


# ------------------------------
#根据学号返回单个学生成绩(成绩ID,学号，姓名，考核序次，成绩)
# ------------------------------
def return_student_no_score(sno,db):
    result = db.query( Score.id
                      ,Score.student_no
                      ,Student.student_name
                      ,Score.exam_order
                      ,Score.score).select_from(Student).join(Score).where(
                        and_(Score.is_deleted==0,Student.student_no==sno)).all()
    return result



# ------------------------------
#添加单(多)个学生的成绩信息(学号，考核序次，成绩)
# ------------------------------
def add_scores(scores,db):

    try:
        for i in scores:
            dbScore=Score(student_no=i.student_no,exam_order=i.exam_order,score=i.score)
            result_again=(db.query(Score.student_no
                     ,Score.exam_order)
                          .where(and_(Score.student_no==dbScore.student_no
                     ,Score.exam_order==dbScore.exam_order,Score.is_deleted==0)).first())
            if result_again:
                return {
                    "code": 400,
                    "msg": f"学生{dbScore.student_no}该次{dbScore.exam_order}考核成绩已存在，不可重复添加"
                }
            db.add(dbScore)
        db.commit()
    except Exception as e:
        db.rollback()
        raise Exception(f"数据库保存失败：{str(e)}")

    return scores


    # db.add(new_score)
    # db.commit()
    # return scores

# ------------------------------
#修改单个学生的成绩信息(根据成绩ID)
# ------------------------------
def patch_score(score,db):
    new_score = Score(id=score.id,score=score.score)
    result = db.query(Score).where(and_(Score.id==new_score.id
                                   ,Score.is_deleted==0)).first()
    print(result)
    if result:
        result.score = score.score
        db.commit()
    else:
        return "error"



# ------------------------------
#删除单个学生的成绩信息(逻辑)(根据成绩ID)
# ------------------------------
def delete_score(score,db):
    new_score = Score(id=score.id)
    result = db.query(Score).where(and_(Score.id==new_score.id
                                   ,Score.is_deleted==0)).first()
    print(result)
    if result :
        result.is_deleted = 1
        db.commit()
    else:
        return "error"

# ------------------------------
#查询每次考试成绩都在80分以上的学生
# ------------------------------
def select_eighty_score(db):

    result1=db.query(Score.student_no).where(Score.score<=80).group_by(Score.student_no).subquery()
    result2 = (db.query(
        Score.student_no
        ,Student.student_name
        ,Score.score
    ).select_from(Student)
              .join(Score)
              .where(and_(Score.is_deleted == 0,Score.student_no.not_in(result1))).all()
              )
    # not in 要传整个子查询，not_in() 需要的是：一个 “结果集合”
    print(result2)
    return result2

# ------------------------------
#返回不同考核序次班级的平均分(考核序次，成绩)
# ------------------------------
def return_avg_score(state,db):
    sfunc=None
    if state == "avg":
        sfunc = func.avg(Score.score).label("score")

    elif state == "max":
        sfunc = func.max(Score.score).label("score")

    elif state == "min":
        sfunc = func.min(Score.score).label("score")

    result = (db.query(
                      Score.exam_order
                       ,ClassInfo.class_name
                       ,sfunc
                       ).select_from(ClassInfo)
                        .join(Student).join(Score).where(and_(Score.is_deleted==0))
                        .group_by(Score.exam_order,ClassInfo.class_name)
                        .order_by(Score.exam_order, desc(sfunc)).all())
    return result


# ------------------------------
#返回前三的学生成绩(学号，姓名，考核序次，成绩)
# ------------------------------
def return_thirdscores(db):

    result = db.query( Score.id
                      ,Score.student_no
                      ,Student.student_name
                      ,Score.exam_order
                      ,Score.score
                       ,func.row_number().over(
                        partition_by=Score.exam_order,
                        order_by=desc(Score.score)
                        ).label("rk")
                       ).select_from(Student).join(Score).where(and_(Score.is_deleted==0)).subquery()
    # print(result)
#subquery() = 把一段查询变成一张 “临时表”
#.c 是 column（列） 的缩写！
    result1=db.query(result).where(or_(result.c.rk==1,result.c.rk==2,result.c.rk==3)).all()

    return result1

