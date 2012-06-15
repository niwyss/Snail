#!/usr/bin/python

import json
import sys
import re

if len(sys.argv) < 2:
    sys.exit('Usage: %s ville' % sys.argv[0])

# Parsing du fichier
data = open('listegares.json', 'r')
for line in data:
    json_data = json.loads(line)
data.close()

# Recuperation des donnees
gares = json_data['stations']
for gare in gares:
    if re.search(sys.argv[1], gare['name'], re.I):
        code = gare['codeDDG']
        name = gare['name']
        print code + "\t" + name

