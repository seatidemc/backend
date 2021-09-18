from flask_restful import Resource
from flask import request
from fn.keywords import INVALID_TOKEN, INVALID_ACTION, NOT_ENOUGH_ARGUMENT, DATABASE_ERROR, TOKEN_EXPIRED, TOKEN_INVALID, USER_NOT_EXISTS
from fn.common import getFromRequest
from fn.req import ok, er, ng
from fn.auth import checkDataFromToken, verifyToken, getToken
from models.user import User

class Auth(Resource):
    def post(self):  
        type = getFromRequest(request, 'type')
        if not type:
            return er(NOT_ENOUGH_ARGUMENT, 'type')
        match = {
            'check': self.check,
            'auth': self.auth,
            'checkAdmin': self.checkAdmin
        }
        if not type in match.keys():
            return er(INVALID_ACTION)
        return match[type]() #type:ignore
    
    def check(self):
        username = getFromRequest(request, 'username')
        token = getFromRequest(request, 'token')
        if not token or not username:
            return er(NOT_ENOUGH_ARGUMENT, 'token, username')
        c = verifyToken(token, username)
        if c is True:
            return ok()
        elif c is None:
            return ng(TOKEN_EXPIRED)
        else:
            return er(INVALID_TOKEN)
        
    def auth(self):
        username = getFromRequest(request, 'username')
        password = getFromRequest(request, 'password')
        if not username or not password:
            return er(NOT_ENOUGH_ARGUMENT, 'username, password')
        user = User(username, password)
        try:
            if not user.exists():
                return ng(USER_NOT_EXISTS)
            if user.checkPassword():
                group = user.get()['group']
                return ok(getToken(username, group))
            else:
                return ng(TOKEN_INVALID)
        except Exception as e:
            return er(DATABASE_ERROR, str(e))
    
    def checkAdmin(self):
        token = getFromRequest(request, 'token')
        if not token:
            return er(NOT_ENOUGH_ARGUMENT, 'token')
        if checkDataFromToken(token, 'group', 'admin'):
            return ok(True)
        return ok(False)