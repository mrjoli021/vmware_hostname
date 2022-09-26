from setuptools import setup
from pathlib import Path

dummy_data = ['vcenter="your_vcenter"',
              'username="vcenter_username"',
              'password="vcenter_password"',
              'domain="vcenter_domain"']

secret_file = Path('.env')

with open('requirements.txt') as f:
    required = f.read().splitlines()

# create .env file if it doesnt exist and populates it with dummy_data
if not secret_file.exists():
    with open(secret_file, 'w') as f:
        for line in dummy_data:
            f.write(line)
            f.write('\n')

setup(
    name='vmware_host',
    version='1.1',
    packages=[''],
    url='',
    license='MIT',
    author='jolim',
    author_email='jmartinez@zerobitsolutions.com',
    description='',
    install_requires=required
)
