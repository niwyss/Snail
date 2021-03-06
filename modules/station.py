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

# Template
template_station_format  = unicode("{0:3}  {1:40} {4:4} ({2:0<13} / {3:0<13})")
template_train_format  = unicode("{0:5}  {1:4}  {4:6}  {3:2}  {5:3}  {2:35}  {6:3}  {7:35}  {8:10}")

# Global
stations = {}

def __print_station(station):

    # Prepare the output
    code = station['code']
    compagnie = station['compagnie']
    longitude = station['longitude']
    latitude = station['latitude']
    name = station['name']
    output = template_station_format.format(code, name, longitude, latitude, compagnie) 
    
    # Clean It
    output = unicodedata.normalize('NFKD', output).encode('ascii', 'ignore')
    
    print output
    
def __print_train(train):

    # Prepare the output
    code = train['trainMissionCode']
    terminus = train['trainTerminus']
    position = train['trainPosition']
    lane = train['trainLane']
    number = train['trainNumber']
    hour = train['trainHour'][11:]
    nameTerminus = stations[terminus].strip()
    namePosition = stations[position].strip()
    position = train['trainPosition']
    departure = train['trainDeparture']
    status = train['trainStatus']
    output = template_train_format.format(hour, code, nameTerminus, lane, number, terminus, position, namePosition, status)
    
    # Clean It
    output = unicodedata.normalize('NFKD', output).encode('ascii', 'ignore')
    
    print output  

def __print_information(information):
    print " - " + information.strip().encode("utf-8", 'replace').replace("\n", "\n   ")

# Find position of a train
def __get_train_position(stops):
      
    position = ""

    if stops and not len(stops) == 0:
        
        # Defautl : first stop
        position = stops[0]['codeGare']
        
        for stop in stops:
            
            # Get time
            time = stop['time'][11:]
            
            # Get position
            if not time or len(time) == 0:
                position = stop['codeGare']

    return position

# Find departure of a train
def __get_train_departure(stops):
    
    departure = ""

    if stops and not len(stops) == 0:
        departure = stops[0]['codeGare']
        
    return departure

# Find status of a train
def __get_train_status(departure, position, mention, stops):
    
    status = "."

    if mention and not len(stops) == 0:
        status = mention
    elif departure == position:
        status = "wait"
    else: 
        status = "incoming"
    
    return status
  
# Next trains on a station
def next(database_path, parameters_path, code_station):
    
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
    global stations
    stations[''] = ''
    for station in database.fetch_all_stations(connection):
        code = station['code']
        name = station['name']
        stations[code] = name
    
    # Only if code exits in database
    if code_station in stations:

        # Get informations for this station 
        station_infos = services.fetch_station_infos(parameters_path, code_station)
        
        # Print informations of the station
        station = database.fetch_station_by_code(connection, code_station)
        __print_station(station)

        # Print list of next trains for this station
        trains = station_infos['data']
        if trains and not len(trains) == 0:
            print "\n%d train(s)" % len(trains)
            codes = []
            for train in trains:

                # Get some ID for the train
                number = train['trainNumber']
                code = train['trainMissionCode']

                # Get some extra infos from train service
                departure = ""
                position = ""
                status = "."

                if not code in codes:
                    
                    # Keep the code
                    codes.append(code)
                    
                    # Get stops for this train 
                    stops = services.fetch_train_infos(parameters_path, number)['data']
                    
                    # Find position
                    position = __get_train_position(stops)
                    
                    # Find departure
                    departure = __get_train_departure(stops)
                    
                    # Find status
                    status = __get_train_status(departure, position, train['trainMention'], stops)

                # Print informations
                train['trainDeparture'] = departure
                train['trainStatus'] = status
                train['trainPosition'] = position
                __print_train(train)

        # Print informations on the track
        infos = station_infos['list']
        if infos and not len(infos) == 0:
            print "\n%d information(s)" % len(infos)
            for information in infos:
                __print_information(information)

    # Close the connection
    connection.close()

            
        

    
