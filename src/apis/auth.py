from flask_restful import Resource
from flask import request
from fn import INVALID_TOKEN, INVALID_ACTION, NOT_ENOUGH_ARGUMENT, DATABASE_ERROR, getFromRequest, ok, er, ng
from models.user import User
from itsdangerous import BadSignature, SignatureExpired, TimedJSONWebSignatureSerializer as TS
from conf import getcfg

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
        
def getToken(username, group):
    secret = getcfg()['secret']
    s = TS(secret_key=secret, expires_in=604800) # 7 days
    return s.dumps({'username': username, 'group': group}).decode('ascii')

def verifyToken(token, username):
    """Verify if a token is valid, expired or invalid. Returns `group`."""
    secret = getcfg()['secret']
    s = TS(secret_key=secret)
    try:
        data = s.loads(token)
        if username:
            if username == data['username']:
                return data['group']
        elif username is None:
            return data['group']
        return False
    except SignatureExpired:
        return None
    except BadSignature:
        return False
    
def isAdminToken(token):
    """Verify if a token has administrator's power."""
    group = verifyToken(token, None)
    if not group:
        return False
    return group == 'admin'