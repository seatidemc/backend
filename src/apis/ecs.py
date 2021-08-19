from flask.json import JSONDecoder
from aliyunsdkcore.acs_exception.exceptions import ServerException
from flask_restful import Resource
from flask import request
from fn import PARSE_ERROR, REQUEST_ERROR, getId, updateId, ng, ok, updateId, writeHistory
from conf import getcfg
from sdk import allocateIp, deleteInstance, deploy, startInstance, createInstance, describeAvailable, describeInstanceStatus, describePrice
from futures import doif
from threading import Thread as T

cfg = getcfg()

class EcsAction(Resource):
    def get(self):
        ep = request.endpoint
        m = {
            'act-new': self.new,
            'act-delete': self.delete,
            'act-start': self.start
        }
        return m[ep]() #type: ignore
    
    def init(self):
        id = getId()
        de = JSONDecoder()
        try:
            try:
                t1 = T(target=doif, args=(de, id, 'Stopped', allocateIp))
                t2 = T(target=doif, args=(de, id, 'Stopped', startInstance))
                t3 = T(target=doif, args=(de, id, 'Running', deploy))
                t1.start()
                t2.start()
                t3.start()
            except:
                return ng('Failed to open tasks.')
            writeHistory(id, 'init')
            return ok()
        except ServerException as e:
            return ng('init ' + REQUEST_ERROR + " Details: " + str(e))
    
    def start(self):
        id = getId()
        try:
            startInstance(id)
            writeHistory(id, 'start')
        except ServerException as e:
            return ng('start ' + REQUEST_ERROR + " Details: " + str(e))
        return ok()
    
    def stop(self):
        id = getId()
        try:
            startInstance(id)
            writeHistory(id, 'stop')
        except ServerException as e:
            return ng('stop ' + REQUEST_ERROR + " Details: " + str(e))
        return ok()
    
    def delete(self):
        id = getId()
        try:
            deleteInstance(id)
            writeHistory(id, 'delete')
            updateId('')
        except ServerException as e:
            return ng('delete ' + REQUEST_ERROR + " Details: " + str(e))
        return ok()
    
    def new(self):
        id = getId()
        if id:
            return ng('There is already an instance recorded in the database.')
        r = createInstance()
        if not r:
            return ng('new ' + REQUEST_ERROR)
        de = JSONDecoder()
        r = de.decode(r)
        id = r.get('InstanceId')
        if not id:
            return ng('Failed to get InstanceId.')
        updateId(id)
        writeHistory(id, 'create')
        return self.init()

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
        price = r.get('PriceInfo').get('Price').get('TradePrice')
        return ok(price)
    
    def instance(self):
        ecs = cfg['ecs']
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
            if len(r.get('AvailableZones').get('AvailableZone')) > 0:
                return ok(True)
            else:
                return ok(False)
        except:
            return ng(PARSE_ERROR)
        
    def status(self):
        id = getId()
        if not id:
            return ng('Unable to find instance id in database.')
        r = describeInstanceStatus(id)
        if not r:
            return ng(REQUEST_ERROR)
        de = JSONDecoder()
        r = de.decode(r)
        try:
            st = r.get('InstanceStatuses').get('InstanceStatus')
            if len(st) > 0:
                status = st[0].get('Status')
                id = st[0].get('InstanceId')
                return ok({
                    'status': status,
                    'id': id,
                    'created': True
                })
            else:
                return ok({
                    'created': False
                })
        except:
            return ng(PARSE_ERROR)