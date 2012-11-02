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
import sys
import os
import services

def create(database_path):

    # Test : database
    if os.path.exists(database_path):
        print "snail: error: database already exists."
        sys.exit(1)

    # Connection to the base
    connection = sqlite3.connect(database_path)

    # Create table station
    connection.execute(''' create table station (id integer primary key, 
                                                 code      text,
                                                 name      text,
                                                 compagnie text,
                                                 longitude real, 
                                                 latitude  real)''')

    # Create table line
    connection.execute(''' create table line (id integer primary key, 
                                              code      text,
                                              network   text,
                                              position  integer,
                                              vehicle   text)''')

    # Save (commit) the changes 
    connection.commit()

def init(database_path, parameters_path):

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

    # Get the lines list
    lines = services.fetch_lines(parameters_path, "000000000000")

    # Connection to the base
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    
    # Clean the base
    connection.execute(' delete from station '); 

    # Fill the table station
    for station in stations['data']:
    
        # Fetch values from JSON
        code = station['codeTR3A']
        name = station['name']
        compagnie = station['type']
        longitude = station['positions'][0]['longitude']
        latitude = station['positions'][0]['latitude']

        # Correct value for SNCF station
        if (len(compagnie) == 0):
            compagnie = 'SNCF'  
        
        # Add to the database
        add_station(connection, code, name, compagnie, longitude, latitude)

    # Fill the table line
    for line in lines['data']:

        # Fetch values from JSON
        code = line['idLigne']
        position = line['position']
        vehicle = line['type']
        network = line['network']
        picto = line['picto']

        # Add to the database
        add_line(connection, code, position, vehicle, network) 

    # Save (commit) the changes
    connection.commit()

# Table : Line

def add_line(connection, code, position, vehicle, network):
     values = (code, position, vehicle, network) 
     connection.execute(''' insert into line(code, position, vehicle, network) 
                            values (?, ?, ?, ?) ''', values )    


# Table : Station

def add_station(connection, code, name, compagnie, longitude, latitude):
     values = (code, name, compagnie, longitude, latitude) 
     connection.execute(''' insert into station(code, name, compagnie, longitude, latitude) 
                            values (?, ?, ?, ?, ?) ''', values )           

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
