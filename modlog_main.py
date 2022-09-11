import praw
import time
from helper import *
with open("PMSLog.txt", "a+") as f:
    f.write(" ")
while True:
    try:
        for log in subreddit.mod.stream.log():
            if log.created_utc < time.time()-550:
                pass
            elif log.id in open("PMSLog.txt").read():
                pass
            elif str(log.mod).lower() == "uslbot":
                pass
            elif log.action == "banuser":
                with open("PMSLog.txt", "a+") as f:
                    f.write(" " + log.id)
                print("Processing " + log.id)
                description = log.description
                target_author = log.target_author
                ban_length = log.details
                if "permanent" in ban_length:
                    reddit.subreddit(second_subreddit).banned.add(
                        target_author, note=description)
                    reddit.redditor("r/" + sub).message(subject = "u/" + target_author + " has been permanently banned.",
                                                        message = "You all have permanently banned u/" + target_author + " from /r/pmsforsale. Please reply to this message with the reason, using the following format:\n\n\n\n!reason include reason here\n\n\n\nExamples:\n\n\n\n!reason scammer\n\n\n\n!reason Inadequate packaging")
                """
                else:
                    reason_list = ban_length.split(" ")
                    days = -1
                    for i in range(len(reason_list)):
                        if reason_list[i] == "days":
                            days = int(reason_list[i-1])
                            break
                    if days == -1:
                        print("error with " + log.id)
                    else:
                        reddit.subreddit(second_subreddit).banned.add(target_author, duration = days, note = description)
                """
            elif log.action == "unbanuser":
                with open("PMSLog.txt", "a+") as f:
                    f.write(" " + log.id)
                print("Processing " + log.id)
                reddit.subreddit(second_subreddit).banned.remove(
                    log.target_author)

        time.sleep(20)

    except Exception as e:
        print(e)
        pass
