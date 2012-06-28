#!/usr/bin/python

import json
import sys
import sqlite3

if len(sys.argv) < 2:
    sys.exit('Usage: %s ville' % sys.argv[0])

# Connection to the base
connection = sqlite3.connect('snail.sqlite')
connection.row_factory = sqlite3.Row

# Fetch data
sql = ' SELECT * FROM station where name like ? '
args = ['%' + sys.argv[1] + '%']
for station in connection.execute(sql,args):
    codeDDG = station['codeDDG']
    name = station['name'].strip().encode("utf-8", 'replace')
    print('{0:3}  {1:35} '.format(codeDDG, name))

