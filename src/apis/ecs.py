from flask.json import JSONDecoder
from aliyunsdkcore.acs_exception.exceptions import ServerException
from flask_restful import Resource, abort
from flask import request
from fn.keywords import INVALID_ACTION, NOT_ENOUGH_ARGUMENT, PARSE_ERROR, PERMISSION_DENIED, REQUEST_ERROR
from fn.common import getFromRequest, getObject, toString
from fn.req import ng, ok, er
from models.instance import getIId, setIId, writeActionHistory, getLastInvocation 
from conf import getcfg
from sdk import allocateIp, deleteInstance, deploy, startInstance, createInstance, describeAvailable, describeInstanceStatus, describePrice, describeInvocationResult
from futures import doif
from threading import Thread as T
from base64 import b64decode
from apis.auth import isAdminToken

cfg = getcfg()

class EcsAction(Resource):
    def post(self):
        type = getFromRequest(request, 'type')
        token = getFromRequest(request, 'token')
        if not type or not token:
            return ng(NOT_ENOUGH_ARGUMENT, 'type, token')
        if not isAdminToken(token):
            return ng(PERMISSION_DENIED, 'Administrator\'s token is required.')
        self.id = getIId()
        match = {
            'new': self.new,
            'delete': self.delete,
            'start': self.start,
            'stop': self.stop
        }
        if not type in match.keys():
            return er(INVALID_ACTION)
        return match[type]() #type:ignore
    
    def init(self):
        id = self.id
        de = JSONDecoder()
        try:
            try:
                t1 = T(target=doif, args=(de, id, 'Stopped', allocateIp))
                t2 = T(target=doif, args=(de, id, 'Stopped', startInstance))
                t3 = T(target=doif, args=(de, id, 'Running', deploy))
                t1.start()
                t2.start()
                if str(cfg['deploy']) == 'True':
                    t3.start()   
            except:
                return ng('Failed to open tasks.')
            writeActionHistory(id, 'init')
            return ok()
        except ServerException as e:
            return ng('init ' + REQUEST_ERROR + " Details: " + str(e))
    
    def start(self):
        id = self.id
        try:
            startInstance(id)
            writeActionHistory(id, 'start')
        except ServerException as e:
            return ng('start ' + REQUEST_ERROR + " Details: " + str(e))
        return ok()
    
    def stop(self):
        id = self.id
        try:
            startInstance(id)
            writeActionHistory(id, 'stop')
        except ServerException as e:
            return ng('stop ' + REQUEST_ERROR + " Details: " + str(e))
        return ok()
    
    def delete(self):
        id = self.id
        try:
            deleteInstance(id)
            writeActionHistory(id, 'delete')
            setIId('')
        except ServerException as e:
            return ng('delete ' + REQUEST_ERROR + " Details: " + str(e))
        return ok()
    
    def new(self):
        id = self.id
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
        setIId(id)
        writeActionHistory(id, 'create')
        return self.init()

class EcsDescribe(Resource):
    def get(self):
        ep = request.endpoint
        m = {
            'desc-pric': self.price,
            'desc-inst': self.instance,
            'desc-avai': self.available,
            'desc-stat': self.status,
            'desc-lastinv': self.lastInvocation
        }
        return m[ep]() #type: ignore
    
    def lastInvocation(self):
        i = getLastInvocation()
        r = getObject(describeInvocationResult(i))
        if not i:
            return ng('No invocation history found.')
        if not r:
            return ng(REQUEST_ERROR)
        invocation = r.get('Invocation').get('InvocationResults').get('InvocationResult')
        if len(invocation) == 0:
            return ng('No invocation information found.')
        invocation = invocation[0]
        return ok({
            'status': invocation.get('InvocationStatus'),
            'output': toString(b64decode(invocation.get('Output'))),
            'error': invocation.get('ErrorInfo')
        })
     
    def price(self):
        r = describePrice()
        if not r:
            return ng(REQUEST_ERROR)
        r = getObject(r)
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
        r = getObject(r)
        try:
            if len(r.get('AvailableZones').get('AvailableZone')) > 0:
                return ok(True)
            else:
                return ok(False)
        except:
            return ng(PARSE_ERROR)
        
    def status(self):
        id = getIId()
        if not id:
            return ng('Unable to find instance id in database.')
        r = describeInstanceStatus(id)
        if not r:
            return ng(REQUEST_ERROR)
        r = getObject(r, True)
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