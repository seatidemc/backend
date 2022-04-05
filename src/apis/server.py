from flask_restful import Resource
from flask import request
from fn.req import ok
from models.instance import getIp
from mcstatus import MinecraftServer

colorDict = {'dark_gray': '8', 'gold': '6', 'green': 'a', 'aqua': 'b', 'light_purple': 'd', 'white': 'f', 'red': 'c', 'gray': '7', 'yellow': 'e'}

def translate(bold, italic, color, text):
    result = text
    if colorDict.get(color) != None:
        result = '§' + str(colorDict.get(color)) + result;
    if bold: 
        result = '§l' + result;
    if italic:
        result = '§o' + result;
    return result + "§r";

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
        basic = {
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
        motdRaw = raw.get('description').get('extra')
        motd = ''
        if len(motdRaw) > 0:
            motd = "".join([translate(x.get('bold'), x.get('italic'), x.get('color'), x.get('text')) for x in motdRaw])
        index = 0
        for m in mods:
            if m.get('modId') in ('minecraft', 'forge', 'arclight', 'mohist'):
                del mods[index]
            index += 1
        full = dict()
        full.update(basic)
        full.update({
            'online': True,
            'maxPlayers': status.players.max,
            'onlinePlayers': status.players.online,
            'motd': motd,
            'onlinePlayersDetails': raw.get('players').get('sample'),
            'rawMods': mods
        })
        return ok(full)
    
    def getIp(self):
        return ok(self.ip)