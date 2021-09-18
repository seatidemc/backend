from flask.json import JSONDecoder
import datetime
from fn.keywords import TIME_FORMAT

def getFromArgs(args, name: str):
    """A safe approach to getting a value from `args` object."""
    try:
        v = args[name]
        if v is '0':
            return 0
        if v.isdigit():
            return int(v)
        return v
    except:
        return None

def getFromRequest(request, name: str):
    """A safe approach to getting a value from `request` object."""
    try:
        return request.get_json(force=True)[name]
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