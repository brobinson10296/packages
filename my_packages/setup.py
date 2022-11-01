from glob import glob
from os.path import basename, splitext
from setuptools import find_packages, setup

setup(
    name='gw_ee_lifetime_package',
    version='0.1.0',
    packages=find_packages(where='my_packages'),
    package_dir={'': 'my_packages'},
    py_modules=[splitext(basename(path))[0] for path in glob('my_packages/*.py')],
)
