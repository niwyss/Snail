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
import database
import services

def __print_stop(stop, stations):
    hour = stop['time'][11:]
    code = stop['codeGare']
    name = stations[code].strip()
    lane = stop['lane']
    print(unicode('{0:5}  {3:2}  {1:4}  {2:35} ').format(hour, code, name, lane))


# Infos about the train
def detail(database_path, parameters_path, code_train):
    
    # Test : database
    if not os.path.exists(database_path):
        print "snail: error: database doesn't exist. Create it with : snail init."
        sys.exit(1)

    # Test : parameters.json
    if not os.path.exists(parameters_path):
        print "snail: error: parameters.json doesn't exist. Grab it from anywhere."
        sys.exit(1)

    # Connection to the base
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
       
    # Transforms stations list into dictionnary
    stations = {}
    for station in database.fetch_all_stations(connection):
        code = station['code']
        name = station['name']
        stations[code] = name

    # Get informations for this train 
    train_infos = services.fetch_train_infos(parameters_path, code_train)

    # Print list of next stop for this train
    stops = train_infos['data']
    if stops and not len(stops) == 0:
        print "%d stop(s)" % len(stops)
        for stop in stops:
            __print_stop(stop, stations)
    
    # Close the connection
    connection.close()
