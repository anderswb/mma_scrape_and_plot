# -*- coding: utf-8 -*-

import sqlite3
import sys
import csv
import re
import pickle

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
    fighters[name]['nameentries'] = 0
    if fighters[name]['aliases']:
        for alias in fighters[name]['aliases']:
            if alias in alias_list:
                print("Warning: Found duplicate alias {}".format(alias))
            else:
                alias_list.append(alias)

print('Connecting to database')
conn = sqlite3.connect('databases/mma.db')

print('Getting entries')
query = "SELECT selftext FROM posts WHERE self IS '1' OR self IS NULL"
cursor = conn.execute(query)
rows = cursor.fetchall()
print('Got {} entries'.format((len(rows))))

i = 1
for name in fighters:
    print('Processing fighter {} of {}'.format(i, len(fighters)))
    i += 1
    pattern = r'\b{}+\b'.format(name)
    for row in rows:
        string = row[0]
        if re.search(pattern, string):
            fighters[name]['nameentries'] += 1

for name in fighters:
    print('{}: {}'.format(name, fighters[name]['nameentries']))

with open('fighters.pickle', 'wb') as f:
    # Pickle the dictionary using the highest protocol available.
    pickle.dump(fighters, f, pickle.HIGHEST_PROTOCOL)