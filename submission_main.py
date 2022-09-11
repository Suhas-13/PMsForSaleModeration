import praw
import time
from threeday import *
from helper import *
import regex
"""
Automod code to flair users by default
author:
     flair_text: ""
     set_flair: ["S: 0 | B: 0", "red"]
"""


with open("PMSBot.txt.txt", "a+") as f:
    f.write(" ")

while True:
    try:
        for submission in subreddit.stream.submissions():
            if submission is None:
                break
            elif submission.created_utc < time.time()-400:
                pass
            elif submission.id not in open("PMSBot.txt").read():
                with open("PMSBot.txt", "a+") as f:
                        f.write(" " + submission.id)
                removed=False
                if str(submission.author).lower() != "automoderator" and str(submission.author).lower() != "cancer-cheater":
                    post_type = get_post_type(str(submission.title))
                    last_post = get_last_post(
                        str(submission.author), post_type)
                    if post_type == -1:
                        submission.mod.remove()
                        mod_comment = submission.reply(title_removal_message)
                        mod_comment.mod.distinguish(how='yes', sticky=True)
                        removed=True
                    elif submission.created_utc-max_time_difference < last_post[0]:
                        remaining_time = get_remaining_time(submission.created_utc, last_post[0])
                        if post_type == 1:
                            mod_comment = submission.reply(
                                MESSAGE_WTS.format(str(last_post[1]), str(remaining_time[0]), str(remaining_time[1])), )
                        elif post_type == 2:
                            mod_comment = submission.reply(
                                MESSAGE_WTB.format(str(last_post[1]), str(remaining_time[0]), str(remaining_time[1])), )
                        elif post_type == 3:
                            mod_comment = submission.reply(
                                MESSAGE_WTS.format(str(last_post[1]), str(remaining_time[0]), str(remaining_time[1])))
                        mod_comment.mod.distinguish(how='yes', sticky=True)
                        submission.mod.remove()
                        removed=True
                        
                    elif (post_type == 1 or post_type == 3) and image_found(submission.selftext) == False:
                        mod_comment = submission.reply(post_no_proof_picture)
                        mod_comment.mod.distinguish(how='yes', sticky=True)
                        submission.mod.remove()
                        removed=True
                    elif sum(get_author_points(str(submission.author))) < 3:
                        if post_type == 1 or post_type == 3:
                            mod_comment = submission.reply(author_under_seller)
                            mod_comment.mod.distinguish(how='yes', sticky=True)
                        elif post_type == 2:
                            mod_comment = submission.reply(author_under_buyer)
                            mod_comment.mod.distinguish(how='yes', sticky=True)
                        
                        set_last_post(str(submission.author),
                                      submission, post_type)
                    else:
                        set_last_post(str(submission.author),
                                      submission, post_type)
                    if (removed == False and sum(get_author_points(str(submission.author))) == 0):
                            reddit.redditor(str(submission.author)).message(subject = "Scammers", message = new_user_warning)
                print("Processing " + str(submission.id))
        print("Sleeping stream...")
        time.sleep(15)

    except Exception as e:
        print(e)
        pass

    
