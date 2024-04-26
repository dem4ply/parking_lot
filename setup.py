#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'flask==3.0.3', 'flask_restful==0.3.10', 'marshmallow==3.21.1',
    'factory-boy==3.3.0', 'flask-restx==1.3.0'
]

setup(
    author="dem4ply",
    author_email='dem4ply@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="small service for admin a parking lot",
    entry_points={
        'console_scripts': [
            'parking_lot=parking_lot.cli:main',
        ],
    },
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='parking_lot',
    name='parking_lot',
    packages=find_packages(include=['parking_lot', 'parking_lot.*']),
    url='https://github.com/dem4ply/parking_lot',
    version='0.0.1',
    zip_safe=False,
)
