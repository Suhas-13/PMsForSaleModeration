import praw
import regex
import time
from dateutil import parser
from datetime import timezone, datetime

sub = "pmsforsale"
bot_user = "SuperShinyBot"
second_subreddit = "pmsfeedback"
external_subreddit = "coinsales"
title_removal_message = """Your post has automatically been flagged for removal.\n\nIn order for me to work, your post must start with [WTS], [WTB], or [WTT].\n\nPlease delete this post and create another with the proper format."""
faq_message = "Thanks for reaching out to us. The answer to your question can be found here:\n\n\n\n**[FAQ](https://www.reddit.com/r/Pmsforsale/wiki/faq)**\n\n\n\nHere are some more helpful links:\n\n\n\n[rules](https://www.reddit.com/r/Pmsforsale/wiki/rules)\n\n\n\n[middlemen](https://www.reddit.com/r/Pmsforsale/wiki/middlemen)\n\n\n\n[shiny points (flair)](https://www.reddit.com/r/Pmsforsale/wiki/flair)"
mm_message = "Thanks for reaching out to us. The answer to your question can be found here:\n\n\n\n**[MIDDLEMEN](https://www.reddit.com/r/Pmsforsale/wiki/middlemen)**\n\n\n\nHere are some more helpful links:\n\n\n\n[rules](https://www.reddit.com/r/Pmsforsale/wiki/rules)\n\n\n\n[FAQ](https://www.reddit.com/r/Pmsforsale/wiki/faq)\n\n\n\n[shiny points (flair)](https://www.reddit.com/r/Pmsforsale/wiki/flair)"
rules_message = "Thanks for reaching out to us. The answer to your question can be found here:\n\n\n\n**[RULES](https://www.reddit.com/r/Pmsforsale/wiki/rules)**\n\n\n\nHere are some more helpful links:\n\n\n\n[middlemen](https://www.reddit.com/r/Pmsforsale/wiki/middlemen)\n\n\n\n[FAQ](https://www.reddit.com/r/Pmsforsale/wiki/faq)\n\n\n\n[shiny points (flair)](https://www.reddit.com/r/Pmsforsale/wiki/flair)"
flair_message = "Thanks for reaching out to us. The answer to your question can be found here:\n\n\n\n**[SHINY POINTS](https://www.reddit.com/r/Pmsforsale/wiki/flair)**\n\n\n\nHere are some more helpful links:\n\n\n\n[middlemen](https://www.reddit.com/r/Pmsforsale/wiki/middlemen)\n\n\n\n[FAQ](https://www.reddit.com/r/Pmsforsale/wiki/faq)\n\n\n\n[rules](https://www.reddit.com/r/Pmsforsale/wiki/rules)"
with open("PMSComments.txt","a+") as f:
    f.write("")
with open("PMSTransactions.txt","a+") as f:
    f.write("")
with open("PMSMessages.txt","a+") as f:
    f.write("")
with open("PMSModmail.txt","a+") as f:
    f.write("")
with open("exclusion_list.txt","a+") as f:
    f.write("") 

    
reddit = praw.Reddit(client_id='',
                     client_secret='',
                     username=bot_user,
                     password='',
                     user_agent='PreciousMetals moderation bot by u/hacksorskill')

subreddit = reddit.subreddit(sub)


