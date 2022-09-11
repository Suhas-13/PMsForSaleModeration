from helper import *
with open("PMSComments.txt","a+") as f:
    f.write(" ")
with open("PMSTransactions.txt","a+") as f:
    f.write(" ")
with open("exclusion_list.txt","a+") as f:
    f.write("  ") 
while True:
    try:
        for comment in subreddit.stream.comments():
            if comment is None:
                break
            elif comment.created_utc < time.time()-400:
                pass
            elif comment.id not in open("PMSComments.txt").read():
                with open("PMSComments.txt", "a+") as f:
                    f.write(" " + comment.id)
                if "trade completed!" == comment.body.lower().strip() and check_is_author(str(comment.author), comment) == True:
                    if str(comment.parent().author) == "supershinybot" or str(comment.parent().author) == "automoderator":
                        comment.reply(bot_trade_message)
                    elif time.time()-comment.submission.created_utc < 86400:
                        mod_comment = comment.reply(buy_triggered_early)
                        mod_comment.mod.distinguish(how='yes')
                    elif comment.is_root == False and make_transaction(str(comment.author), str(comment.parent().author), comment.submission.title):
                        mod_comment = comment.reply("Trade successfully completed between /u/" + str(
                            comment.author) + " and /u/" + str(comment.parent().author) + ".")
                        mod_comment.mod.distinguish(how='yes', sticky=True)
                        if (sum(get_author_points(str(comment.author))) <= 20 and sum(get_author_points(str(comment.parent().author))) <= 20):
                            if str(comment.submission.id)+"-" +str(comment.author)+":"+str(comment.parent().author) in open("PMSTransactions.txt","r").read() or (str(comment.submission.id)+"-" +str(comment.parent().author)+":"+str(comment.author)) in open("PMSTransactions.txt","r").read():
                                reddit.redditor("Cancer-Cheater").message(subject = "POSSIBLE CONFIRM ABUSE u/" + str(comment.author), message = str(comment.permalink))
                            if open("PMSTransactions.txt","r").read().count(str(comment.submission.id)) >= 4:
                                reddit.redditor("Cancer-Cheater").message(subject = "POSSIBLE CONFIRM ABUSE u/" + str(comment.author), message = str(comment.permalink))
                                print("Detected 5 in same post")
                            with open("PMSTransactions.txt","a+") as f:
                                f.write(str(comment.submission.id)+"-" + str(comment.author) +":"+str(comment.parent().author) +"\n")
                        print("Transaction between /u/" + str(comment.author) +
                                " and /u/" + str(comment.parent().author))
                        if (str(comment.author) not in open("exclusion_list.txt").read()):
                            send_feedback_message(comment.author, comment.parent().author, get_post_type(comment.submission.title), 1)
                        if (str(comment.parent().author) not in open("exclusion_list.txt").read()):
                            send_feedback_message(comment.parent().author, comment.author, get_post_type(comment.submission.title), 2)          
                    else:
                        mod_comment = comment.reply(
                            "An error occured\n\nPlease ensure that the OP of this post is the one confirming the transaction, also please ensure that the OP is replying to a comment made by the user they transacted with.\n\n\n\nIf you believe the bot is experiencing an issue, modmail us [here](https://www.reddit.com/message/compose?to=r/Pmsforsale&subject=BOT%20ISSUES)")
                        mod_comment.mod.distinguish(how='yes', sticky=True)
                        print("An error occured")   
                elif "!mm" == comment.body.lower().strip() or "!middlemen" == comment.body.lower().strip() or "!middleman" == comment.body.lower().strip():
                    comment=comment.reply("[Find out about middlemen!](https://www.reddit.com/r/Pmsforsale/wiki/middlemen)")
                    comment.mod.distinguish(how='yes', sticky=True)
                elif "!rules" == comment.body.lower().strip():
                    comment=comment.reply("[Here’s a link to the rules!](https://www.reddit.com/r/Pmsforsale/about/rules/)")
                    comment.mod.distinguish(how='yes', sticky=True)
                elif "!practices" == comment.body.lower().strip():
                    comment=comment.reply("[Here’s our recommended practices!](https://www.reddit.com/r/Pmsforsale/wiki/practices)")
                    comment.mod.distinguish(how='yes', sticky=True)
                elif "!banned" == comment.body.lower().strip():
                    comment=comment.reply("[Here’s the list of banned users!](https://www.reddit.com/r/Pmsforsale/wiki/banned)")
                    comment.mod.distinguish(how='yes', sticky=True)
                elif "!feedback" == comment.body.lower().strip() and comment.parent().name[0:1] != "t3":
                    comment=comment.reply("[Here’s](https://www.reddit.com/r/pmsfeedback/search?q=%22" + str(comment.parent().author) + "%22&restrict_sr=on&sort=new&t=all) a list of the feedback for /u/" + str(comment.parent().author))
                    comment.mod.distinguish(how='yes', sticky=True)
                elif "!commands" == comment.body.lower().strip():
                    comment=comment.reply("[Here's a list of commands](https://www.reddit.com/r/Pmsforsale/wiki/commands)")
                    comment.mod.distinguish(how='yes', sticky=True)
                elif "!flair" == comment.body.lower().strip():
                    comment=comment.reply("[Here's some information on flairs](https://www.reddit.com/r/Pmsforsale/wiki/flair)")
    except Exception as e:
        print(e)
        pass