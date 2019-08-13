"""
视图和路由文件
"""
import hashlib
from flask import session
# from app import session
from flask import jsonify
from flask import request
from flask import redirect
from flask import make_response
from flask import render_template


from . import main
from app import csrf
# from app import cache
from app.models import *
from .forms import TeacherForm


def SetPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    return md5.hexdigest()

def loginValid(fun):
    def inner(*args,**kwargs):
        cookie_username = request.cookies.get("username")
        id = request.cookies.get("user_id")
        session_username = session.get("username")
        if cookie_username and id and session_username:
            if cookie_username == session_username:
                return fun(*args,**kwargs)
        return redirect("/login/")
    return inner



@main.route("/register/",methods=["GET","POST"])
def register():
    if request.method == 'POST':
        form_data = request.form
        username = form_data.get("username")
        password = form_data.get("password")
        identity = form_data.get("identity")

        user = User()
        user.username = username
        user.password = SetPassword(password)
        user.identity = int(identity)
        user.save()

        return redirect('/login/')
    return render_template("register.html")


@main.route("/login/",methods=["GET","POST"])
def login():
    if request.method == "POST":
        form_data = request.form
        username = form_data.get("username")
        password = form_data.get("password")

        # 获取用户信息
        user = User.query.filter_by(username=username).first()
        # 检查用户身份：老师1，学生0
        identity = user.identity
        # 检查身份资料是否完善
        identity_id = user.identity_id

        if user:
            db_password = user.password
            md5_password = SetPassword(password)
            if md5_password == db_password:
                # 验证成功，跳转首页
                response = redirect('/index/')
                # 设置cookie
                response.set_cookie("username",username)
                response.set_cookie("user_id",str(user.id))

                # 使用cookie来判断用户身份
                response.set_cookie("identity",str(identity))
                # 使用cookie来判断用户是否完善可个人信息
                if identity_id:
                    response.set_cookie("identity_id",str(identity_id))
                else:
                    response.set_cookie("identity_id","")

                # 设置session
                session["username"] = username
                # 返回跳转页面
                return response
    return render_template("login.html")


@main.route("/index/",methods=["GET","POST"])
@loginValid
# @cache.cached(timeout=20)
def index():
    # print(session.get('username'))
    # 查讯所有课程
    course_list = Course.query.all()
    # 通过cookie获取identity_id和identity
    identity_id = request.cookies.get("identity_id")
    identity = request.cookies.get("identity")
    if identity_id:
        if identity == '1':
            teacher = Teacher.query.get(int(identity_id))
        else:
            student = Student.query.get(int(identity_id))
    else:
        if identity == '1':
            teacher = {}
        else:
            student = {}

    # 身份信息添加
    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        gender = request.form.get("gender")
        course = request.form.get("course")
        # 判断用户身份
        if request.cookies.get("identity") == "0":
            student = Student()
            student.name = name
            student.age = age
            student.gender = gender
            student.save()
            # 更新用户和学生的关联
            user = User.query.get(int(request.cookies.get("user_id")))
            user.identity_id = student.id
            user.save()
            # 将用户的详情信息的状态改掉
            response = make_response(render_template("index.html", **locals()))
            response.set_cookie("identity_id", str(student.id))
            return response
        else:
            teacher = Teacher()
            teacher.name = name
            teacher.age = age
            teacher.gender = gender
            teacher.course_id = int(course)
            teacher.save()
            # 更新用户和教师的关联
            user = User.query.get(int(request.cookies.get("user_id")))
            user.identity_id = teacher.id
            user.save()
            # 将用户的详情信息的状态改掉
            response = make_response(render_template("index.html",**locals()))
            response.set_cookie("identity_id",str(teacher.id))
            return response

    return render_template("index.html",**locals())


@main.route("/logout/",methods=["GET","POST"])
def logout():
    response = redirect('/login/')
    for key in request.cookies:
        response.delete_cookie(key)
    del session["username"]
    return response

# @csrf.exempt # 临时关闭csrf校验
@main.route("/add_teacher/",methods=["GET","POST"])
def add_teacher():
    teacher_form = TeacherForm()
    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        gender = request.form.get("gender")
        course = request.form.get("course")

        teacher = Teacher()
        teacher.name = name
        teacher.age = age
        teacher.gender = gender
        teacher.course_id = course
        teacher.save()
    return render_template("add_teacher.html",**locals())

# csrf 如果没有配置跳转的错误页面
@csrf.error_handler
# @main.errorhandler
@main.route("/csrf_403/")
def csrf_tonken_error(reason):
    return render_template("csrf_403.html")

# ajax 前端校验
@main.route("/userValid/",methods=["GET","POST"])
def userValid():
    # 定义json字典数据格式
    result = {
        "code":"",
        "data":""
    }
    if request.method == "POST":
        username = request.form.get("username")
        if username:
            user = User.query.filter_by(username=username).first()
            if user:
                result["code"] = 400
                result["data"] = "用户名已存在"
            else:
                result["code"] = 200
                result["data"] = "用户名未被注册，可以使用"
    return jsonify(result)

@main.route("/student_list/")
def student_list():
    students = Student.query.all()
    return render_template("student_lists.html",**locals())


# @main.route("/clearCache/")
# def clearCache():
#     cache.clear()
#     return "cache is clear"
