# List VM counts for SAP extension
[![Deploy To Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fsajitsasi%2Fsap-vm-extension%2Fmain%2Fqueries%2Fsap-vm-count%2Fazuredeploy.json)
## Description
This query will:
1. Go through all active subscriptions for the user
2. Find VMs that have tags ```System: SAP```
3. Check to see whether these VMs have the Azure Enhanced Monitoring (AEM) extension required for SAP installed
4. Output VM counts (SAP Extension Present, SAP Extension NOT Present, Total VMs)
