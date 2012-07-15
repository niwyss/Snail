#!/usr/bin/python
# -*- coding:utf-8 -*-

# Copyright 2012 Nicolas Wyss
#
# This file is part of SNAIL.
#
# SNAIL is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SNAIL is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

import sqlite3
import json
import httplib
import sys
import os
from   urlparse import urlparse

def create(database_path):

    # Test : database
    if os.path.exists(database_path):
        print "snail: error: database already exists."
        sys.exit(1)

    # Connection to the base
    connection = sqlite3.connect(database_path)

    # Create table
    connection.execute(''' create table station (id integer primary key, 
                                                 name text,  
                                                 longitude real, 
                                                 latitude real, 
                                                 codeDDG text, 
                                                 codeUIC text, 
                                                 codeQLT text)''')

    # Save (commit) the changes 
    connection.commit()


def init(database_path, url):

    # Parse the url
    url = urlparse(url)
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
    connection = sqlite3.connect(database_path)
    
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

