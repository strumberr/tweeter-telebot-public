import logging, pytz
import configparser
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import sqlite3
from database import database, create_db, database2
import pandas as pd
import tweepy
import os
import datetime
from time import time, sleep
import random
import asyncio
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from telegram.ext import Updater, MessageHandler, Filters
import time as tm
from telegram.ext import Updater, CommandHandler

con = sqlite3.connect('info_people.db', check_same_thread=False)

cur = con.cursor()
#Import username and password
config = configparser.ConfigParser()
config.read('config.ini')

token = "token"

access_key = 'token'
access_secret = 'token'
consumer_key = 'token'
consumer_secret = 'token'

fileVariable = open('scraped_tweets.csv', 'r+')
fileVariable. truncate(0)
fileVariable. close()

cur = con.cursor()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update, context):

        cur = con.cursor()
        bot = context.bot
        chat_id = update.message.chat_id
        chat_id_int = int(chat_id)
        first_name = update.message.chat.first_name
        last_name = update.message.chat.last_name
        chat_id_column = cur.execute("SELECT chat_id FROM info_people")  # execute a simple SQL select query
        chat_id_column_fetched = chat_id_column.fetchall()

        list1 = []

        for el0 in chat_id_column_fetched:
                el = str(el0)
                el2 = el.replace(",", "")
                el3 = el2.replace("(", "")
                el4 = el3.replace(")", "")
                el5 = int(el4)
                list1.append(el5)

        
        if chat_id_int not in list1:
                print(f"New User added: {chat_id_int, first_name, last_name}")
                bot.sendMessage(chat_id=chat_id_int, text=f"Hello {first_name} and welcome to the tweeter bot, where you can receive daily random tweets! Or ask for a random tweet!")
                database(chat_id_int, first_name, last_name)
        else:
                bot.sendMessage(chat_id=chat_id_int, text=f"{first_name}, you have already sent me start before, there's no need to send it again. \nSend '/tweet' or '/help' instead.")


def help(update, context):
        bot = context.bot
        chat_id = update.message.chat_id
        chat_id_int = int(chat_id)
        first_name = update.message.chat.first_name
        last_name = update.message.chat.last_name
        bot.sendMessage(chat_id=chat_id_int, text=f"So you need my help {first_name}?")
        bot.sendMessage(chat_id=chat_id_int, text=f"""Here you go...
/tweet - For a random tweet, from a random date
/help - For help
/start - To start the bot (A command you use before anything else)
/ctweet [keyword] - Find a random tweet with the keyword
/ctweet #[keyword] - Find a random tweet with the hashtag
/ctweet @[person] - Find a random tweet with the @ of a person
/usernames [number of random usernames] - pulls x amount of random usernames (max 10 at a a time)""")


