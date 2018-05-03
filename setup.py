
# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyConFlask0518',
    version='1.0.0',
    description='HN Flask App',
    long_description=long_description,
    url='https://pyconflask0518.mybluemix.net/',
    license='Apache-2.0'
)
