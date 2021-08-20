from flask_restful import Resource
from flask import request
from fn.keywords import INVALID_TOKEN, INVALID_ACTION, NOT_ENOUGH_ARGUMENT, DATABASE_ERROR
from fn.common import getFromRequest
from fn.req import ok, er, ng
from fn.auth import verifyToken, getToken
from models.user import User

class Auth(Resource):
    def post(self):
        self.username = getFromRequest(request, 'username')
        type = getFromRequest(request, 'type')
        if not type or not self.username:
            return er(NOT_ENOUGH_ARGUMENT)
        match = {
            'check': self.check,
            'auth': self.auth
        }
        if not type in match.keys():
            return er(INVALID_ACTION)
        return match[type]() #type:ignore
    
    def check(self):
        token = getFromRequest(request, 'token')
        c = verifyToken(token, self.username)
        if c is True:
            return ok()
        elif c is None:
            return ng('Expired token.')
        else:
            return er(INVALID_TOKEN)
        
    def auth(self):
        username = getFromRequest(request, 'username')
        password = getFromRequest(request, 'password')
        if not username or not password:
            return er(NOT_ENOUGH_ARGUMENT)
        user = User(username, password)
        try:
            if not user.exists():
                return ng('User not exists.')
            if user.checkPassword():
                group = user.get()['group']
                return ok(getToken(username, group))
            else:
                return ng('Not verified.')
        except Exception as e:
            return er(DATABASE_ERROR, str(e))
    