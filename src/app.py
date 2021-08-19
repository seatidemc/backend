from flask import Flask, jsonify, make_response
from conf import getcfg
from flask_restful import Api
from apis.ecs import EcsAction, EcsDescribe

app = Flask(__name__)
api = Api(app)

@app.errorhandler(404)
def notFoundError(err):
    return make_response(
        jsonify({
            'error': 'NOT_FOUND',
            'code': 404
        })
    )

@app.errorhandler(500)
def internalServerError(err):
    return make_response(
        jsonify({
            'error': 'INTERNAL_SERVER_ERROR',
            'code': 500
        })
    )

@app.errorhandler(401)
def unauthorizedError(err):
    return make_response(
        jsonify({
            'error': 'UNAUTHORIZED',
            'code': 401
        })
    )
    
NAME = 'ecs'
VERSION = 'v1'
PREFIX = '/api/' + NAME + '/' + VERSION + '/'

api.add_resource(EcsDescribe, PREFIX + 'describe/price', endpoint = 'desc-pric')
api.add_resource(EcsDescribe, PREFIX + 'describe/instance', endpoint = 'desc-inst')
api.add_resource(EcsDescribe, PREFIX + 'describe/available', endpoint = 'desc-avai')
api.add_resource(EcsDescribe, PREFIX + 'describe/status', endpoint = 'desc-stat')
api.add_resource(EcsAction, PREFIX + 'action/new', endpoint = 'act-new')
api.add_resource(EcsAction, PREFIX + 'action/delete', endpoint = 'act-delete')
api.add_resource(EcsAction, PREFIX + 'action/start', endpoint = 'act-start')
api.add_resource(EcsAction, PREFIX + 'action/stop', endpoint = 'act-stop')

if __name__ == '__main__':
    app.run(debug=True)
