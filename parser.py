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
    fighters[name]['nameentries'] = []
    if fighters[name]['aliases']:
        for alias in fighters[name]['aliases']:
            if alias in alias_list:
                print("Warning: Found duplicate alias {}".format(alias))
            else:
                alias_list.append(alias)

print('Connecting to database')
conn = sqlite3.connect('databases/mma.db')

print('Getting entries')
query = "SELECT created, selftext FROM posts WHERE self IS '1' OR self IS NULL"
cursor = conn.execute(query)
rows = cursor.fetchall()
print('Got {} entries'.format((len(rows))))

fighter_no = 1
for name in fighters:
    searchterms = [name]
    if fighters[name]['aliases']:
        for alias in fighters[name]['aliases']:
            searchterms.append(alias)

    print('Processing fighter {} of {}: {}. Search terms: {}'.format(fighter_no, len(fighters), name, searchterms))
    fighter_no += 1

    pattern = r'\b('
    i = 0
    for term in searchterms:
        if i != 0:
            pattern += '|'
        pattern += term
        i += 1
    pattern += r')\b'
    # print('Pattern: {}'.format(pattern))

    for row in rows:
        created = row[0]
        selftext = row[1]
        if re.search(pattern, selftext):
            fighters[name]['nameentries'].append(created)
    print('Found {} nameentries'.format(len(fighters[name]['nameentries'])))

for name in fighters:
    print('{}: {}'.format(name, len(fighters[name]['nameentries'])))

with open('fighters.pickle', 'wb') as f:
    # Pickle the dictionary using the highest protocol available.
    pickle.dump(fighters, f, pickle.HIGHEST_PROTOCOL)