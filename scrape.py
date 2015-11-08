__author__ = 'Anders'

import praw
import time

r = praw.Reddit(user_agent="MMA Scraber")

print('Getting submissions')
limit = 12000
submissions = r.get_subreddit('mma').get_new(limit=limit)

print('Iterating submissions')
i = 1
comments = []
times = []
with open('dataset.txt', 'w') as fp:
    for submission in submissions:
        print('Interating submission {} of {}'.format(i, limit))
        t0 = time.clock()
        submission.replace_more_comments(limit=16, threshold=10)
        flat_comments = praw.helpers.flatten_tree(submission.comments)
        for comment in flat_comments:
            date = int(comment.created)
            body = comment.body.replace('\n', ' ')
            try:
                fp.write('{} ::: {}\n'.format(date, body))
            except:
                continue

        times.append(time.clock() - t0)
        tavg = sum(times)/len(times)

        seconds_remaining = int(tavg*(limit-i))
        m, s = divmod(seconds_remaining, 60)
        h, m = divmod(m, 60)
        print("Time remaining: %d:%02d:%02d" % (h, m, s))
        i += 1



