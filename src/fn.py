from flask import jsonify
from db import database
import re
import urllib.request
import yaml
import os
import io

NOT_ENOUGH_ARGUMENT = 'Not enough argument.'
DATABASE_ERROR = 'Database error.'

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
    
def writeStatusHistory(status):
    ip = getIP()
    ip = ip if ip else '0.0.0.0'
    with database() as d:
        cur = d.cursor()
        cur.execute('INSERT INTO history (status, created_at, created_by) VALUES ("%s", NOW(), "%s")' % (status, ip))
        d.commit()
    pass

def getIP():
    with urllib.request.urlopen("https://pv.sohu.com/cityjson?ie=utf-8") as r:
        result = r.read().decode("utf8")
        ip = re.findall(r'\d+.\d+.\d+.\d+', result)
        if ip:
            return ip[0]
    return False

def getcfg():
    path = os.path.dirname(os.path.realpath(__file__))
    yamlPath = os.path.join(path, "config.yml")
    raw = io.open(yamlPath, 'r', encoding="utf-8").read()
    cfg = yaml.load(raw, Loader=yaml.FullLoader)
    return cfg