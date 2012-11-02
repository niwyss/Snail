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
# along with SNAIL.  If not, see <http://www.gnu.org/licenses/>.

import json
import sys
import httplib
import sqlite3
import os
import services

def execute(database_path, parameters_path):

    # Test : database
    if not os.path.exists(database_path):
        print "snail: error: database doesn't exist. Create it with : snail init."
        sys.exit(1)

    # Test : parameters.json
    if not os.path.exists(parameters_path):
        print "snail: error: parameters.json doesn't exist. Grab it from anywhere."
        sys.exit(1)

    # Get the stations list
    stations = services.fetch_stations(parameters_path, "000000000000")

    # Connection to the base
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    
    # Clean the base
    connection.execute(' delete from station '); 

    # Fill the table
    for station in stations['data']:
    
        # Fetch values from JSON
        values = (station['codeTR3A'],  
                  station['name'], 
                  station['type'], 
                  station['positions'][0]['latitude'],
                  station['positions'][0]['longitude'])

        # Insert a row of data
        connection.execute(''' insert into station(code,
                                                   name,
                                                   type, 
                                                   latitude,
                                                   longitude) 
                               values (?, ?, ?, ?, ?) ''', values )
    
    # Save (commit) the changes
    connection.commit()
