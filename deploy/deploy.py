#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Script de deploy do RIG BR para Windows (setup .exe) e Linux (pacote .deb)
# Autor: Gustavo Moraes <gustavosotnas1@gmail.com>
# MIT License – Copyright (c) 2018 Gustavo Moraes

import sys, os, json, shutil, subprocess

defaultPaths = {
	'build': 'build',
	'dist': 'dist',
	'spec': 'rig-br.spec',
	'pycache': '../src/__pycache__',
	'src': '../src/rig-br.py',
	'icon': '../../rig-br.wiki/icon/rig-br.ico',
	'iscc': 'C:\Program Files (x86)\Inno Setup 5\ISCC.exe',
	'iss': 'innosetup/rig-br.iss'
}

def readManifestFile():
	with open('../manifest.json') as json_data_file:
		data = json.load(json_data_file)
	print(data)

# Source:
#https://www.webucator.com/how-to/how-check-the-operating-system-with-python.cfm
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
		print("OS: Windows")
	elif osName is "Linux":
		print("OS: Linux")
	else:
		print("OS: Unknown ("+ osName +")")

def rm_R(fileOrFolder):
	if os.path.isfile(fileOrFolder):
		try:
			print("Deleting '"+ fileOrFolder +"' file...")
			os.remove(fileOrFolder)
		except OSError as ose:
			print("'"+ fileOrFolder +"' file has been previously deleted.")
	else:
		try:
			print("Deleting '"+ fileOrFolder +"' folder...")
			shutil.rmtree(fileOrFolder)
			print("The folder '"+ fileOrFolder +"' folder has been deleted successfully.")
		except FileNotFoundError as fnfe:
			print("'"+ fileOrFolder +"' folder has been previously deleted.")

def cleanBuild():
	rm_R(defaultPaths['build'])
	rm_R(defaultPaths['dist'])
	rm_R(defaultPaths['spec'])
	rm_R(defaultPaths['pycache'])

def isPyinstallerInstalled():
	commandOutput = subprocess.run('pyinstaller --version',
		shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
	return True if commandOutput.returncode is 0 else False

def compile():
	src = defaultPaths['src']
	icon = defaultPaths['icon']
	commandInput = 'pyinstaller \''+ src +'\' -w -i \''+ icon +'\''
	if getPlatform() is "Windows":
		# Workaround about PyInstaller (doesn't run in Python shells on Windows)
		commandInput = 'PowerShell -Command "& {'+ commandInput +'}"'
	print(commandInput)
	commandOutput = subprocess.run(commandInput, shell=True)
	print(commandOutput.returncode)

# def isInnoSetupInstalled():
# 	iscc = defaultPaths['iscc']
# 	commandInput = 'PowerShell -Command "&(“'+ iscc +'”)"'
# 	#commandInput = 'PowerShell -Command "&(“'+ iscc +'” /?)"'
# 	print(commandInput)
# 	commandOutput = subprocess.run(commandInput,
# 		shell=True)
# 		#shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
# 	return True if commandOutput.returncode is 0 else False

# def build():
# 	iscc = defaultPaths['iscc']
# 	iss = defaultPaths['iss']
# 	print("Build started!")
# 	commandInput = 'cmd.exe /C "'+ iscc +'" "'+ iss + '"'
# 	print(commandInput)
# 	commandOutput = subprocess.run(commandInput,
# 		shell=True)
# 		#shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
# 	return True if commandOutput.returncode is 0 else False

readManifestFile()
detectOS()
cleanBuild()
if isPyinstallerInstalled():
	compile()
# if getPlatform() is "Windows":
# 	if isInnoSetupInstalled():
# 		build()
# 	else:
# 		print("Build NOT started.")
# build()
