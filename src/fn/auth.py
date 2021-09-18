from typing import Any
from conf import getcfg
from itsdangerous import BadSignature, SignatureExpired
from itsdangerous.jws import TimedJSONWebSignatureSerializer as TS


def getToken(username: str, group: str):
    secret = getcfg()['secret']
    s = TS(secret_key=secret, expires_in=604800) # 7 days
    return s.dumps({'username': username, 'group': group}).decode('ascii')

def verifyToken(token: str, username: str = None):
    """Verify if a token is valid, expired or invalid. Returns `True` if verified, `False` if invalid, `None` if expired."""
    secret = getcfg()['secret']
    s = TS(secret_key=secret)
    try:
        data = s.loads(token)
        if username:
            if username == data['username']:
                return True
        elif username is None:
            return True
        return False
    except SignatureExpired:
        return None
    except BadSignature:
        return False

def getDataFromToken(token: str, key: str):
    """Get internal data decoded from a token using a key."""
    secret = getcfg()['secret']
    s = TS(secret_key=secret)
    try:
        data = s.loads(token)
        if data:
            return data[key]
        return None
    except:
        return None

def checkDataFromToken(token: str, key: str, value: Any) -> bool:
    """Check if the corresponding value of internal data decoded is equivalent."""
    if not verifyToken(token):
        return False
    data = getDataFromToken(token, key)
    if not data:
        return False
    return data == value