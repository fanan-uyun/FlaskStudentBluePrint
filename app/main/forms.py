import wtforms # 定义字段
from flask_wtf import FlaskForm # 定义表单
from wtforms import validators # 定义校验

# forms当中禁止查看数据库，数据库查询被认为视图功能
course_list = []

class TeacherForm(FlaskForm):
    """
    form字段的参数
    label=None, 表单的标签
    validators=None, 校验，传入校验的方法
    filters=tuple(), 过滤
    description='',  描述
    id=None, html id
    default=None, 默认值
    widget=None, 样式
    render_kw=None, 属性 参数
    """

    name = wtforms.StringField(
        label="教师姓名",
        validators=[
            validators.DataRequired('姓名不可以为空')
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "教师姓名"
        }
    )
    age = wtforms.IntegerField(
        label="教师年龄",
        validators=[
            validators.DataRequired("年龄不可以为空"),
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "教师年龄",
        }
    )
    gender = wtforms.SelectField(
        label="教师性别",
        choices=[
            ("1","男"),
            ("2","女")
        ],
        render_kw={
            "class": "form-control",
        }
    )
    course = wtforms.SelectField(
        label="学科",
        choices=course_list,
        render_kw={
            "class": "form-control",
        }
    )
    submit = wtforms.SubmitField(
        label="提交",
        render_kw={
            "class": "btn btn-primary btn-block",
        },
    )