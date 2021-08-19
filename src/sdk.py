from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526 import DescribeInvocationResultsRequest, RebootInstanceRequest, RunCommandRequest, DeleteInstanceRequest, StartInstanceRequest, AllocatePublicIpAddressRequest, CreateInstanceRequest, DescribePriceRequest, DescribeAvailableResourceRequest, DescribeInstanceStatusRequest
from conf import getcfg
from json import JSONDecoder

ecs = getcfg()['ecs']

client = AcsClient(
   ecs['access_key'], 
   ecs['access_secret'],
   ecs['region']
)

def describePrice():
    request = DescribePriceRequest.DescribePriceRequest()
    request.set_InstanceType(ecs['type'])
    request.set_InstanceNetworkType(ecs['network'])
    request.set_InternetChargeType(ecs['i_chargetype'])
    request.set_InternetMaxBandwidthOut(ecs['i_bandwidth'])
    request.set_SystemDiskCategory(ecs['disktype'])
    request.set_SystemDiskSize(ecs['disksize'])
    request.set_ZoneId(ecs['zone'])
    request.set_SpotStrategy(ecs['strategy'])
    response = client.do_action_with_exception(request)
    try:
        s = str(response, encoding='utf-8') #type: ignore
        return s
    except:
        return None
   

def describeAvailable():
    request = DescribeAvailableResourceRequest.DescribeAvailableResourceRequest()
    request.set_InstanceType(ecs['type'])
    request.set_SystemDiskCategory(ecs['disktype'])
    request.set_ZoneId(ecs['zone'])
    request.set_SpotStrategy(ecs['strategy'])
    request.set_DestinationResource('InstanceType')
    response = client.do_action_with_exception(request)
    try:
        s = str(response, encoding='utf-8') #type: ignore
        return s
    except:
        return None
    

def describeInstanceStatus(id):
    request = DescribeInstanceStatusRequest.DescribeInstanceStatusRequest()
    request.set_InstanceIds([id])
    response = client.do_action_with_exception(request)
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
    request.set_SystemDiskCategory(ecs['disktype'])
    request.set_SystemDiskSize(ecs['disksize'])
    request.set_ZoneId(ecs['zone'])
    request.set_SpotStrategy(ecs['strategy'])
    request.set_ImageId(ecs['image'])
    if ecs['password']:
        request.set_Password(ecs['password'])
    request.set_SpotPriceLimit(0)
    response = client.do_action_with_exception(request)
    try:
        s = str(response, encoding='utf-8') #type: ignore
    except:
        return None
    return s

def allocateIp(id):
    request = AllocatePublicIpAddressRequest.AllocatePublicIpAddressRequest()
    request.set_InstanceId(id)
    client.do_action_with_exception(request)
    
def startInstance(id):
    request = StartInstanceRequest.StartInstanceRequest()
    request.set_InstanceId(id)
    client.do_action_with_exception(request)
    
def deleteInstance(id):
    request = DeleteInstanceRequest.DeleteInstanceRequest()
    request.set_Force(True)
    request.set_InstanceId(id)
    client.do_action_with_exception(request)
    
def deploy(id):
    request = RunCommandRequest.RunCommandRequest()
    try:
        f = open('run.sh')
        cmd = f.read()
        f.close()
    except:
        return False
    request.set_InstanceIds([id])
    request.set_CommandContent(cmd)
    request.set_Type('RunShellScript')
    client.do_action_with_exception(request)
    
def rebootInstance(id):
    request = RebootInstanceRequest.RebootInstanceRequest()
    request.set_InstanceId(id)
    client.do_action_with_exception(request)