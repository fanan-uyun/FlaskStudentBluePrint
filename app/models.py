from app import db

# 创建数据库回话，基于会话进行增删改查
# 由于此处session与flask session设置冲突，改为sess

class BaseModel(db.Model):
    __abstract__ = True # 抽象表为True，代表当前类为抽象类，不会被创建
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)

    # 数据保存方法
    def save(self):
        sess = db.session()
        sess.add(self)
        sess.commit()

     # 数据删除方法
    def delete_data(self):
        sess = db.session()
        sess.delete(self)
        sess.commit()

class User(BaseModel):
    """
    用户表
    """
    __tablename__ = "user"
    username = db.Column(db.String(32))
    password = db.Column(db.String(32))
    identity = db.Column(db.Integer) # 1老师 0学生
    identity_id = db.Column(db.Integer,nullable=True)

class Student(BaseModel):
    """
    学生表
    """
    __tablename__ = "student"
    name = db.Column(db.String(32))
    age = db.Column(db.Integer)
    gender = db.Column(db.Integer) # 1 男 2 女
    to_attend = db.relationship(
        "Attend",
        backref = "to_student"
    )

# 学生课程关联表(多对多)，也可以使用上面的方式创建该表
Student_Course = db.Table(
    "student_course",
    db.Column("id",db.Integer,primary_key=True,autoincrement=True),
    db.Column("student_id",db.Integer,db.ForeignKey("student.id")),
    db.Column("course_id",db.Integer,db.ForeignKey("course.id")),
    db.Column("delete_flag",db.Integer,default=1)  # 1没有停课 0停课

)

class Course(BaseModel):
    """
    课程表
    """
    __tablename__ = "course"
    name = db.Column(db.String(32))
    description = db.Column(db.Text)
    to_teacher = db.relationship(
        'Teacher', # 映射模型
        backref = 'to_course', # 反向映射字段，反向映射表通过该字段查询当前表
    ) # 映射表字段

    to_student = db.relationship(
        "Student",# 映射模型
        secondary = Student_Course, # 第二映射的模型
        backref = db.backref("to_course",lazy="dynamic"),
        lazy = "dynamic"
            # select 访问该字段时，加载所有的映射数据
            # joined 对关联的两个表student和student_course进行join查询
            # dynamic 访问该字段时，不加载数据
    )

class Grade(BaseModel):
    """
    成绩表
    学生、课程关联此表
    """
    __tablename__ = "grade"
    grade = db.Column(db.Float,default=0)
    student_id = db.Column(db.Integer,db.ForeignKey("student.id"))
    course_id = db.Column(db.Integer,db.ForeignKey("course.id"))

class Attend(BaseModel):
    """
    考勤表：记录学生出勤状况
    学生考勤：一对多
    """
    __tablename__ = "attend"
    att_time = db.Column(db.Date)
    status = db.Column(db.Integer,default=1) # 0 请假 ；1 正常出勤 ；2 迟到 ；3 早退 ；4 旷课
    student_id = db.Column(db.Integer,db.ForeignKey("student.id"))

class Teacher(BaseModel):
    """
    老师表
    老师与课程是多对一
    """
    __tablename__ = "teacher"
    name = db.Column(db.String(32))
    age = db.Column(db.Integer)
    gender = db.Column(db.Integer)
    course_id = db.Column(db.Integer,db.ForeignKey("course.id"))