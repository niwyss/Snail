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

import settings
import sqlite3
import sys
import os
import csv
import datetime
import time

def create(database_path):

    # Test : database
    if os.path.exists(database_path):
        print "snail: error: database already exists."
        sys.exit(1)

    # Connection to the base
    connection = sqlite3.connect(database_path)

    # Create table station
    connection.execute(''' create table station (id integer primary key,
                                                 code        text,
                                                 name        text,
                                                 city        text,
                                                 compagny    text,
                                                 zone_navigo int,
                                                 longitude   real,
                                                 latitude    real)''')

    # Save (commit) the changes
    connection.commit()

def init_with_file(database_path, stations_file, app_path):

    # Test : database
    if not os.path.exists(database_path):
        print "snail: error: database doesn't exist. Create it with : snail init."
        sys.exit(1)

    # Test : parameters.json
    if not stations_file:
        print "snail: error: parameters.json doesn't exist. Grab it from anywhere."
        sys.exit(1)

    # Connection to the base
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row

    # Clean the base
    connection.execute(' delete from station ');

    # Get a reader for the file
    reader = csv.DictReader(stations_file, delimiter=';')

    # Fill the table station
    for station in reader:

        # Fetch values from JSON
        code = station["code_uic"]
        name = station["libelle"].decode('utf-8')
        city = station["commune"].decode('utf-8')
        longitude, latitude = station["coord_gps_wgs84"].split(', ')
        zone_navigo = station["zone_navigo"]

        # Correct value for SNCF station
        compagny = "SNCF"
        if (station["gare_non_sncf"] == '1'):
            compagny = 'RATP'

        # Add to the database
        add_station(connection, code, name, compagny, longitude, latitude, city, zone_navigo)

    # Save (commit) the changes
    connection.commit()

    # Store station file
    store_station_file(stations_file, app_path)

def store_station_file(stations_file, app_path):

    # Create storage folder (if needed)
    data_path = os.path.join(app_path, settings.STATION_FILE_STORAGE_DIRECTORY_FOLDER)
    if  not os.path.exists(data_path):
        os.makedirs(data_path)

    # Move file
    st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S.csv')
    os.rename(stations_file.name, os.path.join(data_path, st))

def add_station(connection, code, name, compagnie, longitude, latitude, city, zone_navigo):
     values = (code, name, compagnie, longitude, latitude, city, zone_navigo)
     connection.execute(''' insert into station(code, name, compagny, longitude, latitude, city, zone_navigo)
                            values (?, ?, ?, ?, ?, ?, ?) ''', values )

def fetch_all_stations(connection):
    sql = ' SELECT * FROM station '
    args = []
    return connection.execute(sql, args).fetchall()

def fetch_stations_by_names(connection, names):
    sql = ' SELECT * FROM station WHERE ' + ' OR '.join(' name LIKE ?' for n in names)
    args = map(lambda x: '%' + x + '%', names)
    return connection.execute(sql, args).fetchall()

def fetch_stations_by_codes(connection, codes):
    sql = ' SELECT * FROM station WHERE ' + ' OR '.join(' code LIKE ?' for n in codes)
    args = map(lambda x: '%' + x + '%', codes)
    return connection.execute(sql, args).fetchall()

def fetch_station_by_code(connection, code):
    sql = ' SELECT * FROM station where code = ? '
    args = [code]
    return connection.execute(sql, args).fetchone()
