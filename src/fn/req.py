from flask import jsonify

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