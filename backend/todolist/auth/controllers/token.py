import jwt
import datetime
import os

from flask import jsonify
from flask_restful import Resource
from flask_login import login_required, current_user

class IssueToken(Resource):
    """ Return a token that grants access tothe API """
    method_decorators = [login_required]
    def get(self):
        jwt_payload = {
            "uid": str(current_user.id),
            "eml": current_user.email,
            "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        }

        token = jwt.encode(jwt_payload, os.environ["SECRET_KEY"]).decode("utf-8")

        return jsonify({
            "id": current_user.id,
            "token": token
        })
        
        