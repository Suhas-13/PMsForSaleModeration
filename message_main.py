from helper import *
import time
import sys
from itertools import chain
from datetime import datetime
import os
import pytz
import json
try:
    pending_posts = json.load(open("pending_posts.json"))
except Exception as e:
    with open("pending_posts.json", "a+") as f:
        f.write("{}")
HOURS_IN_DAY = 24
SECONDS_PER_HOUR = 3600
CURRENT_BAN_ID = "vl7eer"
CURRENT_BAN_POST = reddit.submission(CURRENT_BAN_ID)
EST = pytz.timezone('US/Eastern')

while True:
    try:
        for message in reddit.inbox.unread(limit=None):
            if message is None:
                pass
            elif message.created_utc < time.time() - 150:
                pass
            elif message.fullname[0:2] != "t4":
                pass
            elif message.id not in open("PMSMessages.txt").read():
                with open("PMSMessages.txt", "a+") as f:
                    f.write(" " + message.id)
                reddit.inbox.mark_read([message])
                if (str(message.subject).lower() == "!optout"):
                    opt_out(str(message.author))
                    message.reply(
                        body="Opted out succesfully!\n\nTo opt back in, click [here](https://old.reddit.com/message/compose?to=supershinybot&subject=!optin&message=!optin)")
                elif (str(message.subject).lower() == "!optin"):
                    opt_in(str(message.author))
                    message.reply(body="Opted in succesfully!")
                elif str(message.body).startswith("!time") or str(message.body).startswith("!yes") or str(message.body).startswith("!no"):
                    parent_message = message
                    while parent_message.parent:
                        parent_message = parent_message.parent
                    if "has been permanently banned from /r/pmsforsale" in parent_message.subject and parent_message.author.name.lower() == bot_user.lower():
                        target_user = str(parent_message.subject).split(" ")[
                            0].split("u/")[1]
                        if target_user in pending_posts:
                            if time.time() > float(pending_posts[target_user]['post_time']):
                                message.reply(
                                    body="Unfortunately the time limit on this post has expired.")
                            elif str(message.body).startswith("!time"):
                                if not pending_posts[target_user]['extendable']:
                                    if pending_posts[target_user]['extended']:
                                        message.reply(
                                            body="Unfortunately this decision cannot be extended again.")
                                    else:
                                        message.reply(
                                            body="Unfortunately since this scammer is active in the /r/pmsforsale community, we aren't able to extend this decision an extra 24 hours.")
                                else:
                                    message.reply(
                                        body="You'll have an additional 24 hours to make a decision on whether /r/coinsales would like to be added to the /r/pmsfeedback post for the permanent ban of /u/" + target_user + "\n\n\n\n" +
                                        "/r/coinsales has until " + datetime.fromtimestamp(float(pending_posts[target_user]['post_time'])).astimezone(EST).strftime("%b %-d, %Y at %H:%M %p") + " EST to make this decision. If no decision is made, the post will be made in /r/pmsfeedback without including /r/coinsales.")
                                    pending_posts[target_user]['post_time'] = float(
                                        pending_posts[target_user]['post_time']) + (HOURS_IN_DAY * SECONDS_PER_HOUR)
                                    pending_posts[target_user]['extendable'] = False
                                    pending_posts[target_user]['extended'] = True
                                    with open('pending_posts.json', 'w+') as f:
                                        json.dump(pending_posts, f)
                            elif str(message.body).startswith("!yes"):
                                post = reddit.subreddit(second_subreddit).submit(title="/u/" + target_user + " has permanently been banned from /r/pmsforsale and /r/coinsales.",
                                                                                 selftext="/u/" + target_user + " has permanently been banned from /r/pmsforsale and /r/coinsales." + "\n\n\n\nReason: " + pending_posts[target_user]['reason'])
                                message.reply(
                                    body="Feedback post on /r/pmsfeedback created [successfully.](" + post.url + ")")
                                add_ban(target_user, post.url,
                                        CURRENT_BAN_POST.id)
                                subreddit.modmail(pending_posts[target_user]['id']).reply(
                                    body="Feedback post created [here](" + post.url + ").")
                                del(pending_posts[target_user])
                                with open('pending_posts.json', 'w+') as f:
                                    json.dump(pending_posts, f)
                            elif str(message.body.startswith("!no")):
                                post = reddit.subreddit(second_subreddit).submit(title="/u/" + target_user + " has permanently been banned from /r/pmsforsale.",
                                                                                 selftext="/u/" + target_user + " has permanently been banned from /r/pmsforsale." + "\n\n\n\nReason: " + pending_posts[target_user]['reason'])
                                message.reply(
                                    body="Feedback post on /r/pmsfeedback created [successfully.](" + post.url + ")")
                                add_ban(target_user, post.url,
                                        CURRENT_BAN_POST.id)
                                subreddit.modmail(pending_posts[target_user]['id']).reply(
                                    body="Feedback post created [here](" + post.url + ").")
                                del(pending_posts[target_user])
                                with open('pending_posts.json', 'w+') as f:
                                    json.dump(pending_posts, f)
                        else:
                            message.reply(
                                body="An error occured.\n\n\n\nThis may be because the post was already created on r/pmsfeedback.\n\n\n\nPlease contact r/pmsforsale.")

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(e)
        print(exc_type, fname, exc_tb.tb_lineno)
    try:
        modmail_threads = chain(subreddit.modmail.conversations(
            state="all"), subreddit.modmail.conversations(state="mod"))
        for modmail in modmail_threads:
            if modmail.messages[0].id not in open("PMSModmail.txt").read() and modmail.num_messages > 1 and modmail.messages[0].author.name.lower() != bot_user.lower() and modmail_not_older_than(modmail, 5):
                with open("PMSModmail.txt", "a+") as f:
                    f.write(
                        " " + modmail.messages[0].id)
                modmail.read()
                current_message = modmail.messages[0]
                modmail = subreddit.modmail(modmail.id)
                first_message = modmail.messages[0]
                if "!faq" in current_message.body_markdown.lower() and current_message.is_internal:
                    modmail.reply(body=faq_message, author_hidden=True)
                elif "!rules" in current_message.body_markdown.lower() and current_message.is_internal:
                    modmail.reply(body=rules_message, author_hidden=True)
                elif "!mm" in current_message.body_markdown.lower() and current_message.is_internal:
                    modmail.reply(body=mm_message, author_hidden=True)
                elif "!flair" in current_message.body_markdown.lower() and current_message.is_internal:
                    modmail.reply(body=flair_message, author_hidden=True)
                elif is_ignored_post(modmail):
                    pass
                elif first_message.author.name.lower() == bot_user.lower() and "has been permanently banned" in modmail.subject:
                    if current_message.body_markdown.startswith("!reason"):
                        previous_post = find_previous_post(modmail)
                        if not previous_post or reddit.submission(previous_post[0]).selftext == "[deleted]":
                            modmail.reply(
                                body="Do you want to notify /r/coinsales?\n\nPlease respond with !yes or !no.", author_hidden=True)
                        else:
                            modmail.reply(
                                "A post already exists. Use !edit to modify it, or !delete to remove it and create a new post.")
                    elif current_message.body_markdown.startswith("!no") or current_message.body_markdown.startswith("!yes"):
                        reason_body = None
                        target_user = None
                        for message in reversed(modmail.messages):
                            if message.body_markdown.startswith("!reason"):
                                reason_body = message.body_markdown.split("!reason ")[
                                    1]
                                if "u/" in modmail.subject.split(" ")[0]:
                                    target_user = modmail.subject.split(
                                        " ")[0].split("u/")[1]
                                break
                        if reason_body is None:
                            modmail.reply(
                                body="Ban reason has not been set. Please use !reason to set the reason.")
                        elif target_user is None:
                            modmail.reply(
                                body="The command is being used in the wrong modmail thread.")
                        else:
                            if current_message.body_markdown.startswith("!no"):
                                sticky_post = reddit.subreddit(second_subreddit).submit(title="/u/" + target_user + " has permanently been banned from /r/pmsforsale.",
                                                                                        selftext="/u/" + target_user + " has permanently been banned from /r/pmsforsale." + "\n\n\n\nReason: " + reason_body)
                                sticky_post.mod.distinguish(how="yes")
                                sticky_post.mod.lock()
                                modmail.reply(
                                    body="Feedback post created [here](" + sticky_post.url + ").")
                                add_ban(target_user, sticky_post.url,
                                        CURRENT_BAN_POST.id)
                            elif current_message.body_markdown.startswith("!yes"):
                                mod_note = next(
                                    subreddit.mod.notes.redditors(target_user)).note
                                if mod_note and "#scammer" in mod_note:
                                    extendable = False
                                    time_body = "/r/coinsales has 24 hours to respond to this message before the banned post will be automatically created in /r/pmsfeedback. No response will indicate that /r/coinsales would not like to be included."
                                else:
                                    extendable = True
                                    time_body = "/r/coinsales has 24 hours to respond to this message before the banned post will be automatically created in /r/pmsfeedback. No response will indicate that /r/coinsales would not like to be included.\n\n\n\nIf you would like to extend this to 48 hours to have a discussion, please respond with '!time'."
                                pending_posts[target_user] = {'id': modmail.id, 'post_time': time.time(
                                ) + (HOURS_IN_DAY * SECONDS_PER_HOUR), 'reason': reason_body, 'extendable': extendable, 'extended': False}
                                with open('pending_posts.json', 'w+') as f:
                                    json.dump(pending_posts, f)
                                reddit.redditor("r/" + external_subreddit).message(subject="u/" + target_user + " has been permanently banned from /r/pmsforsale.", message="u/" + target_user + " has been permanently banned from /r/pmsforsale.\n\n\n\nThe reason that will be posted in /r/pmsfeedback will be:\n\n\n\n" + quoteify(reason_body) + "\n\n\n\n" +
                                                                                   "Are you going to permanently ban them from /r/coinsales, and would you like /r/coinsales to be included in the banned post to the community?\n\n\n\nPlease respond to this message with '!yes' or '!no'\n\n\n\nIf you'd like to discuss this with the mods of /r/pmsforsale, please message them [here.](https://www.reddit.com/message/compose/?to=/r/Pmsforsale)\n\n\n\n" + time_body)
                                modmail.reply(
                                    body="Message sent to /r/coinsales. If there is no reply, the post will automatically be created in 24 hours.")
                    elif current_message.body_markdown.startswith("!delete"):
                        post_id, previous_message = find_previous_post(modmail)
                        if not post_id:
                            modmail.reply(
                                body="An error occured. The post to remove could not be found.")
                        else:
                            post = reddit.submission(post_id)
                            if post and post.selftext != "[deleted]":
                                reddit.submission(post_id).delete()
                                modmail.reply(
                                    body="Post removed. Please enter a new reason.")
                            else:
                                modmail.reply(
                                    body="No post currently exists. You can create one using !reason [REASON]")
                    elif current_message.body_markdown.startswith("!edit"):
                        post_id, previous_message = find_previous_post(modmail)
                        if not post_id:
                            modmail.reply(
                                body="An error occured. The post to edit could not be found.")
                        else:
                            try:
                                new_body = current_message.body_markdown.split("!edit ")[
                                    1]
                                post = reddit.submission(post_id)
                                if not post or post.selftext == "[deleted]":
                                    modmail.reply(
                                        body="No post currently exists. You can create one using !reason [REASON]")
                                else:
                                    target_user = post.title.split(
                                        "/u/")[1].split(" ")[0]
                                    post.edit(body=post.selftext.split("\n\n")[
                                              0] + "\n\n\n\nReason: " + new_body)
                                    modmail.reply(body="Post edited.")
                            except Exception as e:
                                print(e)
                                modmail.reply(
                                    body="An error occured. Please provide a new reason as follows '!edit [REASON]'")

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(e)
        print(exc_type, fname, exc_tb.tb_lineno)

    try:
        for target_user in list(pending_posts.keys()):
            if float(pending_posts[target_user]['post_time']) < time.time():
                post = reddit.subreddit(second_subreddit).submit(title="/u/" + target_user + " has permanently been banned from /r/pmsforsale.",
                                                                 selftext="/u/" + target_user + " has permanently been banned from /r/pmsforsale." + "\n\n\n\nReason: " + pending_posts[target_user]['reason'])
                subreddit.modmail(pending_posts[target_user]['id']).reply(
                    body="Feedback post created [here](" + post.url + ").")
                add_ban(target_user, post.url,
                        CURRENT_BAN_POST.id)
                del(pending_posts[target_user])
                with open('pending_posts.json', 'w+') as f:
                    json.dump(pending_posts, f)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(e)
        print(exc_type, fname, exc_tb.tb_lineno)
