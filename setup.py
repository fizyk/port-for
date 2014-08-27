#!/usr/bin/env python
from distutils.core import setup

for cmd in ('egg_info', 'develop'):
    import sys
    if cmd in sys.argv:
        from setuptools import setup

version='0.3'

setup(
    name='port-for',
    version=version,
    author='Mikhail Korobov',
    author_email='kmike84@gmail.com',

    packages=['port_for'],
    scripts=['scripts/port-for'],

    url='https://github.com/kmike/port-for/',
    license = 'MIT license',
    description = """Utility that helps with local TCP ports managment. It can find an unused TCP localhost port and remember the association.""",

    long_description = open('README.rst').read(),

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',

        'Operating System :: POSIX',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Systems Administration',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
    ],
)
