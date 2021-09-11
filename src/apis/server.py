from flask_restful import Resource
from flask import request
from conf import getserver
from fn.req import ok, ng, er
from fn.keywords import NO_SERVER_IP_FOUND
from models.instance import getIp
from mcstatus import MinecraftServer
from socket import timeout

class Server(Resource):
    def get(self):
        ep = request.endpoint
        self.ip = getIp()
        if self.ip:
            self.s = MinecraftServer(self.ip)
        m = {
            'get-server': self.server
        }
        return m[ep]() #type: ignore
        
    def server(self):
        ser = getserver()
        basic = {
            'mods': ser['mods'],
            'version': ser['version'],
            'since': ser['since'],
            'bestram': ser['bestram'],
            'term': ser['term'],
            'created': True if self.ip else False,
            'ip': self.ip
        }
        try:
            status = self.s.status()
        except:
            basic['online'] = False
            return ok(basic)
        raw = status.raw
        mods = raw.get('forgeData').get('mods')
        index = 0
        for m in mods:
            if m.get('modId') in ('minecraft', 'forge'):
                del mods[index]
            index += 1
        full = dict()
        full.update(basic)
        full.update({
            'online': True,
            'maxPlayers': status.players.max,
            'onlinePlayers': status.players.online,
            'motd': raw.get('description').get('text'),
            'onlinePlayersDetails': raw.get('players').get('sample'),
            'rawMods': mods
        })
        return ok(full)