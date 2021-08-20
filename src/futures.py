from sdk import describeInstanceStatus
import time

def doif(de, type, cb, id=None, token=None):
    while True:
        r = describeInstanceStatus(id)
        if not r:
            raise Exception()
        r = de.decode(r)
        try:
            st = r.get('InstanceStatuses').get('InstanceStatus')
            if len(st) > 0:
                status = st[0].get('Status')
                print(status)
                if status == type:
                    print('do running: ' + type)
                    if id and token:
                        cb(id, token)
                    elif id:
                        cb(id)
                    elif token:
                        cb(token)
                    else:
                        cb()
                    break
                time.sleep(3)
            else:
                raise Exception()
        except:
            raise Exception()