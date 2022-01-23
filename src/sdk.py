from aliyunsdkcore.client import AcsClient
from alibabacloud_bssopenapi20171214 import models as bssModel
from alibabacloud_bssopenapi20171214.client import Client as BssClient
from alibabacloud_tea_openapi import models as apiModel
from aliyunsdkecs.request.v20140526 import DescribeInvocationResultsRequest, StopInstanceRequest, RebootInstanceRequest, RunCommandRequest, DeleteInstanceRequest, StartInstanceRequest, AllocatePublicIpAddressRequest, CreateInstanceRequest, DescribePriceRequest, DescribeAvailableResourceRequest, DescribeInstanceStatusRequest
from conf import getcfg
from fn.common import getObject
from models.instance import getIId, writeCommandHistory, writeIp

ecs = getcfg()['ecs']
bss = apiModel.Config(access_key_id=ecs['access_key'], access_key_secret=ecs['access_secret'], endpoint='business.aliyuncs.com')

acsClient = AcsClient(
   ecs['access_key'], 
   ecs['access_secret'],
   ecs['region'],
   timeout=20
)

bssClient = BssClient(bss)

def describeBalance():
    try:
        bal = bssClient.query_account_balance()
        assert bal.body != None and bal.body.data != None
    except:
        return None
    result = bal.body.data.available_cash_amount
    return result

def describeTransaction(maxResults, pageNum = 1, startDate = None, endDate = None):
    try:
        if startDate is None: startDate = "2021-02-01T00:00:00Z"
        trans = bssClient.query_account_transactions(bssModel.QueryAccountTransactionsRequest(page_num=pageNum, page_size=maxResults, create_time_start=startDate, create_time_end=endDate))
        assert trans.body != None and trans.body.data != None and trans.body.data.account_transactions_list != None
    except Exception as e:
        return None
    result = [{'amount': t['Amount'], 'type': t['Remarks'], 'date': t['TransactionTime'], 'flow': t['TransactionFlow']} for t in trans.body.data.account_transactions_list.to_map()['AccountTransactionsList']]
    return {
        'result': result,
        'total': trans.body.data.total_count
    }
    
def describeDailyBilling(year: str, month: str, day: str):
    try:
        result = bssClient.query_account_bill(bssModel.QueryAccountBillRequest(billing_cycle=year + '-' + month, billing_date=year + '-' + month + '-' + day, granularity='DAILY'))
        assert result.body != None and result.body.data != None and result.body.data.items != None
        return result.body.data.items.to_map()['Item'][0]['PaymentAmount']
    except:
        return None
    
def describeMonthlyBilling(year: str, month: str):
    try:
        result = bssClient.query_account_bill(bssModel.QueryAccountBillRequest(billing_cycle=year + '-' + month))
        assert result.body != None and result.body.data != None and result.body.data.items != None
        return result.body.data.items.to_map()['Item'][0]['PaymentAmount']
    except:
        return None
    
def describePrice():
    request = DescribePriceRequest.DescribePriceRequest()
    request.set_InstanceType(ecs['type'])
    request.set_InstanceNetworkType(ecs['network'])
    request.set_InternetChargeType(ecs['i_chargetype'])
    request.set_InternetMaxBandwidthOut(ecs['i_bandwidth'])
    request.set_SystemDiskCategory(ecs['systemdisk']['type'])
    request.set_SystemDiskSize(ecs['systemdisk']['size'])
    request.set_DataDisk1Category(ecs['datadisk']['type'])
    request.set_DataDisk1Size(ecs['datadisk']['size'])
    request.set_ZoneId(ecs['zone'])
    request.set_SpotStrategy(ecs['strategy'])
    response = acsClient.do_action_with_exception(request)
    try:
        s = str(response, encoding='utf-8') #type: ignore
        return s
    except:
        return None
   

