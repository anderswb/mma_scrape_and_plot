import pickle
import numpy as np
import matplotlib.pyplot as plt

with open('fighters.pickle', 'rb') as f:
    # The protocol version used is detected automatically, so we do not
    # have to specify it.
    fighters = pickle.load(f)


names = ('Conor McGregor',
         'Ronda Rousey',
         'Sage Northcutt',
         'Bas Rutten',
         'Jose Aldo',
         'T.J. Dillashaw',
         'Mark Hunt',
         'Nick Diaz',
         'Royce Gracie',
         'Chris Weidman',
         'Anderson Silva',
         'Dana White')

for name in names:
    x = sorted(fighters[name]['nameentries'])
    y = list(range(1, len(fighters[name]['nameentries'])+1))
    plt.plot(x, y, '-', linewidth=2, label=name)

plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()
