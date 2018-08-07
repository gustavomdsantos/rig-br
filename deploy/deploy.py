#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Script de deploy do RIG BR para Windows (setup .exe) e Linux (pacote .deb)
# Autor: Gustavo Moraes <gustavosotnas1@gmail.com>
# MIT License – Copyright (c) 2018 Gustavo Moraes

import sys, os, json, shutil, subprocess
from libs.pshwrapper.pshwrapper import PowerShellWrapper

paths = {
	'manifest': '../manifest.json',
	'build': 'build',
	'dist': 'dist',
	'spec': 'rig-br.spec',
	'pycache': '../src/__pycache__',
	'src': '../src/rig-br.py',
	'icon': '../../rig-br.wiki/icon/rig-br.ico',
	'iscc': 'C:\\Program Files (x86)\\Inno Setup 5\\ISCC.exe',
	'iss': '.\\innosetup\\rig-br.iss'
}

def readManifestFile():
	with open(paths['manifest']) as manifestJSON:
		manifest = json.load(manifestJSON)
	print(manifest)

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
	rm_R(paths['build'])
	rm_R(paths['dist'])
	rm_R(paths['spec'])
	rm_R(paths['pycache'])

def isPyinstallerInstalled():
	commandOutput = subprocess.run('pyinstaller --version',
		shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
	return True if commandOutput.returncode is 0 else False

def compile():
	commandInput = 'pyinstaller \''+ paths['src'] +'\' -w -i \''+ paths['icon'] +'\''
	if getPlatform() is "Windows":
		powershell = PowerShellWrapper()
		powershell.run(commandInput)
	else:
		commandOutput = subprocess.run(commandInput, shell=True)

# Create a corresponding package for the running OS.
def build():
	osName = getPlatform()
	if osName is "Windows":
		createWin32Package()
	elif osName is "Linux":
		createDebPackage()

def createWin32Package():
	if isInnoSetupInstalled():
		runInnoSetup()
	else:
		print("Build NOT started.")

def createDebPackage():
	raise NotImplementedError("Not implemented yet.")

def isInnoSetupInstalled():
	return True if os.path.isfile(paths['iscc']) else False

def runInnoSetup():
	powershell = PowerShellWrapper()
	powershell.run("& \'" + paths['iscc'] +"\' "+ paths['iss'])

# =================================== main ====================================

if len(sys.argv) > 1 and sys.argv[1] == '--clean':
	cleanBuild()
else:
	readManifestFile()
	detectOS()
	cleanBuild()
	if isPyinstallerInstalled():
		compile()
		build()
		cleanBuild()

# ================================= end main ==================================

class Deploy:
	"""Classe-base (interface) que determina os métodos que um Deploy deve ter,
	independentemente do SO usado"""
	def cleanBuild(self):
		raise NotImplementedError("Not implemented yet.")

	def isPyinstallerInstalled(self):
		raise NotImplementedError("Not implemented yet.")

	def compile(self):
		raise NotImplementedError("Not implemented yet.")

	def build(self):
		raise NotImplementedError("Not implemented yet.")

class Deploy4Windows(Deploy):
	"""Classe que faz deploy para Windows."""
	def cleanBuild(self):
		print("cleanBuild no Windows.")

	def isPyinstallerInstalled(self):
		print("isPyinstallerInstalled no Windows.")

	def compile(self):
		print("compile no Windows.")

	def build(self):
		print("build no Windows.")

class Deploy4Linux(Deploy):
	"""Classe que faz deploy para Linux."""
	def cleanBuild(self):
		print("cleanBuild no Linux.")

	def isPyinstallerInstalled(self):
		print("isPyinstallerInstalled no Linux.")

	def compile(self):
		print("compile no Linux.")

	def build(self):
		print("build no Linux.")