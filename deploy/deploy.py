#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Script de deploy do RIG BR para Windows (setup .exe) e Linux (pacote .deb)
# Autor: Gustavo Moraes <gustavosotnas1@gmail.com>
# MIT License – Copyright (c) 2018 Gustavo Moraes

import sys, os, json, shutil, subprocess
from enum import Enum, unique
from deps.pshwrapper.pshwrapper import PowerShellWrapper

paths = {
	'manifest': '../manifest.json',
	'build': 'build',
	'dist': 'dist',
	'spec': 'rig-br.spec',
	'pycache': '../src/__pycache__',
	'src': '../src/rig-br.py',
	'icon': 'deps/rig-br.wiki/icon/rig-br.ico',
	'iscc': 'C:\\Program Files (x86)\\Inno Setup 5\\ISCC.exe',
	'iss': '.\\innosetup\\rig-br.iss'
}

def readManifestFile():
	with open(paths['manifest']) as manifestJSON:
		manifest = json.load(manifestJSON)
	print(manifest)

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

@unique
class OS(Enum):
	"""Enum de aliases para os principais sistemas operacionais."""

	WINDOWS = 'win32'
	LINUX = ['linux', 'linux1', 'linux2']
	OSX = 'darwin'

class DeployRunner():
	"""Classe estática que executa o script de deploy"""

	@staticmethod
	def run(deploy):
		deploy.cleanBuild()
		if deploy.isPyInstallerInstalled():
			deploy.compile()
			deploy.build()
			deploy.cleanBuild()
		else:
		 	print("\n ! PyInstaller is not installed!\n Please install it with: 'pip install pyinstaller'\n and run this script again.\n")

	@staticmethod
	def clean(deploy):
		deploy.cleanBuild()

class GenericDeploy:
	"""Classe-base (interface) que determina os métodos que um Deploy deve ter,
	independentemente do SO usado"""

	def __init__(self):
		print("\nRIG BR deploy script \n© 2018 Gustavo Moraes")
		raise NotImplementedError("ERROR: Unknown operating system ("+ sys.platform +")")

	def cleanBuild(self):
		raise NotImplementedError("Not implemented yet.")

	def isPyInstallerInstalled(self):
		raise NotImplementedError("Not implemented yet.")

	def compile(self):
		raise NotImplementedError("Not implemented yet.")

	def build(self):
		raise NotImplementedError("Not implemented yet.")

class Deploy4Windows(GenericDeploy):
	"""Classe que faz deploy para Windows."""

	# Override
	def __init__(self):
		print("\nRIG BR deploy script for Windows \n© 2018 Gustavo Moraes")

	# Override
	def cleanBuild(self):
		print("\n * Cleaning build...\n")
		rm_R(paths['build'])
		rm_R(paths['dist'])
		rm_R(paths['spec'])
		rm_R(paths['pycache'])

	# Override
	def isPyInstallerInstalled(self):
		print("\n * Detecting PyInstaller in this computer...\n")
		commandOutput = subprocess.run('pyinstaller --version',
			shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		return True if commandOutput.returncode is 0 else False

	# Override
	def compile(self):
		print("\n * Compiling program...\n")
		commandInput = 'pyinstaller \''+ paths['src'] +'\' -w -i \''+ paths['icon'] +'\''
		powershell = PowerShellWrapper()
		powershell.run(commandInput)

	# Override
	def build(self):
		print("\n * Building installer...\n")
		if self.__isInnoSetupInstalled():
			self.__createWin32Package()
		# else:
		# 	print("Build NOT started.")

	def __isInnoSetupInstalled(self):
		return True if os.path.isfile(paths['iscc']) else False

	def __createWin32Package(self):
		powershell = PowerShellWrapper()
		powershell.run("& \'" + paths['iscc'] +"\' "+ paths['iss'])

class Deploy4Linux(GenericDeploy):
	"""Classe que faz deploy para Linux."""

	# Override
	def __init__(self):
		print("\nRIG BR deploy script for Linux \n© 2018 Gustavo Moraes")

	# Override
	def cleanBuild(self):
		print("cleanBuild no Linux.")

	# Override
	def isPyInstallerInstalled(self):
		print("\n * Detecting PyInstaller in this computer...\n")
		commandOutput = subprocess.run('pyinstaller --version',
			shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		return True if commandOutput.returncode is 0 else False

	# Override
	def compile(self):
		print("\n * Compiling program...\n")
		commandInput = 'pyinstaller \''+ paths['src'] +'\' -w -i \''+ paths['icon'] +'\''
		commandOutput = subprocess.run(commandInput, shell=True)

	# Override
	def build(self):
		print("build no Linux.")

	def __createDebPackage(self):
		raise NotImplementedError("Not implemented yet.")

# =================================== main ====================================

def main():
	osName = sys.platform

	if osName in OS.WINDOWS.value:
		deploy = Deploy4Windows()
	elif osName in OS.LINUX.value:
		deploy = Deploy4Linux()
	else:
		deploy = GenericDeploy()

	try:
		if len(sys.argv) > 1 and sys.argv[1] == '--clean':
			DeployRunner.clean(deploy)
		else:
			DeployRunner.run(deploy)
	except NotImplementedError as nie:
		print(nie, file=sys.stderr)

main()

# ================================= end main ==================================
