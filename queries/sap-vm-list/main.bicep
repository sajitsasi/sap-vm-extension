resource SAPGraphQuery 'Microsoft.ResourceGraph/queries@2018-09-01-preview' = {
  name: 'CheckSAPExtensionQuery'
  location: 'global'
  properties: {
    description: 'Check if Azure Enhanced Monitoring Extension is installed which is required for SAP VMs'
    query: 'resources | where type == \'microsoft.compute/virtualmachines\' | where tags.system =~ \'SAP\' or tags.System =~ \'SAP\' | extend JoinID = toupper(id), VMName = tostring(properties.osProfile.computerName), OSType = tostring(properties.storageProfile.osDisk.osType), VMSize = tostring(properties.hardwareProfile.vmSize) | join kind=leftouter( resources | where type == \'microsoft.compute/virtualmachines/extensions\' | where name == "MonitorX64Linux" or name == "MonitorX64Windows" | extend VMId = toupper(substring(id, 0, indexof(id, \'/extensions\'))), Extension = name) on $left.JoinID == $right.VMId | extend SAPExtensionPresent = iff(Extension == "MonitorX64Linux" or Extension == "MonitorX64Windows", "Yes", "No") | summarize by VMName, VMSize, OSType, SAPExtensionPresent'
  }
}
