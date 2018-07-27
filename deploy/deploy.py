#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Script de deploy do RIG BR para Windows (setup .exe) e Linux (pacote .deb)
# Autor: Gustavo Moraes <gustavosotnas1@gmail.com>
# MIT License – Copyright (c) 2018 Gustavo Moraes

import json, sys, shutil, subprocess

defaultPaths = {
	'dist': '../dist',
	'src': '../src/rig-br.py',
	'icon': '../../RIG BR.wiki/icon/rig-br.ico'
}

def readManifestFile():
	with open('../manifest.json') as json_data_file:
		data = json.load(json_data_file)
	print(data)

# Source:
# https://www.webucator.com/how-to/how-check-the-operating-system-with-python.cfm
def getPlatform():
	platforms = {
		'linux1' : 'Linux',
		'linux2' : 'Linux',
		'darwin' : 'OS X',
		'win32' : 'Windows'
	}
	if sys.platform not in platforms:
		return sys.platform
	
	return platforms[sys.platform]

def detectOS():
	osName = getPlatform()
	if osName is "Windows":
		print("I'm running on a Windows PC!")
	elif osName is "Linux":
		print("I'm running on a Linux PC!")
	else:
		print("I don't know where I'm being running.")

def rmDistFolder():
	distPath = defaultPaths['dist']
	try:
		print("Deleting '"+ distPath +"' folder...")
		shutil.rmtree(distPath)
		print("Deleted '"+ distPath +"' folder has been previously deleted.")
	except FileNotFoundError as fnfe:
		print("'"+ distPath +"' folder has been previously deleted.")

def isPyinstallerInstalled():
	commandOutput = subprocess.run('pyinstaller --version',
		shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
	return True if commandOutput.returncode is 0 else False

def compile():
	src = defaultPaths['src']
	icon = defaultPaths['icon']
	commandInput = 'pyinstaller \''+ src +'\' -w -i \''+ icon +'\''
	print(commandInput)
	commandOutput = subprocess.run(commandInput, shell=True)
	print(commandOutput.returncode)

readManifestFile()
detectOS()
rmDistFolder()
if isPyinstallerInstalled():
	compile()