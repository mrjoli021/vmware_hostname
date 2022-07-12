The API manual for the vcenter can be found locally on the vcenter at:
https://vcenter/mob

I used this article to write my script:
https://www.vcloudnine.de/first-steps-with-python-and-pyvmomi-vsphere-sdk-for-python/

# Installation
1. create a .env file in the root directory with the following info:
```python
vcenter="<vcenter fqdn or ip>"
username="<vcenter username>"
password="<vcenter password>"
```

2. run setup.py
```
python setup.py install
```

3. Either run main.py manually or put it in a cronjob
```python
python main.py
```
