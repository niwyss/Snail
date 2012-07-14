#!/usr/bin/python

import json
import sys
import sqlite3
import os

def value_to_arg(value): 
    return '%' + value + '%'

def fetch_stations_by_name(connection, names):
    if names and len(names) != 0:
        sql = ' SELECT * FROM station WHERE ' + ' OR '.join('name LIKE ?' for n in names)
    else:
        sql = ' SELECT * FROM station '
    args = map(value_to_arg, names)
    return connection.execute(sql, args).fetchall()

def print_station(station):
    codeDDG = station['codeDDG']
    codeQLT = station['codeQLT']
    codeUIC = station['codeUIC']
    longitude = station['longitude']
    latitude = station['latitude']
    name = station['name'].strip().encode("utf-8", 'replace')
    print('{0:3}  {1:35} '.format(codeDDG, name))

def list(database_path, names):

    # Test : database
    if not os.path.exists(database_path):
        print "snail: error: database doesn't exist. Create it with : snail init."
        sys.exit(1)

    # Connection to the base
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row

    # Print stations
    for station in fetch_stations_by_name(connection, names):
        print_station(station)

    # Close the connection
    connection.close()