def tweet(update, context):

    bot = context.bot
    chat_id = update.message.chat_id
    chat_id_int = int(chat_id)
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name
    chat_id_column = cur.execute("SELECT chat_id FROM info_people")  # execute a simple SQL select query
    chat_id_column_fetched = chat_id_column.fetchall()
    chat_id_column_fetched_list = list(chat_id_column_fetched)

    list1 = []

    for el0 in chat_id_column_fetched:
            el = str(el0)
            el2 = el.replace(",", "")
            el3 = el2.replace("(", "")
            el4 = el3.replace(")", "")
            el5 = int(el4)
            list1.append(el5)
    
    if chat_id_int not in list1:
            print(f"New User added: {chat_id_int, first_name, last_name}")
            bot.sendMessage(chat_id=chat_id_int, text=f"Hello {first_name} and welcome to the tweeter bot, where you can receive daily random tweets! Or ask for a random tweet!")
            database(chat_id_int, first_name, last_name)
    else:
            pass

    #------------------------------------------------------------

 
    # Enter your own credentials obtained
    # from your developer account
 
 
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    
    start_date = datetime.date(2022, 1, 1)
    end_date = datetime.date(2022, 12, 30)

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)

    # Enter Hashtag and initial date
    words = "a"
    date_since = random_date

    # number of tweets you want to extract in one run
    numtweet = 1

            # Creating DataFrame using pandas
    db = pd.DataFrame(columns=['username',
                                'description',
                                'location',
                                'following',
                                'followers',
                                'totaltweets',
                                'retweetcount',
                                'text',
                                'hashtags', 
                                'date'])

    # We are using .Cursor() to search
    # through twitter for the required tweets.
    # The number of tweets can be
    # restricted using .items(number of tweets)
    tweets = tweepy.Cursor(api.search_tweets,
                            words, lang="en",
                            until=date_since,
                            tweet_mode='extended').items(numtweet)


    # .Cursor() returns an iterable object. Each item in
    # the iterator has various attributes
    # that you can access to
    # get information about each tweet
    list_tweets = [tweet for tweet in tweets]

    # Counter to maintain Tweet Count
    i = 1

    # we will iterate over each tweet in the
    # list for extracting information about each tweet
    for tweet in list_tweets:
            username = tweet.user.screen_name
            description = tweet.user.description
            location = tweet.user.location
            following = tweet.user.friends_count
            followers = tweet.user.followers_count
            totaltweets = tweet.user.statuses_count
            retweetcount = tweet.retweet_count
            hashtags = tweet.entities['hashtags']

            # Retweets can be distinguished by
            # a retweeted_status attribute,
            # in case it is an invalid reference,
            # except block will be executed
            try:
                    text = tweet.retweeted_status.full_text
            except AttributeError:
                    text = tweet.full_text
            hashtext = list()
            for j in range(0, len(hashtags)):
                    hashtext.append(hashtags[j]['text'])

            # Here we are appending all the
            # extracted information in the DataFrame
            ith_tweet = [username, description,
                            location, following,
                            followers, totaltweets,
                            retweetcount, text, hashtext, date_since]
            db.loc[len(db)] = ith_tweet

            # Function call to print tweet data on screen
            username = f"{ith_tweet[0]} tweeted:"
            tweet_text = ith_tweet[7]
            hashtags = f"Hashtags In Tweet: {ith_tweet[8]}"
            location = f"Location: {ith_tweet[2]}"
            i = i+1
    filename = 'scraped_tweets.csv'

    # we will save our database as a CSV file.
    db.to_csv(filename)

    print('API Worked!', chat_id_int, first_name, last_name)

    #------------------------------------------------------------

    text = (tweet_text + "\n" + location + "\n" + hashtags)
    
    bot.sendMessage(chat_id=chat_id_int, text=username + "\n\n" + text)


