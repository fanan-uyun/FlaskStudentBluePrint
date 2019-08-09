from flask import Blueprint  # 导入flask蓝图

# 创建蓝图
main = Blueprint("main",__name__)

# 加载视图路由
from . import views