from flask_restful import Resource, request
from sdk import describeBalance
from fn.req import ng, ok

class InfoDescribe(Resource):
    def get(self):
        ep = request.endpoint
        m = {
            'desc-balance': self.balance
        }
        return m[ep]() #type: ignore
    
    def balance(self):
        bal = describeBalance()
        if bal is None:
            return ng('Balance not found.')
        return ok(bal)