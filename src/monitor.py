from threading import Thread as T
from models.instance import getIId, setIId, writeActionHistory
from sdk import describeInstanceStatus
from time import sleep
from fn.common import getObject

class Monitor():
    def __init__(self):
        self.work = T(target=self.monitor)
        pass
    
    def monitor(self):
        while True:
            print("[MONITOR] Monitoring instance status...")
            id = getIId()
            sleep(5)
            if not id:
                continue
            print("[MONITOR][DETECTED] Detected instance id in database " + id)
            r = describeInstanceStatus(id)
            try:
                r = getObject(r, True)
                st = r.get('InstanceStatuses').get('InstanceStatus')
                if len(st) == 0:
                    print("[MONITOR][DETECTED] Unexpected deletion.")
                    writeActionHistory(None, id, 'udelete', '_monitor')
                    setIId('')
                else:
                    status = st[0].get('Status')
                    print("[MONITOR] Normal: " + status)
                    continue
            except Exception as e:
                print("[MONITOR][ERROR] Error in monitor:")
                print(str(e))
    
    def start(self):
        self.work.daemon = True
        self.work.start()
        pass