import sys
from setuptools import setup
setup(
    name='pipyphone',
    description='Your homemade phone',
    author='Sean Dutton',
    package_dir={'': 'lib'},
    packages=['waveshare_epd'],
)
