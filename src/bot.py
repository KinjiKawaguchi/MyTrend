import csv
import tweepy
import os
import csv
import datetime

CK = os.environ.get('API_KEY')
CS = os.environ.get('API_KEY_SECRET')
AT = os.environ.get('ACCESS_TOKEN')
AS = os.environ.get('ACCESS_TOKEN_SECRET')
print(CK,CK,AT,AS)
auth = tweepy.OAuthHandler(CK, CS)
auth.set_access_token(AT, AS)
api = tweepy.API(auth)

class mkcsv:
    def __init__(self,filename):
        self.finename = filename
        with open(self.filename,mode='w',encoding="utf-8") as file:
            writer = csv.writer(file)
            header=[
                "RT",
                "text",
                "tweet_id",
                "post_date",
                "retweet",
                "favorite",
                "user",
                "screen_name",
                "reply_id",
                "language"
            ]
            writer.writerow(header)
            
    def mk(self,tweet):
        with open(self.filename,mode='a',encoding="utf-8") as file:
            writer = csv.writer(file)
            if 'RT' in tweet.text:
                RT = True
            else:
                RT = False
            text = str(tweet.text).replace('\n','')
            if text.find(','):
                text.replace(',','，')

            body=[
                RT,
                text,
                tweet.id,
                tweet.created_at + datetime.timedelta(hours=+9),
                tweet.retweet_count,
                tweet.favorite_count,
                tweet.user.name,
                tweet.user.screen_name,
                tweet.in_reply_to_status_id,
                tweet.lang
            ]
            writer.writerow(body)