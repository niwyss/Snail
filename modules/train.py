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

def __fetch_trains(host, selector, params, headers, code_station):
    try:
        conn = httplib.HTTPConnection(host)
        conn.request("POST", selector, params % code_station, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close() 
        return json.loads(data)
    except:
        print "snail: error: web service unreachable."
        sys.exit(0)

def __fetch_all_stations(connection):
    sql = ' SELECT * FROM station '
    return connection.execute(sql).fetchall()

def __fetch_station_by_code_ddg(connection, code_ddg):
    sql = ' SELECT * FROM station where codeDDG = ? '
    args = [code_ddg]
    return connection.execute(sql, args).fetchone()

def __print_station(station):
    name = station['name'].strip().encode("utf-8", 'replace')
    codeDDG = station['codeDDG']
    codeQLT = station['codeQLT']
    codeUIC = station['codeUIC']
    longitude = station['longitude']
    latitude = station['latitude']
    print("{0} [{1}] ({2}/{3})").format(name, codeDDG, longitude, latitude)

def __print_train(train, stations):
    code = train['trainMissionCode']
    terminus = train['trainTerminus'].strip().encode("utf-8", 'replace')
    lane = train['trainLane']
    number = train['trainNumber']
    hour = train['trainHour'][11:]
    name = stations[terminus].strip().encode("utf-8", 'replace')
    print('{0:5}  {1:4}  {4:6}  {3:1}  {5:3}  {2:35}'.format(hour, code, name, lane, number, terminus))

def __print_information(information):
    print " - " + information.strip().encode("utf-8", 'replace').replace("\n", "\n   ")
  
def list(database_path, parameters_path, station_code_ddg):
    
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
    
    # Get webservice request configuration
    data = open(parameters_path, 'r')
    json_data_parametres = json.loads(data.read())
    data.close()
      
    # Transforms stations list into dictionnary
    stations = {}
    for station in __fetch_all_stations(connection):
        code = station['codeDDG']
        name = station['name']
        stations[code] = name
    
    # Only if code exits in database
    if station_code_ddg in stations:

        # Get informations for this station 
        host = json_data_parametres["host"] 
        selector = json_data_parametres["selector"] 
        params = json_data_parametres["params"]["list_trains"]
        headers = json_data_parametres["headers"]
        json_data_trains = __fetch_trains(host, selector, params, headers, station_code_ddg)
        
        # Print informations of the station
        station = __fetch_station_by_code_ddg(connection, station_code_ddg)
        __print_station(station)

        # Print list of next trains for this station
        trains = json_data_trains[0]['data']
        if trains and not len(trains) == 0:
            print "\n%d train(s)" % len(trains)
            for train in trains:
               __print_train(train, stations)

        # Print informations on the track
        infos = json_data_trains[0]['list']
        if infos and not len(infos) == 0:
            print "\n%d information(s)" % len(infos)
            for information in infos:
                __print_information(information)

    # Close the connection
    connection.close()
