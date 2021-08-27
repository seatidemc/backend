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
        except Exception:
            return ok({
                'online': False
            })
        m = {
            'get-server': self.server
        }
        return m[ep]() #type: ignore
        
    def server(self):
        ser = getserver()
        status = self.s.status()
        raw = status.raw
        mods = raw.get('forgeData').get('mods')
        index = 0
        for m in mods:
            if m.get('modId') in ('minecraft', 'forge'):
                del mods[index]
            index += 1
        return ok({
            'mods': ser['mods'],
            'version': ser['version'],
            'since': ser['since'],
            'bestram': ser['bestram'],
            'term': ser['term'],
            'ip': self.ip,
            'online': True,
            'maxPlayers': status.players.max,
            'onlinePlayers': status.players.online,
            'motd': raw.get('description').get('text'),
            'onlinePlayersDetails': raw.get('players').get('sample'),
            'rawMods': mods
        })