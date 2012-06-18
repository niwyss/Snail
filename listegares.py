#!/usr/bin/python

import json
import sys
import re

if len(sys.argv) < 2:
    sys.exit('Usage: %s ville' % sys.argv[0])

# Parsing du fichier
data = open('listegares.json', 'r')
json_data = json.loads(data.read())
data.close()

# Recuperation des donnees
gares = json_data['stations']
for gare in gares:
    if re.search(sys.argv[1], gare['name'], re.I):
        code = gare['codeDDG']
        name = gare['name']
        gpsX = gare['x']
        gpsY = gare['y']
        print code + "\t" + name

