# sap-vm-extension

## Introduction
This script will find all the VMs within a subscription that:
1. Have ```SAP``` defined in the VM tags
2. Check whether they have the Azure Enhanced Monitoring (AEM) extension installed
3. Install the AEM extension if 1 above is true, but 2 above is not

## Installation
1. Download the code 
   ```git clone https://github.com/sajitsasi/sap-vm-extension.git```
2. Change directory 
   ```cd sap-vm-extension```
3. Add current subscription to environment variable 
   ```export AZ_SUBSCRIPTION_ID=$(az account show --query id)```
4. Run the code
   ```./check_vm_extensions.py```


## Contributing
This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.