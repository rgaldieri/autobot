#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys

con = None

try:
    con = lite.connect('users.db.sqlite')
    
    cur = con.cursor()    
    cur.execute('SELECT * FROM settings')
    
    data = cur.fetchone()
    
    print data                
    
except lite.Error, e:
    
    print "Error %s:" % e.args[0]
    sys.exit(1)
    
finally:
    
    if con:
        con.close()