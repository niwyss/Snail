#!/usr/bin/python

import json
import sys
import httplib
import sqlite3

if len(sys.argv) < 2:
    sys.exit('Usage: %s codeDDG [ex: PRU]' % sys.argv[0])

codeStation = sys.argv[1]

# Connection to the base
connection = sqlite3.connect('snail.sqlite')
connection.row_factory = sqlite3.Row

# Request parameters
data = open('parameters.json', 'r')
json_data_parametres = json.loads(data.read())
data.close()
HOST = json_data_parametres["host"] 
SELECTOR = json_data_parametres["selector"] 
PARAMS = json_data_parametres["params"] 
HEADERS = json_data_parametres["headers"]  

# Transforms stations list into dictionnary (Code DDG) -> (libelle)
stations = {}
sql = ' SELECT * FROM station '
for station in connection.execute(sql):
    code = station['codeDDG']
    name = station['name']
    stations[code] = name

# Get informations for this station 
conn = httplib.HTTPConnection(HOST)
conn.request("POST", SELECTOR, PARAMS % codeStation, HEADERS)
response = conn.getresponse()
data = response.read()
conn.close()
json_data_trains = json.loads(data)

# Print list of next trains for this station
trains = json_data_trains[0]['data']
for train in trains:
    code = train['trainMissionCode']
    terminus = train['trainTerminus'].strip().encode("utf-8", 'replace')
    lane = train['trainLane']
    hour = train['trainHour'][11:]
    name = stations[terminus].strip().encode("utf-8", 'replace')
    print('{0:4}  {1:5}  {3:1}  {2:35}'.format(code, hour, name, lane))


