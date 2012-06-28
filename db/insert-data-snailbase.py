#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
import json
import httplib
import sys
from urlparse import urlparse

if len(sys.argv) < 2:
    sys.exit('Usage: %s url' % sys.argv[0])

# Parse the url
url = urlparse(sys.argv[1])
server = url.netloc
path = url.path

if len(server) == 0 or len(path) == 0:
    sys.exit('Error: Bad url format !')

# Fetch data from web site
httpConnection = httplib.HTTPConnection(server)
httpConnection.request("GET", path)
httpResponse = httpConnection.getresponse()
data = httpResponse.read()
httpConnection.close()
json_data = json.loads(data)

# Connection to the base
connection = sqlite3.connect('snail.sqlite')

# Clean the base
connection.execute(' delete from station '); 

# Fill the table
stations = json_data['stations']
for station in stations:
    
    # Fetch values from JSON
    values = (station['name'],  
              station['x'], 
              station['y'], 
              station['codeDDG'], 
              station['codeUIC'], 
              station['codeQLT'])

    # Insert a row of data
    connection.execute(''' insert into station(name,  
                                               longitude, 
                                               latitude, 
                                               codeDDG, 
                                               codeUIC, 
                                               codeQLT) 
                           values (?, ?, ?, ?, ?, ?) ''', values )
    
# Save (commit) the changes
connection.commit()
