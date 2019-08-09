from app.ApiResource import api
from flask_restful import Resource
from app.models import *

result = {
    "version": "v1.0",
    "code": "",
    "data": []
}

@api.resource('/user/')
class UserInfo(Resource):
    def get(self):
        values = User.query.all()
        result["code"] = 200
        for value in values:
            result["data"].append(
                {
                    value.username:{
                        "username":value.username,
                        "password":value.password,
                        "identity":value.identity,
                        "is_active":True
                    }
                }
            )
        result["count"] = len(values)
        return result