from flask.json import JSONDecoder
from aliyunsdkcore.acs_exception.exceptions import ServerException
from flask_restful import Resource
from flask import request
from fn.keywords import DUPLICATE_INSTANCE_CREATION, INVALID_ACTION, NOT_ENOUGH_ARGUMENT, NO_INSTANCE_ID_FOUND, PARSE_ERROR, PERMISSION_DENIED, REQUEST_ERROR
from fn.common import getFromRequest, getObject, toString
from fn.req import ng, ok, er
from fn.auth import checkDataFromToken
from models.instance import getIId, getIp, setIId, writeActionHistory, getLastInvocation, writeIp
from conf import getcfg
from sdk import allocateIp, deleteInstance, deploy, startInstance, createInstance, describeAvailable, describeInstanceStatus, describePrice, describeInvocationResult, stopInstance
from futures import doif
from threading import Thread as T
from base64 import b64decode
from urllib import request as R
cfg = getcfg()

class EcsAction(Resource):
    def post(self):
        type = getFromRequest(request, 'type')
        self.token = getFromRequest(request, 'token')
        if not type or not self.token:
            return ng(NOT_ENOUGH_ARGUMENT, 'type, token')
        if type != "new":
            if not checkDataFromToken(self.token, 'group', 'admin'):
                return ng(PERMISSION_DENIED)
        match = {
            'new': self.new,
            'delete': self.delete,
            'start': self.start,
            'stop': self.stop
        }
        if not type in match.keys():
            return er(INVALID_ACTION)
        return match[type]() #type:ignore
    
    def init(self, id):
        de = JSONDecoder()
        try:
            try:
                t1 = T(target=doif, args=(de, 'Stopped', allocateIp, id))
                t2 = T(target=doif, args=(de, 'Stopped', startInstance, id))
                t3 = T(target=doif, args=(de, 'Running', deploy, id, self.token))
                t1.start()
                t2.start()
                if str(cfg['deploy']) == 'True':
                    t3.start()   
            except:
                return ng('Failed to open tasks.')
            writeActionHistory(self.token, id, 'init')
            return ok()
        except ServerException as e:
            return ng('init ' + REQUEST_ERROR + " Details: " + str(e))
    
    def start(self):
        id = getIId()
        if not id:
            return ng(NO_INSTANCE_ID_FOUND)
        try:
            startInstance(id)
            writeActionHistory(self.token, id, 'start')
        except ServerException as e:
            return ng('start ' + REQUEST_ERROR + " Details: " + str(e))
        return ok()
    
    def stop(self):
        id = getIId()
        if not id:
            return ng(NO_INSTANCE_ID_FOUND)
        try:
            stopInstance(id)
            writeActionHistory(self.token, id, 'stop')
        except ServerException as e:
            return ng('stop ' + REQUEST_ERROR + " Details: " + str(e))
        return ok()
    
    def delete(self):
        id = getIId()
        if not id:
            return ng(NO_INSTANCE_ID_FOUND)
        try:
            deleteInstance(id)
            writeActionHistory(self.token, id, 'delete')
            setIId('')
            writeIp('')
        except ServerException as e:
            return ng('delete ' + REQUEST_ERROR + " Details: " + str(e))
        return ok()
    
    def new(self):
        id = getIId()
        if id:
            return ng(DUPLICATE_INSTANCE_CREATION)
        r = createInstance()
        if not r:
            return ng('new ' + REQUEST_ERROR)
        de = JSONDecoder()
        r = de.decode(r)
        id = r.get('InstanceId')
        if not id:
            return ng('Failed to get InstanceId.')
        setIId(id)
        writeActionHistory(self.token, id, 'create')
        return self.init(id)

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
        r = describeInvocationResult(i)
        if not r or not i:
            return ng('No invocation history found.')
        r = getObject(r)
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
        r = getObject(r, True)
        price = r.get('PriceInfo').get('Price').get('TradePrice')
        return ok(price)
    
    def instance(self):
        ecs = cfg['ecs']
        return ok({
            'type': ecs['type'],
            'bandwidth': ecs['i_bandwidth'],
            'systemdisk': {
                'size': ecs['systemdisk']['size'],
                'type': ecs['systemdisk']['type']
            },
            'datadisk': {
                'size': ecs['datadisk']['size'],
                'type': ecs['datadisk']['type']
            },
            'zone': ecs['zone']
        })
    
    def available(self):
        r = describeAvailable()
        if not r:
            return ng(REQUEST_ERROR)
        r = getObject(r, True)
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
            return ng(NO_INSTANCE_ID_FOUND)
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