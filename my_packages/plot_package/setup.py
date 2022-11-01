from glob import glob
from os.path import basename, splitext
from setuptools import find_packages, setup

setup(
    name='plot_package_files',
    version='0.1.0',
    packages=find_packages(),
)
