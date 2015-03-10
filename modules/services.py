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

import settings
import json
import sys
import requests

def __fetch_data_from_web(url, login, password):
    try:
        response = requests.get(url, auth=(login, password))
        return response.content
    except:
        print "snail: error: web service unreachable."
        sys.exit(0)

def fetch_next_trains(code_station):

    # Get informations for this service
    url = settings.URL_NEXT_TRAIN.format(code_station)
    login = settings.LOGIN
    password = settings.PASSWORD

    # Get data from the service
    return __fetch_data_from_web(url, login, password)
