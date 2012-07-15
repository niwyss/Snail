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
template_title_color = "%s" # "\033[4;37m%s\033[0m"
template_line_format_short = "{0:3}  {1:35}"
template_line_format_long = "{0:3}  {2:5}  {3:8}  {4:10}  {5:10}  {1:35}"


def fetch_stations_by_criteria(connection, criteria, patterns):
    
    # Default request
    sql = ' SELECT * FROM station '

    # Convert patterns to the proper format
    args = map(lambda x: '%' + x + '%', patterns)

    if criteria and patterns and len(patterns) != 0:

        # Criteria : name
        if criteria == 'name':
            sql = ' SELECT * FROM station WHERE ' + ' OR '.join(' name LIKE ?' for n in patterns)

        # Criteria : code
        elif criteria == 'code':
            sql = ' SELECT * FROM station WHERE ' + ' OR '.join(' codeDDG LIKE ?' for n in patterns)
   
    return connection.execute(sql, args).fetchall()


def print_titles(display_format):

    # Print short description
    if display_format == 'short':
        template_titles = template_title_color % template_line_format_short
        print(template_titles.format("DDG", "NAME"))

    # Print long description
    elif display_format  == 'long':
        template_titles = template_title_color % template_line_format_long
        print(template_titles.format("DDG", "NAME", "QLT", "UIC", "LONGITUDE", "LATITUDE"))


def print_station(station, display_format):
    codeDDG = station['codeDDG']
    codeQLT = station['codeQLT']
    codeUIC = station['codeUIC']
    longitude = station['longitude']
    latitude = station['latitude']
    name = station['name'].strip().encode("utf-8", 'replace')

    # Print short description
    if display_format == 'short':
        print(template_line_format_short.format(codeDDG, name))

    # Print long description
    elif display_format  == 'long':
        print(template_line_format_long.format(codeDDG, name, codeQLT, codeUIC, longitude, latitude))


def list(database_path, criteria, patterns, display_format):

    # Test : database
    if not os.path.exists(database_path):
        print "snail: error: database doesn't exist. Create it with : snail init."
        sys.exit(1)

    # Connection to the base
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row

    # Print stations
    stations = fetch_stations_by_criteria(connection, criteria, patterns)
    if stations and len(stations) > 0:
        print_titles(display_format)
        for station in stations:
            print_station(station,display_format )

    # Close the connection
    connection.close()

