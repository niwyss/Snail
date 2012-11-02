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
import json
import httplib
import sys
import os
from   urlparse import urlparse

def create(database_path):

    # Test : database
    if os.path.exists(database_path):
        print "snail: error: database already exists."
        sys.exit(1)

    # Connection to the base
    connection = sqlite3.connect(database_path)

    # Create table update
    connection.execute(''' create table updates (id integer primary key, 
                                                 service text, 
                                                 date timestamp)''')

    # Create table station
    connection.execute(''' create table station (id integer primary key, 
                                                 code text,
                                                 name text,
                                                 type text,
                                                 longitude real, 
                                                 latitude real)''')

    # Save (commit) the changes 
    connection.commit()
