from threading import Thread as T
from models.instance import getIId, getIp, setIId, writeActionHistory, writeIp
from sdk import deleteInstance, describeInstanceStatus
from time import sleep
from fn.common import getObject
from mcstatus import MinecraftServer

class Monitor():
    def __init__(self):
        self.serverCrashTimer = 0
        self.monitors: list[T] = []
        self.monitors.append(T(target=self.unexpectedDeletionMonitor))
        self.monitors.append(T(target=self.serverCrashMonitor))
        pass
    
    def serverCrashMonitor(self):
        """
        Check if the server is offline but the instance is online, which wastes lots of money. If so, the instance will be deleted after 60 retries if no action is taken.
        **Please note that this monitor bans the use of the instance without the server opened.**
        """
        while True:
            sleep(5)
            ip = getIp()
            id = getIId()
            if not id or not ip :
                self.serverCrashTimer = 0
                continue
            if self.serverCrashTimer >= 120:
                # if retries go over 120 times, delete the instance
                try:
                    deleteInstance(id)
                    writeActionHistory(None, id, 'sdelete', '_monitor')
                except Exception as e:
                    continue
            server = MinecraftServer(ip)
            try:
                # if the server is fine, everything is fine.
                server.status()
                self.serverCrashTimer = 0
                continue
            except:
                # the server is not fine.
                try:
                    r = describeInstanceStatus(id)
                except Exception as e:
                    print(str(e))
                    print("Error in serverCrashMonitor: Unable to get instance status.")
                    continue
                try:
                    # check if the instance exists
                    r = getObject(r, True)
                    st = r.get('InstanceStatuses').get('InstanceStatus')
                    if len(st) > 0:
                        # the instance exists, add one retry time
                        self.serverCrashTimer += 1
                    else:
                        continue
                except Exception as e:
                    print(str(e))
                    print("Error in serverCrashMonitor: Unable to get instance status in dict.")
    
    def unexpectedDeletionMonitor(self):
        while True:
            id = getIId()
            sleep(5)
            if not id:
                continue
            if id == 'OCCUPIED':
                continue
            try:
                r = describeInstanceStatus(id)
            except Exception as e:
                print(str(e))
                continue
            try:
                r = getObject(r, True)
                st = r.get('InstanceStatuses').get('InstanceStatus')
                if len(st) == 0:
                    print("[MONITOR] Detected unexpected deletion.")
                    writeActionHistory(None, id, 'udelete', '_monitor')
                    setIId('')
                    writeIp('')
                else:
                    # status = st[0].get('Status')
                    continue
            except Exception as e:
                print("[MONITOR][ERROR] Error in monitor:")
                print(str(e))
    
    def start(self):
        for m in self.monitors:
            m.daemon = True
            m.start()
        pass
