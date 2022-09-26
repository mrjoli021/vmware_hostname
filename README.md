# Set hostname on VM's on ESXi with Venter

## created by: Joli Martinez Email: jmartinez@zerobitsolutions.com

This app logs into a Vcenter grabs the hostnames off all the hosts and updates the DNS record for each host.  In 
this case DNS is running on a Windows host.

The API manual for the vcenter can be found locally on the vcenter at:
https://vcenter/mob

I used this article to write my script:
https://www.vcloudnine.de/first-steps-with-python-and-pyvmomi-vsphere-sdk-for-python/

# Installation
1.  run setup.py
```
python setup.py install
```
2.  Update the  .env file in the root directory with the following info:
```python
vcenter="<vcenter fqdn or ip>"
username="<vcenter username>"
password="<vcenter password>"
domain="<vcenter domain>"
```

3. Either run main.py manually or put it in a cronjob
```python
python main.py
```
