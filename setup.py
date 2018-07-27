#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Script de setup do RIG BR – the Random Identity Generator – para brasileiros.
# Autor: Gustavo Moraes <gustavosotnas1@gmail.com>
# MIT License – Copyright (c) 2018 Gustavo Moraes

from setuptools import setup, setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='rig-br',
	version='0.3.0',
	author='Gustavo Moraes',
	author_email='gustavosotnas1@gmail.com',
	description='RIG BR – the Random Identity Generator – para brasileiros.',
	long_description=long_description,
	url='https://github.com/gustavosotnas/rig-br',
	classifiers=[
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3'
	],
	packages=setuptools.find_packages(),
	#packages=['rig-br'],
	install_requires=['easygui>=0.97']#,
	# entry_points={
	# 	'console_scripts': [
	# 		'encrypt=crytto.main:run'
	# 	]
	# }
)