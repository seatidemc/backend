from flask import jsonify
from flask.json import JSONDecoder
from db import database
import re
import urllib.request

NOT_ENOUGH_ARGUMENT = 'Not enough argument.'
DATABASE_ERROR = 'Database error.'
REQUEST_ERROR = 'Request error.'
PARSE_ERROR = 'Parse error.'

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
    
def writeHistory(id, action):
    ip = getIP()
    ip = ip or '0.0.0.0'
    with database() as d:
        cur = d.cursor()
        cur.execute('INSERT INTO history (instance, action, created_at, created_by) VALUES ("%s", "%s", NOW(), "%s")' % (str(id), action, ip))
        d.commit()
    pass

def writeCommandHistory(cid, iid):
    ip = getIP()
    ip = ip or '0.0.0.0'
    with database() as d:
        cur = d.cursor()
        cur.execute('INSERT INTO cmd_history (command_id, invocation_id, created_at, created_by) VALUES ("%s", "%s", NOW(), "%s")' % (str(cid), str(iid), ip))
        d.commit()
    pass

def getIP():
    with urllib.request.urlopen("https://pv.sohu.com/cityjson?ie=utf-8") as r:
        result = r.read().decode("utf8")
        ip = re.findall(r'\d+.\d+.\d+.\d+', result)
        if ip:
            return ip[0]
    return False

def updateId(id):
    with database() as d:
        cur = d.cursor()
        cur.execute("UPDATE `ecs_status` SET instance='%s'" % str(id))
        d.commit()
    pass

def getId():
    with database() as d:
        cur = d.cursor()
        cur.execute("SELECT instance FROM `ecs_status` WHERE id=1")
        r = cur.fetchone()
        if not r:
            return None
        return r[0]
    
def getObject(response, str=False):
    de = JSONDecoder()
    return de.decode(response if str else toString(response))

def toString(a):
    return str(a, encoding='utf-8')

def getLastInvocation():
    with database() as d:
        cur = d.cursor()
        cur.execute("SELECT invocation_id FROM `cmd_history` ORDER BY id DESC")
        r = cur.fetchall()[0][0]
        return r