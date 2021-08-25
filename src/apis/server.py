from flask_restful import Resource
from flask import request
from conf import getserver
from fn.req import ok, ng, er
from models.instance import getIp
from mcstatus import MinecraftServer
from socket import timeout

class Server(Resource):
    def get(self):
        ep = request.endpoint
        self.ip = '39.105.144.104'
        # self.ip = getIp()
        # if not self.ip:
        #     return ng('No server ip found in database.')
        self.s = MinecraftServer(self.ip)
        try:
            self.s.status()
        except timeout:
            return ok({
                'online': False
            })
        m = {
            'get-status': self.status,
            'get-mods': self.server
        }
        return m[ep]() #type: ignore
    
    def status(self):
        return ok({
            'online': True
        })
        
    def server(self):
        ser = getserver()
        return ok({
            'mods': ser['mods'],
            'version': ser['version'],
            'since': ser['since'],
            'bestram': ser['bestram'],
            'term': ser['term']
        })