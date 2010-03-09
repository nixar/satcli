from setuptools import setup, find_packages
import sys, os

setup(name='satcli',
    version='0.1',
    description='Command Line Interface to RHN Satellite Server',
    classifiers=[], 
    keywords='',
    author='BJ Dierkes',
    author_email='wdierkes@rackspace.com',
    url='http://github.com/derks/satcli',
    license='GPL v2',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "ConfigObj",
        "Genshi",
        "Cement >=0.7.1, <0.9",
        # Uncomment to use shared plugins from The Rosendale Project.
        #"Rosendale",
        ],
    setup_requires=[
        ],
    test_suite='nose.collector',
    entry_points="""
    [console_scripts]
    satcli = satcli.core.appmain:main
    """,
    namespace_packages=[
        'satcli', 
        'satcli.bootstrap',
        'satcli.controllers',
        'satcli.model',
        'satcli.helpers',
        'satcli.templates',
        ],
    )
