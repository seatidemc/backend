from flask import Flask, jsonify, make_response
from flask_restful import Api
from apis.ecs import EcsDescribe, EcsGetstatus, EcsSetstatus

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

api.add_resource(EcsSetstatus, PREFIX + 'setstatus')
api.add_resource(EcsGetstatus, PREFIX + 'getstatus')
api.add_resource(EcsDescribe, PREFIX + 'describe/price', endpoint = 'desc-pric')
api.add_resource(EcsDescribe, PREFIX + "describe/instance", endpoint = 'desc-inst')
api.add_resource(EcsDescribe, PREFIX + "describe/available", endpoint = 'desc-avai')
api.add_resource(EcsDescribe, PREFIX + "describe/status", endpoint = 'desc-stat')

if __name__ == '__main__':
    app.run(debug=True)