new_user_warning = """###SCAMMERS! PLEASE READ!
\n\n\n\n/r/PMsForSale has had an influx of scammers lately, that are specifically targeting new members, like yourself.
\n\n\n\n[Please check out the list of recently banned users to see what their techniques are.](https://www.reddit.com/r/Pmsforsale/wiki/banned)
\n\n\n\nHere are a few things to do before doing a deal with a user:
\n\n\n\n1. They have to comment on your post before a deal is done. If they can’t, that means they’re banned. It also shows their flair to give you an idea of how many transactions they’ve done. If it is “S: 0|B: 0”, **BEWARE**
\n\n\n\n2. Search their name on /r/pmsfeedback - if nothing comes back, **BEWARE**
\n\n\n\n3. If they have few flair, or few feedback and want you to ship first or pay first, **BEWARE**
\n\n\n\nIf you’re new, and they’re newish, USE A MIDDLEMAN. [You can read about that here.](https://www.reddit.com/r/Pmsforsale/wiki/middlemen)
\n\n\n\nCommon scam techniques:
\n\n\n\nThey ask for ½ up front, and ½ after you receive goods.
\n\n\n\nThey say they are a user on another forum.
\n\n\n\nThey give you their number to text them to build trust.
\n\n\n\nPrice that seems too good to be true.
\n\n\n\n[PLEASE REPORT ANY OF THIS TO THE MODS](https://www.reddit.com/message/compose/?to=/r/Pmsforsale)
\n\n\n\nThank you, and welcome!"""
author_under_message = """Please note that this seller has less than 10 seller points, therefore they must follow the following rules:
\n\n1.) All negotiating must be done in the comment section. Once the buyer and seller have accepted the terms of the deal, only then are they free to PM each other their PayPal, and their shipping address.
\n\n2.) This seller can only accept PayPal G&S as their payment option. The only way around this is if they ship first to **established** buyers, or if they use a trusted middleman."""
author_under_buyer = """Hello, and welcome to /r/pmsforsale!
\n\nIt appears you’re new to the sub, so I’m here to help you out.
\n\nIf you haven’t already, please [check out the rules of the sub for buying and selling.](https://www.reddit.com/r/Pmsforsale/about/rules/)
\n\nAlthough this isn’t required, you may want to add a couple things to your post if they’re not already there. First, sellers like to know how much you’re looking to pay for items. Second, you may want to include how you’re going to pay (PayPal, Venmo, crypto, etc).
\n\nIf you have any questions, please feel free to message the mods [here.](https://www.reddit.com/message/compose?to=%2Fr%2FPmsforsale)
\n\nThank you, and welcome!"""
author_under_seller = """Hello, and welcome to /r/pmsforsale!
\n\nIt appears you’re new to the sub, so I’m here to help you out.
\n\nFirst, if you haven’t already, please [check out the rules of the sub for buying and selling.](https://www.reddit.com/r/Pmsforsale/about/rules/)
\n\nSecond, although it isn’t a rule, new sellers and traders usually ship first to **established** members, or they use a middleman. Then after receipt of the items, they’re then paid. I want to stress the importance of established members only. Find out more about middlemen [here](https://www.reddit.com/r/Pmsforsale/wiki/middlemen).
\n\nIf you would be willing to do this, I suggest editing your post to let everyone know.
\n\nIf you have any questions, please feel free to message the mods [here.](https://www.reddit.com/message/compose?to=%2Fr%2FPmsforsale)
\n\nThank you, and welcome!"""

post_no_proof_picture = """Oops! It appears your post is missing the proof picture that both a [WTS] and [WTT] post requires.
\n\nA proof picture is one picture with everything you have for sale or trade with a handwritten note with your username and today’s date included in the photo.
\n\n**Please delete this post and create another with the required proof picture.**"""

buy_triggered_early = """Oops! It appears you’ve tried to trigger me too soon. 
\n\nI’m not to be called until **AFTER** the buyer receives their items, and is happy with their purchase.
\n\nIf you believe there was an error, please [message the mods.](https://www.reddit.com/message/compose?to=%2Fr%2FPmsforsale)"""

trade_complete_message = """Congratulations on completing a deal on /r/pmsforsale!
\n\n**If you have already left feedback for this transaction, please ignore this message.**
\n\nPlease leave feedback for /u/{other_author} by clicking on one of the following:
\n\n{positive_link}  -  {neutral_link}  -  {negative_link}
\n\nThe title is already filled out for you, so you just have to fill out the body and hit “submit”.
\n\nTo opt out of future messages, click [here](https://old.reddit.com/message/compose?to=supershinybot&subject=!optout&message=!optout).
\n\nTo message the mods, click [here](https://www.reddit.com/message/compose?to=%2Fr%2FPmsforsale).
\n\nThank you for contributing to the community!"""
bot_trade_message = """Surely you weren’t able to negotiate a deal with a bot....
\n\n\n\nIf you’re having issues figure out how I work, you can read about flair [here](https://www.reddit.com/r/Pmsforsale/wiki/flair).
\n\n\n\nIf you’re still confused, message the mods [here](https://www.reddit.com/message/compose/?to=/r/Pmsforsale)."""
with open("PMSBot.txt", "a+") as f:
    f.write("")


