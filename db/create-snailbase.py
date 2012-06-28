#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3

# Connection to the base
connection = sqlite3.connect('snail.sqlite')

# Create table
connection.execute(''' create table station (id integer primary key, 
                                             name text,  
                                             longitude real, 
                                             latitude real, 
                                             codeDDG text, 
                                             codeUIC text, 
                                             codeQLT text)''')

# Save (commit) the changes 
connection.commit()