def reply(update, context):
        bot = context.bot
        chat_id = update.message.chat_id
        chat_id_int = int(chat_id)
        user_input = update.message.text
        if "/ctweet" in user_input:
                user_input_string = str(user_input)
                user_input_string_replaced = user_input_string.replace("/ctweet", "")
                answer = user_input_string_replaced

                #------------------------------------------------------------

                first_name = update.message.chat.first_name
                last_name = update.message.chat.last_name
                chat_id_column = cur.execute("SELECT chat_id FROM info_people")  # execute a simple SQL select query
                chat_id_column_fetched = chat_id_column.fetchall()
                chat_id_column_fetched_list = list(chat_id_column_fetched)

                list1 = []

                for el0 in chat_id_column_fetched:
                        el = str(el0)
                        el2 = el.replace(",", "")
                        el3 = el2.replace("(", "")
                        el4 = el3.replace(")", "")
                        el5 = int(el4)
                        list1.append(el5)

                        
                if chat_id_int not in list1:
                        print(f"New User added: {chat_id_int, first_name, last_name}")
                        bot.sendMessage(chat_id=chat_id_int, text=f"Hello {first_name} and welcome to the tweeter bot, where you can receive daily random tweets! Or ask for a random tweet!")
                        database(chat_id_int, first_name, last_name)
                else:
                        pass

                #------------------------------------------------------------

                
                # Enter your own credentials obtained
                # from your developer account
                
                
                auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
                auth.set_access_token(access_key, access_secret)
                api = tweepy.API(auth)

                start_date = datetime.date(2022, 1, 1)
                end_date = datetime.date(2022, 12, 30)

                time_between_dates = end_date - start_date
                days_between_dates = time_between_dates.days
                random_number_of_days = random.randrange(days_between_dates)
                random_date = start_date + datetime.timedelta(days=random_number_of_days)

                # Enter Hashtag and initial date
                words = answer
                date_since = random_date

                # number of tweets you want to extract in one run
                numtweet = 1

                        # Creating DataFrame using pandas
                db = pd.DataFrame(columns=['username',
                                                'description',
                                                'location',
                                                'following',
                                                'followers',
                                                'totaltweets',
                                                'retweetcount',
                                                'text',
                                                'hashtags', 
                                                'date'])

                # We are using .Cursor() to search
                # through twitter for the required tweets.
                # The number of tweets can be
                # restricted using .items(number of tweets)
                tweets = tweepy.Cursor(api.search_tweets,
                                        words, lang="en",
                                        until=date_since,
                                        tweet_mode='extended').items(numtweet)


                # .Cursor() returns an iterable object. Each item in
                # the iterator has various attributes
                # that you can access to
                # get information about each tweet
                list_tweets = [tweet for tweet in tweets]

                # Counter to maintain Tweet Count
                i = 1

                # we will iterate over each tweet in the
                # list for extracting information about each tweet
                for tweet in list_tweets:
                        username = tweet.user.screen_name
                        description = tweet.user.description
                        location = tweet.user.location
                        following = tweet.user.friends_count
                        followers = tweet.user.followers_count
                        totaltweets = tweet.user.statuses_count
                        retweetcount = tweet.retweet_count
                        hashtags = tweet.entities['hashtags']

                        # Retweets can be distinguished by
                        # a retweeted_status attribute,
                        # in case it is an invalid reference,
                        # except block will be executed
                        try:
                                text = tweet.retweeted_status.full_text
                        except AttributeError:
                                text = tweet.full_text
                        hashtext = list()
                        for j in range(0, len(hashtags)):
                                hashtext.append(hashtags[j]['text'])

                        # Here we are appending all the
                        # extracted information in the DataFrame
                        ith_tweet = [username, description,
                                        location, following,
                                        followers, totaltweets,
                                        retweetcount, text, hashtext, date_since]
                        db.loc[len(db)] = ith_tweet

                        # Function call to print tweet data on screen
                        username = f"{ith_tweet[0]} tweeted:"
                        tweet_text = ith_tweet[7]
                        hashtags = f"Hashtags In Tweet: {ith_tweet[8]}"
                        location = f"Location: {ith_tweet[2]}"
                        i = i+1
                filename = 'scraped_tweets.csv'

                # we will save our database as a CSV file.
                db.to_csv(filename)

                print('API Worked!', chat_id_int, first_name, last_name)
                
                #------------------------------------------------------------

                text = (tweet_text + "\n" + location + "\n" + hashtags)

                if text == "":
                                bot.sendMessage(chat_id=chat_id_int, text=f"{first_name}, we couldn't find a tweet with the keyword '{user_input_string_replaced}', please try again with a different keyword!")
                
                bot.sendMessage(chat_id=chat_id_int, text=username + "\n\n" + text)

        elif "/usernames" in user_input:
                user_input_string = str(user_input)
                user_input_string_replaced = user_input_string.replace("/usernames", "")
                answer = user_input_string_replaced

                #------------------------------------------------------------

                first_name = update.message.chat.first_name
                last_name = update.message.chat.last_name
                chat_id_column = cur.execute("SELECT chat_id FROM info_people")  # execute a simple SQL select query
                chat_id_column_fetched = chat_id_column.fetchall()
                chat_id_column_fetched_list = list(chat_id_column_fetched)

                list1 = []

                for el0 in chat_id_column_fetched:
                        el = str(el0)
                        el2 = el.replace(",", "")
                        el3 = el2.replace("(", "")
                        el4 = el3.replace(")", "")
                        el5 = int(el4)
                        list1.append(el5)

                if chat_id_int not in list1:
                        print(f"New User added: {chat_id_int, first_name, last_name}")
                        bot.sendMessage(chat_id=chat_id_int, text=f"Hello {first_name} and welcome to the tweeter bot, where you can receive daily random tweets! Or ask for a random tweet!")
                        database(chat_id_int, first_name, last_name)
                else:
                        pass

                #------------------------------------------------------------

                # Enter your own credentials obtained
                # from your developer account
                
                
                auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
                auth.set_access_token(access_key, access_secret)
                api = tweepy.API(auth)

                start_date = datetime.date(2022, 1, 1)
                end_date = datetime.date(2022, 12, 30)

                time_between_dates = end_date - start_date
                days_between_dates = time_between_dates.days
                random_number_of_days = random.randrange(days_between_dates)
                random_date = start_date + datetime.timedelta(days=random_number_of_days)


                # Enter Hashtag and initial date
                words = "a"
                date_since = random_date

                # number of tweets you want to extract in one run
                answer_string = int(answer)
                if answer_string > 10:
                        bot.sendMessage(chat_id=chat_id_int, text="You cant pull more than 10 at a time!")
                else:


                        numtweet = answer_string

                        # Creating DataFrame using pandas
                db = pd.DataFrame(columns=['username',
                                                'description',
                                                'location',
                                                'following',
                                                'followers',
                                                'totaltweets',
                                                'retweetcount',
                                                'text',
                                                'hashtags', 
                                                'date'])

                # We are using .Cursor() to search
                # through twitter for the required tweets.
                # The number of tweets can be
                # restricted using .items(number of tweets)
                tweets = tweepy.Cursor(api.search_tweets,
                                        words, lang="en",
                                        until=date_since,
                                        tweet_mode='extended').items(numtweet)


                # .Cursor() returns an iterable object. Each item in
                # the iterator has various attributes
                # that you can access to
                # get information about each tweet
                list_tweets = [tweet for tweet in tweets]

                # Counter to maintain Tweet Count
                i = 1

                # we will iterate over each tweet in the
                # list for extracting information about each tweet
                for tweet in list_tweets:
                        username = tweet.user.screen_name
                        description = tweet.user.description
                        location = tweet.user.location
                        following = tweet.user.friends_count
                        followers = tweet.user.followers_count
                        totaltweets = tweet.user.statuses_count
                        retweetcount = tweet.retweet_count
                        hashtags = tweet.entities['hashtags']

                        list_usernames = []
                        list_usernames.append(username)
                        print(list_usernames)

                        try:
                                usernames_join = ' '.join(list_usernames)
                                bot.sendMessage(chat_id=chat_id_int, text=usernames_join)
                        except:
                                pass

                        # Retweets can be distinguished by
                        # a retweeted_status attribute,
                        # in case it is an invalid reference,
                        # except block will be executed
                        try:
                                text = tweet.retweeted_status.full_text
                        except AttributeError:
                                text = tweet.full_text
                        hashtext = list()
                        for j in range(0, len(hashtags)):
                                hashtext.append(hashtags[j]['text'])

                        # Here we are appending all the
                        # extracted information in the DataFrame
                        ith_tweet = [username, description,
                                        location, following,
                                        followers, totaltweets,
                                        retweetcount, text, hashtext, date_since]
                        db.loc[len(db)] = ith_tweet

                        # Function call to print tweet data on screen                        username = f"Random Username: {ith_tweet[0]}"
                        tweet_text = ith_tweet[7]
                        hashtags = f"Hashtags In Tweet: {ith_tweet[8]}"
                        location = f"Location: {ith_tweet[2]}"
                        i = i+1
                filename = 'scraped_tweets.csv'

                # we will save otabase as a CSV file.
                db.to_csv(filename)

                print('API Worked!', chat_id_int, first_name, last_name)
                
                #------------------------------------------------------------


                #if text == "":
                #                bot.sendMessage(chat_id=chat_id_int, text=f"{first_name}, we couldn't find a tweet with the keyword '{user_input_string_replaced}', please try again with a different keyword!")
        

def daily_tweet(context: CallbackContext):

        message = "Good Morning! Have a nice day!"

        chat_id_column = cur.execute("SELECT chat_id FROM info_people")  # execute a simple SQL select query
        chat_id_column_fetched = chat_id_column.fetchall()

        list1 = []

        for el0 in chat_id_column_fetched:
                el = str(el0)
                el2 = el.replace(",", "")
                el3 = el2.replace("(", "")
                el4 = el3.replace(")", "")
                el5 = int(el4)
                list1.append(el5)
    
        # send message to all users
        for el in list1:
                id = el
                context.bot.send_message(chat_id=id, text=message)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
        
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token, use_context=True)


    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("tweet", tweet))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, reply))    


    # on noncommand i.e message - echo the message on Telegram

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    updater.idle()
    

if __name__ == '__main__':
    main()
