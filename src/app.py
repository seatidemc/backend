from flask import Flask, jsonify, make_response
from conf import getcfg
from flask_restful import Api
from apis.ecs import EcsAction, EcsDescribe
from apis.auth import Auth
from apis.user import UserAction

app = Flask(__name__)
api = Api(app)

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

api.add_resource(EcsDescribe, PREFIX + 'describe/price', endpoint = 'desc-pric')
api.add_resource(EcsDescribe, PREFIX + 'describe/instance', endpoint = 'desc-inst')
api.add_resource(EcsDescribe, PREFIX + 'describe/available', endpoint = 'desc-avai')
api.add_resource(EcsDescribe, PREFIX + 'describe/status', endpoint = 'desc-stat')
api.add_resource(EcsDescribe, PREFIX + 'describe/last-invoke', endpoint = 'desc-lastinv')
api.add_resource(EcsAction, PREFIX + 'action')

NAME = 'user'
VERSION = 'v1'
PREFIX = '/api/' + NAME + '/' + VERSION + '/'

api.add_resource(UserAction, PREFIX + 'action')
api.add_resource(Auth, PREFIX + 'auth')

if __name__ == '__main__':
    if getcfg()['production'] is True:
        from waitress import serve
        serve(app, host='0.0.0.0', port='7093') 
    else:
        app.run(debug=True)
