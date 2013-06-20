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

def __fetch_data_from_web(host, selector, params, headers):
    try:
        conn = httplib.HTTPConnection(host)
        conn.request("POST", selector, params, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close() 
        return json.loads(data)
    except:
        print "snail: error: web service unreachable."
        sys.exit(0)

def __read_configuration(parameters_path):
    try:
        data = open(parameters_path, 'r')
        json_data_parametres = json.loads(data.read())
        data.close()
        return json_data_parametres
    except:
        print "snail: error: configuration unreadable."
        sys.exit(0)

def fetch_stations(parameters_path, date):

    # Get configuration
    configuration =  __read_configuration(parameters_path)

    # Get informations for this service
    host = configuration["host"] 
    selector = configuration["selector"] 
    params = configuration["params"]["stations"] % date
    headers = configuration["headers"]

    # Get data from the service
    return __fetch_data_from_web(host, selector, params, headers)[0]

def fetch_lines(parameters_path, date):

    # Get configuration
    configuration =  __read_configuration(parameters_path)

    # Get informations for this service
    host = configuration["host"] 
    selector = configuration["selector"] 
    params = configuration["params"]["lines"] % date
    headers = configuration["headers"]

    # Get data from the service
    return __fetch_data_from_web(host, selector, params, headers)[0]

def fetch_station_infos(parameters_path, code_station):
    
    # Get configuration
    configuration =  __read_configuration(parameters_path)

    # Get informations for this service
    host = configuration["host"] 
    selector = configuration["selector"] 
    params = configuration["params"]["trains"] % code_station
    headers = configuration["headers"]

    # Get data from the service
    return __fetch_data_from_web(host, selector, params, headers)[0]

def fetch_train_infos(parameters_path, train_number):
    
    # Get configuration
    configuration =  __read_configuration(parameters_path)

    # Get informations for this service
    host = configuration["host"] 
    selector = configuration["selector"] 
    params = configuration["params"]["infos"] % train_number
    headers = configuration["headers"]

    # Get data from the service
    return __fetch_data_from_web(host, selector, params, headers)[0]


    
