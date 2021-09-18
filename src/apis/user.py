from fn.auth import checkDataFromToken
from models.user import User
from flask_restful import Resource
from flask import request
from fn.keywords import DATABASE_ERROR, INVALID_ACTION, NOT_ENOUGH_ARGUMENT, PERMISSION_DENIED, USER_ALREADY_EXISTS, USER_NOT_EXISTS
from fn.req import er, ng, ok
from fn.common import getFromRequest, getObject

class UserAction(Resource):
    def post(self):
        type = getFromRequest(request, 'type')
        token = getFromRequest(request, 'token')
        if not type or not token:
            return er(NOT_ENOUGH_ARGUMENT)
        if not type is 'create':
            if not checkDataFromToken(token, 'group', 'admin'):
                return ng(PERMISSION_DENIED)
        match = {
            'create': self.create,
            'delete': self.delete,
            'get': self.gets,
            'alter': self.alter,
            'changepasswd': self.changePassword
        }
        if not type in match.keys():
            return er(INVALID_ACTION)
        return match[type]() #type:ignore
      
    def create(self):
        username = getFromRequest(request, 'username')
        password = getFromRequest(request, 'password')
        email = getFromRequest(request, 'email')
        if not username or not password or not email:
            return er(NOT_ENOUGH_ARGUMENT, 'username, password, email')
        user = User(username, password, email)
        try:
            if user.exists():
                return ng(USER_ALREADY_EXISTS)
            user.create()
        except Exception as e:
            return er(DATABASE_ERROR, str(e))
        return ok()
        
    def delete(self):
        username = getFromRequest(request, 'username')
        if not username:
            return er(NOT_ENOUGH_ARGUMENT, 'username')
        user = User(username)
        try:
            if not user.exists():
                return ng(USER_NOT_EXISTS)
            user.delete()
        except Exception as e:
            return er(DATABASE_ERROR, str(e))
        return ok()
    
    def gets(self):
        username = getFromRequest(request, 'username')
        if not username:
            return er(NOT_ENOUGH_ARGUMENT, 'username')
        user = User(username)
        if not user.exists():
            return ng(USER_NOT_EXISTS)
        return ok(user.get())
    
    def changePassword(self):
        username = getFromRequest(request, 'username')
        newPassword = getFromRequest(request, 'newPassword')
        if not username or not newPassword:
            return er(NOT_ENOUGH_ARGUMENT, 'username, newPassword')
        user = User(username)
        if not user.exists():
            return ng(USER_NOT_EXISTS)
        try:
            user.changePassword(newPassword)
        except Exception as e:
            return er(DATABASE_ERROR, str(e))
        return ok()
    
    def alter(self):
        username = getFromRequest(request, 'username')
        toAlter = getFromRequest(request, 'toAlter')
        if not toAlter or not username:
            return er(NOT_ENOUGH_ARGUMENT, 'username, toAlter')
        user = User(username)
        try:
            obj = getObject(toAlter, True)
            try:
                del obj['password']
                del obj['username']
            except:
                pass
            user.alter(obj)
        except Exception as e:
            return er(DATABASE_ERROR, str(e))
        return ok()