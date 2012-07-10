#!/usr/bin/python

import json
import sys
import sqlite3
import os

def list(database_path, name):

    # Test : database
    if not os.path.exists(database_path):
        print "snail: error: database doesn't exist. Create it with : snail init."
        sys.exit(1)

    # Connection to the base
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row

    # Fetch data
    sql = ' SELECT * FROM station where name like ? '
    args = ['%' + name + '%']
    for station in connection.execute(sql, args):
        codeDDG = station['codeDDG']
        name = station['name'].strip().encode("utf-8", 'replace')
        print('{0:3}  {1:35} '.format(codeDDG, name))

