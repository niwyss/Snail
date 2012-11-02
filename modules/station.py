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

import json
import sys
import sqlite3
import os
import database

# Template
template_line_format  = unicode("{0:3}  {1:40} {4:4} ({2:0<13} / {3:0<13})")

def __print_station(station):
    code = station['code']
    longitude = station['longitude']
    latitude = station['latitude']
    name = station['name']
    compagnie = station['compagnie']
    print template_line_format.format(code, name, longitude, latitude, compagnie) 


def list(database_path, criteria, patterns):

    # Test : database
    if not os.path.exists(database_path):
        print "snail: error: database doesn't exist. Create it with : snail init."
        sys.exit(1)

    # Connection to the base
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row

    # Fetch stations
    if not patterns or len(patterns) == 0:
        stations = database.fetch_all_stations(connection)
    elif criteria == 'code':
        stations = database.fetch_stations_by_codes(connection, patterns)
    else:
        stations = database.fetch_stations_by_names(connection, patterns)

    # Print stations
    if stations and len(stations) > 0:
        print "%d station(s)" % len(stations)
        for station in stations:
            __print_station(station)

    # Close the connection
    connection.close()
