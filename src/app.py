from flask import Flask, jsonify, make_response
from conf import getcfg
from flask_restful import Api
from apis.ecs import EcsAction, EcsDescribe
from apis.auth import Auth
from apis.user import UserAction
from monitor import Monitor

app = Flask(__name__)
api = Api(app)
monitor = Monitor()
monitor.start()

@app.errorhandler(404)
def notFoundError(err):
    return make_response(
        jsonify({
            'error': 'NOT_FOUND',
            'code': 404,
            'status': 'http-error'
        })
    )

@app.errorhandler(500)
def internalServerError(err):
    return make_response(
        jsonify({
            'error': 'INTERNAL_SERVER_ERROR',
            'code': 500,
            'status': 'http-error'
        })
    )

@app.errorhandler(401)
def unauthorizedError(err):
    return make_response(
        jsonify({
            'error': 'UNAUTHORIZED',
            'code': 401,
            'status': 'http-error'
        })
    )
    
NAME = 'ecs'
VERSION = 'v1'
PREFIX = '/api/' + NAME + '/' + VERSION + '/'

describe = [
    ('describe/price', 'desc-pric'),
    ('describe/instance', 'desc-inst'),
    ('describe/available', 'desc-avai'),
    ('describe/status', 'desc-stat'),
    ('describe/last-invoke', 'desc-lastinv'),
    ('describe/server', 'desc-server')
]

for desc in describe:
    api.add_resource(EcsDescribe, PREFIX + desc[0], endpoint = desc[1])
api.add_resource(EcsAction, PREFIX + 'action')

NAME = 'user'
VERSION = 'v1'
PREFIX = '/api/' + NAME + '/' + VERSION + '/'

api.add_resource(UserAction, PREFIX + 'action')
api.add_resource(Auth, PREFIX + 'auth')

if __name__ == '__main__':
    if getcfg()['production'] is True:
        from waitress import serve
        serve(app, host='0.0.0.0', port='8080') 
    else:
        app.run(debug=False)
