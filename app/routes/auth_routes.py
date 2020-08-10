"""Application routes."""
from datetime import datetime as dt
from flask import request, jsonify
from .. import api, name_space1
from flask_restx import Resource, fields
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
import datetime
import requests
import json
from collections import namedtuple
import jsons

# from ..models.models import TestClass, ResponseObj, RequestObj, OrdinationObj

auth_model = api.model('AuthModel', {
    'username': fields.String(readOnly=True, description='Username'),
    'password': fields.String(required=True, description='Password')
})


@name_space1.route('/token')
class AuthClass(Resource):
    @name_space1.expect(auth_model)
    def post(self):
        data = request.form
        username = data['username']
        password = data['password']

        if not username:
            return {"msg": "Missing username parameter"}, 400
        if not password:
            return {"msg": "Missing password parameter"}, 400

        if username != 'test' or password != 'test':
            return {"msg": "Bad username or password"}, 401

        # Identity can be any data that is json serializable
        expires = datetime.timedelta(minutes=8)
        access_token = create_access_token(identity=username, expires_delta=expires)
        return {"access_token": access_token}, 200
