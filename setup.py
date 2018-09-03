import os
from setuptools import setup, find_packages
from io import open

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pseudodb',
    version='0.1alpha',
    description=(
        'pseudodb generates mock sqlite tables for testing'
    ),
    long_description=long_description,
    url='https://github.com/jackhenry/pseudodb',
    license='Apache',
    author=u'Jack Henry',
    packages=find_packages('.', exclude=['examples*', 'test*']),
    entry_points={
        'console_scripts': ['pseudodb = pseudodb.command:main'],
    },
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires = [
        'PyYAML',
        'records',
        'schema',
        'click'
    ]
)