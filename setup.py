#!/usr/bin/env python
from setuptools import setup


setup(
    name="port-for",
    version="0.5.0",
    author="Mikhail Korobov",
    author_email="kmike84@gmail.com",
    packages=["port_for"],
    scripts=["scripts/port-for"],
    url="https://github.com/kmike/port-for/",
    license="MIT license",
    description="""Utility that helps with local TCP ports management.
    It can find an unused TCP localhost port and remember the association.""",
    long_description=open("README.rst").read(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: POSIX",
        "Topic :: System :: Installation/Setup",
        "Topic :: System :: Systems Administration",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
    ],
    python_requires=">=3.6",
)
