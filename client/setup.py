from distutils.core import setup
import setuptools


setup(
    name='copper_client',
    version='1.0',
    install_requires=[
        'requests',
        'beautifulsoup4'
    ],
    packages=[
        'copper_client'
    ],
    entry_points={
        "console_scripts": [
            "copper-watch = copper_client.client:watch" 
        ]
    },
   )
