import pymysql
from conf import getcfg

class database:
    def __init__(self):
        self.dbi = getcfg()['db']
        
    def __enter__(self):
        self.inst = pymysql.connect(
            host=self.dbi['host'],
            user=self.dbi['username'],
            password=self.dbi['password'],
            database='ecs_central',
            charset='utf8mb4'
        )
        return self.inst
    
    def __exit__(self, type, val, pos):
        self.inst.close()