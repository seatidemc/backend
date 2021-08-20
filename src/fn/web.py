import re
import urllib.request

def getIP():
    with urllib.request.urlopen("https://pv.sohu.com/cityjson?ie=utf-8") as r:
        result = r.read().decode("utf8")
        ip = re.findall(r'\d+.\d+.\d+.\d+', result)
        if ip:
            return ip[0]
    return False