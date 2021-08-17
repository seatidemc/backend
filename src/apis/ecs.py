from flask_restful import Resource, abort
from flask import request
from fn import DATABASE_ERROR, NOT_ENOUGH_ARGUMENT, ng, ok, writeStatusHistory
from db import database

class EcsSetstatus(Resource):
    def post(self):
        try:
            status = request.form['status']
        except:
            return ng(NOT_ENOUGH_ARGUMENT)
        with database() as d:
            cur = d.cursor()
            cur.execute('UPDATE `ecs_status` SET status="%s" WHERE id=1' % status)
            d.commit()
        writeStatusHistory(status=status)
        return ok()
