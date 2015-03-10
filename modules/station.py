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
import unicodedata
from BeautifulSoup import BeautifulSoup

# Template
template_station_format  = unicode("{0:8}  {1:55} {4:4} ({2:0<13} / {3:0<13}) {5:3}")
template_train_format  = unicode("{0:16} [{1:1}]  {2:6}  {3:4}  {4:40}")

# Global
stations = {}

def __print_station(station):

    # Prepare the output
    code = station['code']
    compagnie = station['compagny']
    longitude = station['longitude']
    latitude = station['latitude']
    name = station['name']
    zone_navigo = station['zone_navigo']
    output = template_station_format.format(code, name, longitude, latitude, compagnie, zone_navigo)

    # Clean It
    output = unicodedata.normalize('NFKD', output).encode('ascii', 'ignore')

    print output

def __print_train(date, date_mode, mission, number, terminus):

    # Prepare the output
    output = template_train_format.format(date, date_mode, number, mission, terminus)

    # Clean It
    output = unicodedata.normalize('NFKD', output).encode('ascii', 'ignore')

    print output

# Next trains on a station
def next(database_path, code_station):

    # Test : database
    if not os.path.exists(database_path):
        print "snail: error: database doesn't exist. Create it with : snail init."
        sys.exit(1)

    # Connection to the base
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row

    # Transforms stations list into dictionnary
    global stations
    stations[''] = ''
    for station in database.fetch_all_stations(connection):
        code = station['code']
        name = station['name']
        stations[code] = name

    # Only if code exits in database
    if code_station is not None and stations[code_station] is not None:

        # Get informations for this station
        trains = BeautifulSoup(services.fetch_next_trains(code_station)).passages.findAll("train")

        # Print informations of the station
        station = database.fetch_station_by_code(connection, code_station)
        __print_station(station)

        # Print list of next trains for this station
        if trains is not None and not len(trains) == 0:
            print "\n%d train(s)" % len(trains)

            for train in trains:

                # Get some ID for the train
                date = train.date.contents[0]
                date_mode = train.date["mode"]
                number = train.num.contents[0]
                mission = train.miss.contents[0]
                code_terminus = train.term.contents[0]
                terminus = stations.get(code_terminus, "Unknow")

                __print_train(date, date_mode, mission, number, terminus)

    # Close the connection
    connection.close()
