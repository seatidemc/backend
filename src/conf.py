import yaml
import os
import io

def load(name):
    path = os.path.dirname(os.path.realpath(__file__))
    yamlPath = os.path.join(path, name)
    raw = io.open(yamlPath, 'r', encoding="utf-8").read()
    cfg = yaml.load(raw, Loader=yaml.FullLoader)
    return cfg

def getcfg():
    return load('config.yml')

def getserver():
    return load('server.yml')