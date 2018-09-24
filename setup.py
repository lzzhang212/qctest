from setuptools import setup

setup(
    name = 'qctest',
    version = '0.1.0',
    packages = ['qctest'],
    entry_points = {
        'console_scripts': [
            'qctest = qctest.qingcloud_api:cli'
        ]
    })
