from flask import jsonify
from flask.json import JSONDecoder
from db import database
import re
import urllib.request

NOT_ENOUGH_ARGUMENT = 'Not enough argument.'
DATABASE_ERROR = 'Database error.'
REQUEST_ERROR = 'Request error.'
PARSE_ERROR = 'Parse error.'

DBNAME_ECS = 'ecs'
DBNAME_USER = 'user'

def ng(text=None):
    return jsonify({
        'status': 'ng',
        'msg': text
    })
    
def ok(text=None):
    return jsonify({
        'status': 'ok',
        'data': text
    })

def getIP():
    with urllib.request.urlopen("https://pv.sohu.com/cityjson?ie=utf-8") as r:
        result = r.read().decode("utf8")
        ip = re.findall(r'\d+.\d+.\d+.\d+', result)
        if ip:
            return ip[0]
    return False
    
def getObject(response, str=False):
    """Convert a string-like to JSON Object (dictionary). If the string-like is already a string, set the second param to `True`."""
    de = JSONDecoder()
    return de.decode(response if str else toString(response))

def toString(a):
    """Forcefully convert an object to string using `utf-8` encoding."""
    return str(a, encoding='utf-8')

