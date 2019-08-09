from app import create_app,db
from flask_script import Manager
from flask_migrate import Migrate # 用来同步数据库
from flask_migrate import MigrateCommand # 用来同步数据库的命令

# 实例化app
app = create_app("running")

# 命令行封装app
manager = Manager(app)

# 绑定可以管理的数据库模型
migrate = Migrate(app,db)

# 加载数据库管理命令
manager.add_command("db",MigrateCommand)

if __name__ == "__main__":
    manager.run()