def describeAvailable():
    request = DescribeAvailableResourceRequest.DescribeAvailableResourceRequest()
    request.set_InstanceType(ecs['type'])
    request.set_SystemDiskCategory(ecs['systemdisk']['type'])
    request.set_DataDiskCategory(ecs['datadisk']['type'])
    request.set_ZoneId(ecs['zone'])
    request.set_SpotStrategy(ecs['strategy'])
    request.set_DestinationResource('InstanceType')
    response = acsClient.do_action_with_exception(request)
    try:
        s = str(response, encoding='utf-8') #type: ignore
        return s
    except:
        return None
    

def describeInstanceStatus(id):
    request = DescribeInstanceStatusRequest.DescribeInstanceStatusRequest()
    request.set_InstanceIds([id])
    response = acsClient.do_action_with_exception(request)
    try:
        s = str(response, encoding='utf-8') #type: ignore
        return s
    except:
        return None
    
def createInstance():
    request = CreateInstanceRequest.CreateInstanceRequest()
    request.set_InstanceType(ecs['type'])
    request.set_InternetChargeType(ecs['i_chargetype'])
    request.set_InternetMaxBandwidthOut(ecs['i_bandwidth'])
    request.set_SystemDiskCategory(ecs['systemdisk']['type'])
    request.set_SystemDiskSize(ecs['systemdisk']['size'])
    request.set_DataDisks([{
        "Size": ecs['datadisk']['size'],
        "Category": ecs['datadisk']['type'],
        "DeleteWithInstance": True
    }])
    request.set_ZoneId(ecs['zone'])
    request.set_SpotStrategy(ecs['strategy'])
    request.set_ImageId(ecs['image'])
    if ecs['password']:
        request.set_Password(ecs['password'])
    request.set_SpotPriceLimit(0)
    response = acsClient.do_action_with_exception(request)
    try:
        s = str(response, encoding='utf-8') #type: ignore
    except:
        return None
    return s

def allocateIp(id):
    request = AllocatePublicIpAddressRequest.AllocatePublicIpAddressRequest()
    request.set_InstanceId(id)
    r = getObject(acsClient.do_action_with_exception(request))
    writeIp(r.get('IpAddress'))
    
def startInstance(id):
    request = StartInstanceRequest.StartInstanceRequest()
    request.set_InstanceId(id)
    acsClient.do_action_with_exception(request)
    
def deleteInstance(id):
    request = DeleteInstanceRequest.DeleteInstanceRequest()
    request.set_Force(True)
    request.set_InstanceId(id)
    acsClient.do_action_with_exception(request)
    
def deploy(id, token):
    request = RunCommandRequest.RunCommandRequest()
    try:
        f = open('run.sh')
        cmd = f.read()
        f.close()
    except Exception as e:
        print('Cannot open run.sh: ' + str(e))
        cmd = 'echo No run.sh content.'
    request.set_InstanceIds([id])
    request.set_CommandContent(cmd)
    request.set_Type('RunShellScript')
    request.set_Timeout(99999)
    r = getObject(acsClient.do_action_with_exception(request))
    writeCommandHistory(token, r.get('CommandId'), r.get('InvokeId'))
    pass
    
def rebootInstance(id):
    request = RebootInstanceRequest.RebootInstanceRequest()
    request.set_InstanceId(id)
    acsClient.do_action_with_exception(request)
    
def stopInstance(id):
    request = StopInstanceRequest.StopInstanceRequest()
    request.set_InstanceId(id)
    acsClient.do_action_with_exception(request)
    
def describeInvocationResult(id):
    request = DescribeInvocationResultsRequest.DescribeInvocationResultsRequest()
    iid = getIId()
    if not iid:
        return None
    request.set_InvokeId(id)
    request.set_InstanceId(iid)
    return acsClient.do_action_with_exception(request)

def runCommand(id, token, cmd, timeout = 600):
    request = RunCommandRequest.RunCommandRequest()
    request.set_InstanceIds([id])
    request.set_CommandContent(cmd)
    request.set_Type('RunShellScript')
    request.set_Timeout(timeout)
    r = getObject(acsClient.do_action_with_exception(request))
    writeCommandHistory(token, r.get('CommandId'), r.get('InvokeId'))
    pass