#!/usr/bin/env python3

import os
import logging
import sys
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import SubscriptionClient
from azure.mgmt.compute import ComputeManagementClient

def filter_credential_warnings(record):
    if record.levelname == "WARNING":
        message = record.getMessage()
        return False
#O        return "DefaultAzureCredential" in message
    return True


logger = logging.getLogger("azure.identity")
handler = logging.StreamHandler(stream=sys.stdout)
handler.addFilter(filter_credential_warnings)
logger.addHandler(handler)

credentials = DefaultAzureCredential(exclude_shared_token_cache_credential=True)
sub_id = os.environ['AZ_SUBSCRIPTION_ID']
subscription_client = SubscriptionClient(credentials, sub_id)
compute_client = ComputeManagementClient(credentials, sub_id)

vm_list = compute_client.virtual_machines.list_all()
column_width = 32
state_width = 16

print("VM".ljust(column_width+8) + "State".ljust(state_width) + "AEM Extension".ljust(column_width))
print("-" * (column_width * 3))
for vm in vm_list:
    rg = vm.id.split("/")[4]
    status = compute_client.virtual_machines.instance_view(rg, vm.name)
    vm_prov_state = status.statuses[0].display_status.split(" ")[1]
    vm_state = status.statuses[1].display_status.split(" ")[1]
    aem_ext = False
    if vm.tags and "SAP" in [x for x in vm.tags.values()] and status.extensions:
        ext_data = {}
        for ext in status.extensions:
            if "MonitorX64Linux" in ext.name or "MonitorX64Windows" in ext.name:
                aem_ext = True
                break

    print(vm.name.ljust(column_width+8) + vm_state.ljust(state_width) + str(aem_ext))
print("\ndone")