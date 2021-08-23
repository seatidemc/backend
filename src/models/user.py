from db import database
from werkzeug.security import generate_password_hash, check_password_hash
from fn.keywords import DBNAME_USER
from fn.common import toFormattedTime
from pymysql.cursors import DictCursor

class User:
    def __init__(self, username, password=None, email=None):
        self.username = username
        self.password = password
        self.email = email
        pass
    
    def get(self):
        with database(DBNAME_USER) as d:
            cur = d.cursor(DictCursor)
            cur.execute("SELECT * FROM `data` WHERE username='{0}'".format(self.username))
            r = cur.fetchone()
            assert r
            del r['password']
            del r['last_updated']
            r['created_at'] = toFormattedTime(r['created_at']) #type:ignore
            return r
    
    def create(self):
        assert self.password
        hash = generate_password_hash(self.password)
        with database(DBNAME_USER) as d:
            cur = d.cursor()
            cur.execute("INSERT INTO `data` (username, password, email, `group`, created_at) VALUES ('{0}', '{1}', '{2}', 'std', NOW())".format(self.username, hash, self.email))
            d.commit()
        
    def exists(self):
        with database(DBNAME_USER) as d:
            cur = d.cursor()
            cur.execute("SELECT * FROM `data` WHERE username='{0}'".format(self.username))
            r = cur.fetchall()
            if len(r) > 0:
                return True
            return False
        
    def delete(self):
        with database(DBNAME_USER) as d:
            cur = d.cursor()
            cur.execute("DELETE FROM `data` WHERE username='{0}'".format(self.username))
            d.commit()
            
    def alter(self, dict: dict):
        with database(DBNAME_USER) as d:
            cur = d.cursor()
            for k, i in dict.items():
                cur.execute("UPDATE `data` SET `{0}`='{1}' WHERE username='{2}'".format(k, i, self.username))
            d.commit()
    
    def changePassword(self, newPassword):
        hash = generate_password_hash(newPassword)
        with database(DBNAME_USER) as d:
            cur = d.cursor()
            cur.execute("UPDATE `data` SET password='{0}' WHERE username='{1}'".format(hash, self.username))
            d.commit()
    
    def checkPassword(self):
        assert self.password
        with database(DBNAME_USER) as d:
            cur = d.cursor()
            cur.execute("SELECT password FROM `data` WHERE username='{0}'".format(self.username))
            r = cur.fetchone()
            assert r
            hash = r[0]
            return check_password_hash(hash, self.password)