def get_post_type(title):
    if title[0:5].lower() == "[wts]":
        return 1
    elif title[0:5].lower() == "[wtb]":
        return 2
    elif title[0:5].lower() == "[wtt]":
        return 3
    else:
        return -1


def get_author_points(author):
    points = next(subreddit.flair(str(author)))["flair_text"]
    if points is None or len(points) == 0:
        return [0, 0]
    else:
        return [int(points.split(" | ")[0].split(" ")[1]), int(points.split(" | ")[1].split(" ")[1])]


def check_is_author(author, comment):
    if str(comment.submission.author).lower() == str(author).lower():
        return True
    else:
        return False


def get_css_class(points):
    if sum(points) < 10:
        return "red"
    elif sum(points) < 100:
        return "silver"
    else:
        return "gold"

def get_flair_template(points):
    if sum(points) < 10:
        return "4b112a0c-0e8b-11eb-8343-0e74d4d52571"
    elif sum(points) < 100:
        return "641702e2-0e8b-11eb-971d-0ee08778aead"
    else:
        return "7caa2ff0-0e8b-11eb-81ab-0eca8937252b"

def add_sale(user):
    points = get_author_points(user)
    points[0] += 1
    new_flair = "S: " + str(points[0]) + " | B: " + str(points[1])
    #css_class = get_css_class(points)
    flair_template = get_flair_template(points)
    subreddit.flair.set(user, new_flair, flair_template_id=flair_template)


def add_purchase(user):
    points = get_author_points(user)
    points[1] += 1
    new_flair = "S: " + str(points[0]) + " | B: " + str(points[1])
    #css_class = get_css_class(points)
    flair_template = get_flair_template(points)
    subreddit.flair.set(user, new_flair, flair_template_id=flair_template)


def make_transaction(user1, user2, title):
    if user1.lower() == user2.lower():
        return False
    if get_post_type(title) == 1:
        add_sale(user1)
        add_purchase(user2)
    elif get_post_type(title) == 2:
        add_purchase(user1)
        add_sale(user2)
    elif get_post_type(title) == 3:
        add_sale(user1)
        add_sale(user2)
    return True


def image_found(text):
    results = regex.findall('(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+', text)
    if len(results) == 0:
        return False
    flag = False
    for result in results:
        if "reddit" not in result.lower() and len(result) >= 10:
            flag = True
            break
    return flag

