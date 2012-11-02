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

# Template
template_line_format_short = "{0:3}  {1:35}"
template_line_format_long  = "{0:3}  {2:14}  {3:14}  {1:35}"

def __fetch_all_stations(connection):
    sql = ' SELECT * FROM station '
    args = []
    return connection.execute(sql, args).fetchall()

def __fetch_stations_by_names(connection, names):
    sql = ' SELECT * FROM station WHERE ' + ' OR '.join(' name LIKE ?' for n in names)
    args = map(lambda x: '%' + x + '%', names)
    return connection.execute(sql, args).fetchall()

def __fetch_stations_by_codes(connection, codes):
    sql = ' SELECT * FROM station WHERE ' + ' OR '.join(' code LIKE ?' for n in codes)
    args = map(lambda x: '%' + x + '%', codes)
    return connection.execute(sql, args).fetchall()

def __print_station(station, display_format):
    code = station['code']
    longitude = station['longitude']
    latitude = station['latitude']
    name = station['name'].strip().encode("utf-8", 'replace')

    # Print short description
    if display_format == 'short':
        print(template_line_format_short.format(code, name))

    # Print long description
    elif display_format  == 'long':
        print(template_line_format_long.format(code, name, longitude, latitude))


def list(database_path, criteria, patterns, display_format):

    # Test : database
    if not os.path.exists(database_path):
        print "snail: error: database doesn't exist. Create it with : snail init."
        sys.exit(1)

    # Connection to the base
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row

    # Fetch stations
    if not patterns or len(patterns) == 0:
        stations = __fetch_all_stations(connection)
    elif criteria == 'code':
        stations = __fetch_stations_by_codes(connection, patterns)
    else:
        stations = __fetch_stations_by_names(connection, patterns)

    # Print stations
    if stations and len(stations) > 0:
        print "%d station(s)" % len(stations)
        for station in stations:
            __print_station(station,display_format )

    # Close the connection
    connection.close()
