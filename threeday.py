import praw
import time
"""
Automod code to flair users by default
author:
     flair_text: ""
     set_flair: ["S: 0 | B: 0", "red"]
"""


reddit = praw.Reddit(client_id='',
                     client_secret='',
                     username='',
                     password='',
                     user_agent='PreciousMetals moderation bot by u/hacksorskill')


STORAGE_SUB_SELL = "pmstimesub"
STORAGE_SUB_BUY = "pmstimesub2"
MESSAGE_WTS = """This listing has been removed.
\n\n\n\nYou can only create one [WTS]/[WTT] post every 48 hours. Please update your old listing with your new items and change the flair to “New Items”. 
\n\nPlease do not create another [WTS]/[WTT] post until your last post is 48 hours old.
\n\n[Here is a link to your old post.](https://reddit.com/{})
\n\nYou'll be able to create a new post in: **{} hours and {} minutes**
\n\nIf you believe this was done in error, [please message the mods](https://www.reddit.com/message/compose?to=%2Fr%2FPmsforsale).
\n\nThank you!"""
MESSAGE_WTB = """This post has been removed.
\n\n\n\nYou can only create one [WTB] post every 48 hours. 
\n\nPlease do not create another [WTB] post until your last post is 48 hours old. 
\n\n[Here is a link to your old post.](https://reddit.com/{})
\n\nYou'll be able to create a new post in: **{} hours and {} minutes**
\n\nIf you believe this was done in error, [please message the mods](https://www.reddit.com/message/compose?to=%2Fr%2FPmsforsale).
\n\nThank you!"""

max_time_difference = 172800

storage_subreddit = reddit.subreddit(STORAGE_SUB_SELL)
storage_subreddit2 = reddit.subreddit(STORAGE_SUB_BUY)


def get_remaining_time(creation_time, last_post_time):
    time_remaining = max_time_difference - (creation_time - last_post_time )
    remaining_hours = time_remaining // 3600
    remaining_minutes = (time_remaining % 3600) // 60
    if remaining_hours == 0 and remaining_minutes == 0:
        remaining_minutes = 1
    return (int(remaining_hours), int(remaining_minutes))


def get_last_post(author, post_type):
    #print(str(author) + " "  + str(post_type))
    if post_type == 1 or post_type == 3:
        flair_text = next(storage_subreddit.flair(str(author)))["flair_text"]
    elif post_type == 2:
        flair_text = next(storage_subreddit2.flair(str(author)))["flair_text"]
    else:
        flair_text=None
    if flair_text is None or len(flair_text) == 0:
        return(-1, -1)
    else:
        last_post = (float(flair_text.split("|")[0]), flair_text.split("|")[1])
        return last_post


def set_last_post(author, submission, post_type):
    if post_type == 1 or post_type == 3:
        storage_subreddit.flair.set(author, str(
            submission.created_utc) + "|" + str(submission.id))
    elif post_type == 2:
        storage_subreddit2.flair.set(author, str(
            submission.created_utc) + "|" + str(submission.id))
    print("Setting " + author + "'s last post")
