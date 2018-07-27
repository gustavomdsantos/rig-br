#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Script de deploy do RIG BR para Windows (setup .exe) e Linux (pacote .deb)
# Autor: Gustavo Moraes <gustavosotnas1@gmail.com>
# MIT License – Copyright (c) 2018 Gustavo Moraes

import json

def readManifestFile():
	with open('../manifest.json') as json_data_file:
		data = json.load(json_data_file)
	print(data)

readManifestFile()