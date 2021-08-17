from flask.json import JSONDecoder
from flask_restful import Resource
from flask import request
from fn import DATABASE_ERROR, NOT_ENOUGH_ARGUMENT, PARSE_ERROR, REQUEST_ERROR, ng, ok, writeStatusHistory
from conf import getcfg
from db import database
from sdk import describeAvailable, describeInstanceStatus, describePrice

class EcsSetstatus(Resource):
    def post(self):
        try:
            status = request.form['status']
        except:
            return ng(NOT_ENOUGH_ARGUMENT)
        try:
            with database() as d:
                cur = d.cursor()
                cur.execute('UPDATE `ecs_status` SET status="%s" WHERE id=1' % status)
                d.commit()
            writeStatusHistory(status=status)
            return ok()
        except:
            return ng(DATABASE_ERROR)

class EcsGetstatus(Resource):
    def get(self):
        with database() as d:
            cur = d.cursor()
            cur.execute("SELECT * FROM `ecs_status` WHERE id=1")
            r = cur.fetchone()
            print(r)
        if r:
            return ok(r[1])
        else:
            return ng(DATABASE_ERROR)
        
class EcsDescribe(Resource):
    def get(self):
        ep = request.endpoint
        m = {
            'desc-pric': self.price,
            'desc-inst': self.instance,
            'desc-avai': self.available,
            'desc-stat': self.status
        }
        return m[ep]() #type: ignore
                
    def price(self):
        r = describePrice()
        if not r:
            return ng(REQUEST_ERROR)
        de = JSONDecoder()
        r = de.decode(r)
        price = r.get("PriceInfo").get("Price").get("TradePrice")
        return ok(price)
    
    def instance(self):
        ecs = getcfg()['ecs']
        return ok({
            'type': ecs['type'],
            'bandwidth': ecs['i_bandwidth'],
            'disksize': ecs['disksize'],
            'zone': ecs['zone']
        })
    
    def available(self):
        r = describeAvailable()
        if not r:
            return ng(REQUEST_ERROR)
        de = JSONDecoder()
        r = de.decode(r)
        try:
            if len(r.get("AvailableZones").get("AvailableZone")) > 0:
                return ok(True)
            else:
                return ok(False)
        except:
            return ng(PARSE_ERROR)
        
    def status(self):
        r = describeInstanceStatus()
        if not r:
            return ng(REQUEST_ERROR)
        de = JSONDecoder()
        r = de.decode(r)
        try:
            st = r.get("InstanceStatuses").get("InstanceStatus")
            if len(st) > 0:
                status = st[0].get("Status")
                id = st[0].get("InstanceId")
                return ok({
                    'status': status,
                    id: id,
                    'created': True
                })
            else:
                return ok({
                    'created': False
                })
        except:
            return ng(PARSE_ERROR)