def send_feedback_message(target_user, other_user, post_type, role):
    other_user=str(other_user)
    target_user=str(target_user)
    if post_type == 3:
        positive_post_link = "[POSITIVE](https://www.reddit.com/r/pmsfeedback/submit?title=[POSITIVE]%20for%20/u/" + other_user + "%20[trade])"
        neutral_post_link = "[NEUTRAL](https://www.reddit.com/r/pmsfeedback/submit?title=[NEUTRAL]%20for%20/u/" + other_user + "%20[trade])"
        negative_post_link = "[NEGATIVE](https://www.reddit.com/r/pmsfeedback/submit?title=[NEGATIVE]%20for%20/u/" + other_user + "%20[trade])"
    elif post_type == 2:
        if role == 1:
            positive_post_link = "[POSITIVE](https://www.reddit.com/r/pmsfeedback/submit?title=[POSITIVE]%20for%20/u/" + other_user + "%20[seller])"
            neutral_post_link = "[NEUTRAL](https://www.reddit.com/r/pmsfeedback/submit?title=[NEUTRAL]%20for%20/u/" + other_user + "%20[seller])"
            negative_post_link = "[NEGATIVE](https://www.reddit.com/r/pmsfeedback/submit?title=[NEGATIVE]%20for%20/u/" + other_user + "%20[seller])"
        else:
            positive_post_link = "[POSITIVE](https://www.reddit.com/r/pmsfeedback/submit?title=[POSITIVE]%20for%20/u/" + other_user + "%20[buyer])"
            neutral_post_link = "[NEUTRAL](https://www.reddit.com/r/pmsfeedback/submit?title=[NEUTRAL]%20for%20/u/" + other_user + "%20[buyer])"
            negative_post_link = "[NEGATIVE](https://www.reddit.com/r/pmsfeedback/submit?title=[NEGATIVE]%20for%20/u/" + other_user + "%20[buyer])"
    elif post_type == 1:
        if role == 1:
            positive_post_link = "[POSITIVE](https://www.reddit.com/r/pmsfeedback/submit?title=[POSITIVE]%20for%20/u/" + other_user + "%20[buyer])"
            neutral_post_link = "[NEUTRAL](https://www.reddit.com/r/pmsfeedback/submit?title=[NEUTRAL]%20for%20/u/" + other_user + "%20[buyer])"
            negative_post_link = "[NEGATIVE](https://www.reddit.com/r/pmsfeedback/submit?title=[NEGATIVE]%20for%20/u/" + other_user + "%20[buyer])"
        else:
            positive_post_link = "[POSITIVE](https://www.reddit.com/r/pmsfeedback/submit?title=[POSITIVE]%20for%20/u/" + other_user + "%20[seller])"
            neutral_post_link = "[NEUTRAL](https://www.reddit.com/r/pmsfeedback/submit?title=[NEUTRAL]%20for%20/u/" + other_user + "%20[seller])"
            negative_post_link = "[NEGATIVE](https://www.reddit.com/r/pmsfeedback/submit?title=[NEGATIVE]%20for%20/u/" + other_user + "%20[seller])"
    current_message = trade_complete_message.format(other_author=other_user, positive_link = positive_post_link, neutral_link = neutral_post_link, negative_link = negative_post_link)
    reddit.redditor(target_user).message(subject = "Leave Feedback", message = current_message)

def opt_out(author):
    exclusion_list = open("exclusion_list.txt","r").read().split(" ")
    with open("exclusion_list.txt","a+") as f:
        if (str(author) not in exclusion_list):
            f.write(str(author) + " ")
def opt_in(author):
    with open("exclusion_list.txt","r") as f:
        exclusion_text = f.read()
        exclusion_list = exclusion_text.split(" ")
        while str(author) in exclusion_list: 
            exclusion_list.pop(exclusion_list.index(str(author)))
        with open("exclusion_list.txt","w+") as f:
            f.write(" ".join(exclusion_list))
       
def add_ban(target_user, post_url, ban_post_id):
    ban_post = reddit.submission(ban_post_id)
    append_line = "/u/" + target_user + " - [link to ban](" + post_url + ")"
    if ("/u/" + target_user) in ban_post.selftext:
        start_line = ban_post.selftext.find("/u/" + target_user)
        end_line = ban_post.selftext[start_line:].find("\n\n\n\n")
        if end_line == -1:
            end_line = len(ban_post.selftext) - 1
        else:
            end_line += start_line
        ban_post.edit(body = ban_post.selftext[0:start_line] + ban_post.selftext[end_line + 4:] + "\n\n\n\n" + append_line)
    else:
        ban_post.edit(body = ban_post.selftext + "\n\n\n\n" + append_line)

def is_ignored_post(modmail):
    for message in modmail.messages:
        if message.body_markdown.lower().startswith("!ignore"):
            modmail.reply("This modmail thread is no longer accepting new commands as !ignore has been used.")
            return True
    return False

def find_previous_post(modmail):
    try:
        for message in reversed(modmail.messages):
            if message.author.name.lower() == bot_user.lower() and "Feedback post created" in message.body_markdown:
                post_id = message.body_markdown.split("Feedback post created [here]")[1].replace("(", "").replace(")", "").split("/comments/")[1].split("/")[0]
                return post_id, message
    except Exception as e:
        print(e)
        return None 
    return None

def quoteify(text):
    return '>' + text.replace("\n\n","\n\n>") + '\n\n&#x200B;'

def modmail_not_older_than(modmail, days):
    if len(modmail.messages) < 1:
        return False
    date = parser.parse(modmail.messages[0].date)
    days_passed = (time.time() - date.timestamp()) / (3600 * 24)
    return days_passed < days