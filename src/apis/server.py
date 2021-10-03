from flask_restful import Resource
from flask import request
from conf import getcfg, getserver
from fn.req import ok, ng, er
from fn.keywords import NO_SERVER_IP_FOUND, NO_INSTANCE_ID_FOUND, NOT_ENOUGH_ARGUMENT, PERMISSION_DENIED, INVALID_ACTION
from fn.auth import checkDataFromToken
from fn.common import getFromRequest, getObject
from models.instance import getIId, getIp, writeCommandHistory
from mcstatus import MinecraftServer
from aiomcrcon import Client
from sdk import runCommand
import asyncio

class ServerInformation(Resource):
    def get(self):
        ep = request.endpoint
        self.ip = getIp()
        if self.ip:
            self.s = MinecraftServer(self.ip)
        m = {
            'get-server': self.server,
            'get-ip': self.getIp
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
    
    def getIp(self):
        return ok(self.ip)
    
class ServerAction(Resource):
    def post(self):
        try:
            self.cfg = getcfg()
        except:
            return ng("Couldn't get rcon configuration.")
        type = getFromRequest(request, 'type')
        self.token = getFromRequest(request, 'token')
        if not type or not self.token:
            return ng(NOT_ENOUGH_ARGUMENT, 'type, token')
        if not checkDataFromToken(self.token, 'group', 'admin'):
            return ng(PERMISSION_DENIED)
        self.ip = getIp()
        if not self.ip:
            return ng(NO_SERVER_IP_FOUND)
        match = {
            'shutdown': self.shutdown,
            'launch': self.launch,
            'execute': self.executeCommand
        }
        if not type in match.keys():
            return er(INVALID_ACTION)
        return match[type]() #type:ignore
    
    async def execute(self, command):
        async with Client(self.ip, self.cfg['rcon']['port'], self.cfg['rcon']['password']) as c: #type:ignore
            response = await c.send_cmd(command)
            return response
    
    def wait(self, func):
        asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(func)
    
    def shutdown(self):
        response = self.wait(self.execute("stop"))
        return ok(response)
    
    def launch(self):
        id = getIId()
        if not id:
            return ng(NO_INSTANCE_ID_FOUND)
        try:
            # TODO: THIS WON'T WORK FOR `SCREEN` COMMAND!!
            runCommand(id, self.token, self.cfg['launch-command'])
        except Exception as e:
            return er(str(e))
        return ok()
    
    def executeCommand(self):
        cmd = getFromRequest(request, "cmd")
        if not cmd:
            return ng(NOT_ENOUGH_ARGUMENT, 'cmd')
        try:
            response = self.wait(self.execute(cmd))
        except Exception as e:
            return ng(str(e))
        return ok(response)