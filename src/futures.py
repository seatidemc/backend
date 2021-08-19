from sdk import describeInstanceStatus
import time

def doif(de, id, type, cb, withIdArg=True, timeToWait=3):
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
                    if withIdArg is True:
                        cb(id)
                    else:
                        cb()
                    break
                time.sleep(timeToWait)
            else:
                raise Exception()
        except:
            raise Exception()