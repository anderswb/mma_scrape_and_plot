# -*- coding: utf-8 -*-

import sqlite3
import sys
import csv

print('Creating fighters dictionary from csv file')
fighters = dict()
with open('fighters.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    for row in readCSV:
        if row[2]:
            aliases = row[2].split(',')
            aliases = [alias.strip() for alias in aliases]
        else:
            aliases = None
        fighters[row[0]] = {'weightclasses': row[1], 'aliases': aliases}

print('Testing for duplicate aliases')
alias_list = []
for name in fighters:
    if fighters[name]['aliases']:
        for alias in fighters[name]['aliases']:
            if alias in alias_list:
                print("Warning: Found duplicate alias {}".format(alias))
            else:
                alias_list.append(alias)

print('Connecting to database')
conn = sqlite3.connect('databases/mma.db')

i = 1
for name in fighters:
    print('Processing fighter {} of {}'.format(i, len(fighters)))
    query = "SELECT selftext " \
            "FROM posts " \
            "WHERE idstr LIKE 't1_%' " \
            "AND (selftext LIKE '%{}%'".format(name)

    if fighters[name]['aliases']:
        for alias in fighters[name]['aliases']:
            query = query + " OR selftext LIKE '%" + alias + "%'"
    query += ')'
    print('Query:' + query)
    cursor = conn.execute(query)
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