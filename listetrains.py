#!/usr/bin/python

import json
import sys
import re
import httplib

if len(sys.argv) < 2:
    sys.exit('Usage: %s codeDDG [ex: PRU]' % sys.argv[0])

# Parsing du fichier de parametres
data = open('parameters.json', 'r')
json_data_parametres = json.loads(data.read())
data.close()

# Recuperation des parametres
HOST = json_data_parametres["host"] 
SELECTOR = json_data_parametres["selector"] 
PARAMS = json_data_parametres["params"] 
HEADERS = json_data_parametres["headers"]  

# Parsing du fichier pour les gares
data = open('listegares.json', 'r')
json_data_gares = json.loads(data.read())
data.close()

# Transformation en dictionnaire (Code DDG station) -> (libelle station)
gares = json_data_gares['stations']
stations = {}
for gare in gares:
    code = gare['codeDDG']
    name = gare['name']
    stations[code] = name

# Recuperation de liste des trains
conn = httplib.HTTPConnection(HOST)
conn.request("POST", SELECTOR, PARAMS % sys.argv[1], HEADERS)
response = conn.getresponse()
data = response.read()
conn.close()
json_data_trains = json.loads(data)

# Affichage des informations sur les trains
trains = json_data_trains[0]['data']
for train in trains:
    code = train['trainMissionCode']
    terminus = train['trainTerminus']
    lane = train['trainLane']
    hour = train['trainHour']
    name = stations[terminus]
    print code + '\t' + lane + '\t' + hour + '\t' + name


