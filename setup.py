#!/usr/bin/env python

#from distutils.core import setup
from setuptools import setup

setup(name='mailgunbot',
	  version='0.1.0',
	  description='Simple MailGun bot',
	  author='Chris Ochoa',
	  author_email='cochoa0x1@gmail.com',
	  packages=['mailgunbot'],
	  license='MIT',
	  url='https://github.com/cochoa0x1/mailgunbot',
	  install_requires=['requests','tqdm'],
	  )
