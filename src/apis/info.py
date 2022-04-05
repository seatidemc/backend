from pydoc import describe
from flask_restful import Resource, request
from sdk import describeBalance, describeDailyBilling, describeMonthlyBilling, describeTransaction
from fn.req import ng, ok
from fn.common import ifdef
from fn.keywords import NOT_ENOUGH_ARGUMENT, INVALID_ARGUMENT

class InfoDescribe(Resource):
    def get(self):
        ep = request.endpoint
        m = {
            'desc-balance': self.balance,
            'desc-fund': self.fund,
            'desc-billing': self.billing,
            'search-fund': self.searchFund
        }
        return m[ep]() #type: ignore
    
    def balance(self):
        bal = describeBalance()
        if bal is None:
            return ng('Balance not found.')
        return ok(bal)
    
    def fund(self):
        pageNum = int(ifdef(request.args.get('pageNum'), 1))
        maxResult = ifdef(request.args.get('maxResult'), 10)
        startDate = ifdef(request.args.get('startDate'))
        endDate = ifdef(request.args.get('endDate'))
        fund = describeTransaction(maxResult, pageNum, startDate, endDate)
        if fund is None:
            return ng('No transaction found.')
        return ok(fund)
    
    def searchFund(self):
        target = ifdef(request.args.get('target'))
        startDate = ifdef(request.args.get('startDate'))
        endDate = ifdef(request.args.get('endDate'))
        if target is None:
            return ng(NOT_ENOUGH_ARGUMENT, 'target')
        if not target in ['max-expense', 'amount']:
            return ng(INVALID_ARGUMENT, "type must be one of `max-expense`, `amount`.")
        if endDate is None:
            return ng(NOT_ENOUGH_ARGUMENT, 'endDate')
        page = 1
        fund = describeTransaction(maxResults=300, pageNum=page, startDate=startDate, endDate=endDate)
        if fund is None:
            return ng('No search result.')
        result = []
        result.extend(fund['result'])
        while len(fund['result']) != 0:
            page += 1
            fund = describeTransaction(maxResults=300, pageNum=page, startDate=startDate, endDate=endDate)
            if (fund is None): break
            result.extend(fund['result'])
        if target == 'amount':
            return ok(len(result))
        elif target == 'max-expense':
            negmax = result[0]
            for i in result:
                if i['flow'] != 'Expense' or float(negmax['amount']) >= float(i['amount']): continue
                negmax = i
            return ok(negmax)
    
    def billing(self):
        type = ifdef(request.args.get('type'), 'monthly')
        year = ifdef(request.args.get('year'))
        month = ifdef(request.args.get('month'))
        day = ifdef(request.args.get('day'))
        try:
            if type == 'monthly':
                if year is None or month is None:
                    return ng(NOT_ENOUGH_ARGUMENT, 'year, month')
                result = describeMonthlyBilling(year, month)
            elif type == 'daily':
                if year is None or month is None or day is None:
                    return ng(NOT_ENOUGH_ARGUMENT, 'year, month, day')
                if not month.startswith('0') and int(month) < 10:
                    month = "0" + month
                if not day.startswith('0') and int(day) < 10:
                    day = "0" + day
                result = describeDailyBilling(year, month, day)
            else:
                return ng(INVALID_ARGUMENT, 'Billing type must be `daily` or `monthly`.')
        except ValueError as e:
            return ng(INVALID_ARGUMENT)
        if result is None:
            return ng('No billing information found.')
        return ok(result)