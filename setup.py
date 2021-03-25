#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name='wssh3',
    version='0.3.0',
    author='Jeff Lindsay',
    author_email='jeff.lindsay@twilio.com',
    description='command-line websocket client+server shell',
    packages=find_packages(),
    install_requires=['ws4py>=0.2.4','gevent>=0.13.6'],
    data_files=[],
    entry_points={
        'console_scripts': [
            'wssh3 = wssh3:main',]},
)
