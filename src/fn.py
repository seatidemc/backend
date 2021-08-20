from flask import jsonify
from flask.json import JSONDecoder
import re
import urllib.request
import datetime

NOT_ENOUGH_ARGUMENT = 'Not enough argument.'
DATABASE_ERROR = 'Database error.'
REQUEST_ERROR = 'Request error.'
PARSE_ERROR = 'Parse error.'
INVALID_TOKEN = 'Invalid token.'
INVALID_ACTION = 'Invalid action.'
PERMISSION_DENIED = 'Permission denied.'

DBNAME_ECS = 'ecs'
DBNAME_USER = 'user'

TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

def ng(text=None, details=None):
    return jsonify({
        'status': 'ng',
        'msg': (text + ' Details: ' + details) if details else text
    })
    
def er(text=None, details=None):
    return jsonify({
        'status': 'error',
        'msg': (text + ' Details: ' + details) if details else text
    })
    
def ok(text=None, details=None):
    return jsonify({
        'status': 'ok',
        'data': (text + ' Details: ' + details) if details else text
    })

def getIP():
    with urllib.request.urlopen("https://pv.sohu.com/cityjson?ie=utf-8") as r:
        result = r.read().decode("utf8")
        ip = re.findall(r'\d+.\d+.\d+.\d+', result)
        if ip:
            return ip[0]
    return False

def getFromRequest(request, name: str):
    """A safe approach to getting a value from `request` object."""
    try:
        return request.form[name]
    except:
        return None

def getObject(response, str=False):
    """Convert a string-like to JSON Object (dictionary). If the string-like is already a string, set the second param to `True`."""
    de = JSONDecoder()
    return de.decode(response if str else toString(response))

def toString(a):
    """Forcefully convert an object to string using `utf-8` encoding."""
    return str(a, encoding='utf-8')

def toFormattedTime(dt: datetime.datetime):
    return dt.strftime(TIME_FORMAT)