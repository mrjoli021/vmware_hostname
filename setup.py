from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()


setup(
    name='vmware_host',
    version='1.1',
    packages=[''],
    url='',
    license='',
    author='jolim',
    author_email='jmartinez@zerobitsolutions.com',
    description='',
    install_requires=required
)
