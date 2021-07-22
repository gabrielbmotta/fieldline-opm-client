#! /usr/bin/env python
import platform
import os.path as op
import os
import subprocess
import shutil

from setuptools import setup, find_packages

from distutils.command.build_py import build_py
from distutils.cmd import Command

descr = """Code for database management for Neurobooth application."""

DISTNAME = 'fieldline-client'
DESCRIPTION = descr
MAINTAINER = 'Juan G PC'
MAINTAINER_EMAIL = 'juangpc@gmail.com'
URL = ''
LICENSE = ''
DOWNLOAD_URL = 'https://github.com/juangpc/fieldline-opm-client.git'

# get the version
version = None
with open(os.path.join('fieldline_client', '__init__.py'), 'r') as fid:
    for line in (line.strip() for line in fid):
        if line.startswith('__version__'):
            version = line.split('=')[1].strip().strip('\'')
            break
if version is None:
    raise RuntimeError('Could not determine version')


if __name__ == "__main__":
    setup(name=DISTNAME,
          maintainer=MAINTAINER,
          maintainer_email=MAINTAINER_EMAIL,
          description=DESCRIPTION,
          license=LICENSE,
          url=URL,
          version=version,
          download_url=DOWNLOAD_URL,
          long_description=open('README.md').read(),
          classifiers=[
              'Intended Audience :: Science/Research',
              'Intended Audience :: Developers',
              'License :: OSI Approved',
              'Programming Language :: Python',
              'Topic :: Software Development',
              'Topic :: Scientific/Engineering',
              'Operating System :: Microsoft :: Windows',
              'Operating System :: POSIX',
              'Operating System :: Unix',
              'Operating System :: MacOS',
          ],
          platforms='any',
          install_requires=[
              'appdirs==1.4.3',
              'ifaddr==0.1.6',
              'netifaces==0.10.9',
              'numpy==1.18.2',
              'protobuf==3.11.3',
              'six==1.14.0',
              'zeroconf==0.24.5'
          ],
          packages=find_packages()
          )
