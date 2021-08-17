import yaml
import os
import io

def getcfg():
    path = os.path.dirname(os.path.realpath(__file__))
    yamlPath = os.path.join(path, "config.yml")
    raw = io.open(yamlPath, 'r', encoding="utf-8").read()
    cfg = yaml.load(raw, Loader=yaml.FullLoader)
    return cfg