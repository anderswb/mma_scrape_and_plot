# -*- coding: utf-8 -*-

import sqlite3
import sys
import csv

fighters = dict()
with open('fighters.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    for row in readCSV:
        fighters[row[0]] = {'weightclasses': row[1], 'aliases': row[2]}

conn = sqlite3.connect('databases/mma.db')

i = 1
for name in fighters:
    print('Processing fighter {} of {}'.format(i, len(fighters)))
    cursor = conn.execute("SELECT selftext FROM posts WHERE idstr LIKE 't1_%' AND selftext LIKE '%{}%'".format(name))
    fighters[name]['nameentries'] = len(cursor.fetchall())
    i += 1

#skipped = []
#for entry in cursor:
#    try:
#        #print(entry)
#        sys.stdout.buffer.write(entry[0].encode('utf-8'))
#    except:
#        skipped.append(entry)
#        continue

for name in fighters:
    print('{}: {}'.format(name, fighters[name]['nameentries']))