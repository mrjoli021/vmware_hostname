# Created by jolim at 7/9/22
#
# Purpose:
# Enter steps here
from setuptools import setup
import os

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(...
install_requires=required,
...)


setup(
    name='set hostname',
    version='1.0',
    scripts=['main.py'],
)
