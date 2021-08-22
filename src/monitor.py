from threading import Thread as T
from models.instance import getIId, setIId, writeActionHistory
from sdk import describeInstanceStatus
from time import sleep
from fn.common import getObject

class Monitor():
    def __init__(self):
        self.monitors: list[T] = []
        self.monitors.append(T(target=self.unexpectedDeletionMonitor))
        pass
    
    def unexpectedDeletionMonitor(self):
        while True:
            id = getIId()
            sleep(5)
            if not id:
                continue
            r = describeInstanceStatus(id)
            try:
                r = getObject(r, True)
                st = r.get('InstanceStatuses').get('InstanceStatus')
                if len(st) == 0:
                    print("[MONITOR] Detected nexpected deletion.")
                    writeActionHistory(None, id, 'udelete', '_monitor')
                    setIId('')
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