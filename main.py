from pyVim.connect import SmartConnectNoSSL
import os
from dotenv import load_dotenv
import subprocess
import socket
from jinja2 import Environment, FileSystemLoader

load_dotenv()

# Variables


vcenter = os.getenv('vcenter')
username = os.getenv('username')
password = os.getenv('password')
domain = os.getenv('domain')

dmidecode = "dmidecode | grep 'Serial Number: VMware' | cut -d ':' -f 2 | cut -d '-' -f 2- | tr -d ' ' | sed 's/-//'"
current_hostname = os.uname()[1]

c = SmartConnectNoSSL(host=vcenter, user=username, pwd=password)

datacenter = c.content.rootFolder.childEntity[0]
vm_names = datacenter.vmFolder.childEntity
uuid_dict = {}

hostname = ""

template_file = "nsupdate_template.j2"

template_environment = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.getcwd()),
    trim_blocks=True,
    lstrip_blocks=True)


def my_ping(host):
    cmd = f"ping -c 1 {host}";
    response = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE);
    output, error = response.communicate()
    return response.returncode == 0


def get_ip_addr(interface):
    ip_addr_command = f"ip -br addr | grep {interface} | cut -d / -f 1 | tr -d ' ' | cut -d 'P' -f2"

    result = subprocess.getoutput(ip_addr_command)

    return result


# this loop gets names and UUID for all VM's in a given Vcenter and stores it into a dictionary called uuid_dict
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

# gets current UUID
local_uuid = subprocess.getoutput(dmidecode)

# if hostname does not contain a domain add it.
if domain not in current_hostname:
    current_hostname = f"{current_hostname}.{domain}"

# Search all dictionary entries for current hostname
for key, value in uuid_dict.items():

    if local_uuid in value:
        # print(f"UUID is {local_uuid} and hostname is {key}")
        hostname = key

        if current_hostname == f"{hostname}.{domain}":
            print("Hostnames match nothing to do")
            break

        # if host is alive, update it
        ping_result = my_ping(f"{hostname}.{domain}")

        ip_address = get_ip_addr("ens192")
        # j2_file = "nsupdate_template.j2"

        # sanitize hostname
        under_score = "_"
        dash = "-"

        if under_score in hostname:
            hostname = hostname.replace(under_score, dash)

        template_dict = {}
        template_dict["ping_result"] = ping_result
        template_dict["current_hostname"] = current_hostname
        template_dict["hostname"] = hostname.lower()
        template_dict["domain"] = domain
        template_dict["ip_address"] = ip_address

        t = template_environment.get_template(template_file)

        rendered_file = "rendered_template.txt"

        print(t.render(template_dict))

        with open(rendered_file, "w") as fh:
            fh.write(t.render(template_dict))

        # nsupdate
        subprocess.run(["nsupdate", rendered_file])

        # set hostname via command
        subprocess.run(["hostnamectl", "set-hostname", f"{hostname}.{domain}"])
        print(f" hostname being set to 'hostnamectl set-hostname {hostname}.{domain}'")

        # set /etc/hosts
        subprocess.run(["sed", "-i", f'2s/.*/127.0.0.1\t{hostname}.{domain}/', "/etc/hosts"])
