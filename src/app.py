from flask import Flask, request, jsonify, make_response
from flask_restful import Api, Resource
from werkzeug.exceptions import abort
from apis.ecs import EcsSetstatus

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

api.add_resource(EcsSetstatus, '/api/ecs/v1/setstatus')

if __name__ == '__main__':
    app.run(debug=True)
