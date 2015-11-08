__author__ = 'Anders'

fighters = ['Mendes', 'McGregor', 'Dalby', 'McDonald']
dataset = dict()
for fighter in fighters:
    dataset[fighter] = dict()
    dataset[fighter]['Count'] = 0

def searchcomment(time, commentbody):
    for fighter in fighters:
        if fighter.lower() in commentbody.body.lower():
            dataset[fighter]['Count'] += 1

with open('dataset.txt', 'r') as fp:
    while line:
        line = fp.readline()
        splitline = line.split(' ::: ', 2)
        timestamp = splitline[0]
        body = splitline[1]
        searchcomment(timestamp, body)

print(dataset)