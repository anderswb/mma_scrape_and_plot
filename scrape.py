__author__ = 'Anders'

import praw
import datetime
import time

fighters = ['Mendes', 'McGregor', 'Dalby', 'McDonald']

r = praw.Reddit(user_agent="MMA Scraber")

print('Getting submissions')
limit = 12000
submissions = r.get_subreddit('mma').get_new(limit=limit)

print('Iterating submissions')
i = 1
dataset = dict()
for fighter in fighters:
    dataset[fighter] = dict()
    dataset[fighter]['Count'] = 0

comments = []
times = []
for submission in submissions:
    print('Interating submission {} of {}'.format(i, limit))
    t0 = time.clock()
    submission.replace_more_comments(limit=16, threshold=10)
    flat_comments = praw.helpers.flatten_tree(submission.comments)
    for comment in flat_comments:

        comments.append({'date': datetime.datetime.fromtimestamp(comment.created),
                         'body': comment.body})
        #for fighter in fighters:
        #    if fighter.lower() in comment.body.lower():
        #        dataset[fighter]['Count'] += 1

    times.append(time.clock() - t0)
    tavg = sum(times)/len(times)

    seconds_remaining = int(tavg*(limit-i))
    m, s = divmod(seconds_remaining, 60)
    h, m = divmod(m, 60)
    print("Time remaining: %d:%02d:%02d" % (h, m, s))
    i += 1


with open('dataset.txt', 'w') as fp:
    for entry in comments:
        fp.write('{} :::::: {}\n'.format(entry['date'],
                                       entry['body'].replace('\n', ' ')))
