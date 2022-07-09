from pyVim.connect import SmartConnect, SmartConnectNoSSL
import ssl
import os

context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
context.verify_mode = ssl.CERT_NONE

vcenter = os.getenv('vcenter')
username = os.getenv('username')
password = os.getenv('password')

c = SmartConnectNoSSL(host=vcenter, user=username, pwd=password)

datacenter = c.content.rootFolder.childEntity[0]
vm_names = datacenter.vmFolder.childEntity

uuid_dict = {}

# this loop gets this names and UUID for all VM's and stores it into a dictionary
for i, j in enumerate(vm_names):
    # retrieves the config for each VM and puts it into a list format
    try:
        string_data = str(vm_names[i].config).split('\n')
    except AttributeError:
        pass
    # for each line in the config get the first UUID and add the VM name as the key and UUID as the value.
    for index in range(len(string_data)):
        if "uuid" in string_data[index]:
          formatted_uuid = string_data[index].split('=')
          # removes all preformatted data
          uuid_dict[j.name] = formatted_uuid[1].strip().replace("'", "").strip(',').replace("-", "")
          break


print(uuid_dict)
