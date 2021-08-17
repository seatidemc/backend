from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526 import DescribePriceRequest, DescribeAvailableResourceRequest, DescribeInstanceStatusRequest
from conf import getcfg

client = AcsClient(
   "LTAI5tA7M2vgpVAaePbsQWKZ", 
   "iRo9Rmwzqry5VpAdD39WUf9sIDEjWh",
   "cn-beijing"
)

ecs = getcfg()['ecs']

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
    try:
        response = client.do_action_with_exception(request)
    except:
        return None
    s = str(response, encoding='utf-8') #type: ignore
    return s

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
    except:
        return None
    s = str(response, encoding='utf-8') #type: ignore
    return s

def describeInstanceStatus():
    request = DescribeInstanceStatusRequest.DescribeInstanceStatusRequest()
    response = client.do_action_with_exception(request)
    try:
        s = str(response, encoding='utf-8') #type: ignore
    except:
        return None
    s = str(response, encoding='utf-8') #type: ignore
    return s