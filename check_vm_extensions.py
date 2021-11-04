#!/usr/bin/env python3

import os
import logging
import sys
import re
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import SubscriptionClient
from azure.mgmt.compute import ComputeManagementClient

def filter_credential_warnings(record):
    if record.levelname == "WARNING":
        message = record.getMessage()
        return False
#O        return "DefaultAzureCredential" in message
    return True

# Remove pesky warnings from azure.identity
logger = logging.getLogger("azure.identity")
handler = logging.StreamHandler(stream=sys.stdout)
handler.addFilter(filter_credential_warnings)
logger.addHandler(handler)

# Check for environment variables
if 'AZ_SUBSCRIPTION_ID' not in os.environ:
    raise Exception("AZ_SUBSCRIPTION_ID environment variable not set.")
if 'AZ_SAP_VM_TAG_KEY' not in os.environ:
    raise Exception("AZ_SAP_VM_TAG_KEY environment variable not set.")
if 'AZ_SAP_VM_TAG_KEY' not in os.environ:
    raise Exception("AZ_SAP_VM_TAG_KEY environment variable not set.")
sub_id = os.environ['AZ_SUBSCRIPTION_ID']
tag_key = os.environ['AZ_SAP_VM_TAG_KEY']
tag_val = os.environ['AZ_SAP_VM_TAG_VAL']

# Get credentials
credentials = DefaultAzureCredential(exclude_shared_token_cache_credential=True)
subscription_client = SubscriptionClient(credentials, sub_id)
compute_client = ComputeManagementClient(credentials, sub_id)

sap_vm_list = []
vm_list = compute_client.virtual_machines.list_all()
column_width = 32
state_width = 16

print (f"Current VM status in subscription {sub_id}")
print("VM".ljust(column_width+8) + "State".ljust(state_width) + "SAP Extension".ljust(column_width))
print("-" * (column_width * 3))
for vm in vm_list:
    vm_tag_key = []
    vm_tag_val = []
    rg = vm.id.split("/")[4]
    status = compute_client.virtual_machines.instance_view(rg, vm.name)
    vm_prov_state = status.statuses[0].display_status.split(" ")[1]
    vm_state = status.statuses[1].display_status.split(" ")[1]
    aem_ext = False
    if vm.tags:
        vm_tag_key = [x for x in vm.tags.keys() if re.search(tag_key, x, re.IGNORECASE)]
        vm_tag_val = [x for x in vm.tags.values() if re.search(tag_val, x, re.IGNORECASE)]

    if vm_tag_key and vm_tag_val and status.extensions:
        ext_data = {}
        for ext in status.extensions:
            if "MonitorX64Linux" in ext.name or "MonitorX64Windows" in ext.name:
                aem_ext = True
                break

        if not aem_ext:        
            sap_vm_list.append(vm)
        print(vm.name.ljust(column_width+8) + vm_state.ljust(state_width) + str(aem_ext))
print("-" * (column_width * 3))

"""
TODO: Add SAP Extension to VMs that don't have it
print("\nAdding SAP extension to SAP VMs...")
for sap_vm in sap_vm_list:
    rg = vm.id.split("/")[4]
    if "Microsoft" in sap_vm.storage_profile.image_reference.publisher:
        aem_ext_name = "MonitorX64Windows"
    else:
        aem_ext_name = "MonitorX64Linux"
    print(f"Adding {aem_ext_name} extension to {sap_vm.name}")
    extension = compute_client.virtual_machine_extensions.begin_create_or_update(rg, sap_vm.name, aem_ext_name, {
        "location": sap_vm.location,
        "publisher": "Microsoft.AzureCAT.AzureEnhancedMonitoring",
        "type_properties_type": aem_ext_name,
        "type_handler_version": "1.0.0.87",
        "settings": { "system": "SAP" }
    }).result()
    print(f"Extension {aem_ext_name} added to {sap_vm.name} with return {extension}")
"""

    
print("\ndone")
