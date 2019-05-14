# -*- coding: utf-8 -*-

import os

from setuptools import setup
from setuptools import find_packages


README_FILE = os.path.join(
    os.path.abspath(
        os.path.dirname(__file__),
    ),
    'README.md',
)


with open(README_FILE) as fp:
    __description__ = fp.read()


setup(
    name='reqtools',
    version_format='{tag}',
    setup_requires=['setuptools-git-version'],
    url='https://github.com/oztqa/reqtools',
    packages=find_packages(include=('reqtools',), exclude=('tests',)),
    description='Extension for requests library',
    long_description=__description__,
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'requests',
        'curlify'
    ],
    classifiers=(
        'Development Status :: 4 - Beta',
        'Natural Language :: Russian',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
    ),
)
