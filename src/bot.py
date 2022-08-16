import csv
from distutils.archive_util import make_archive
from unittest import expectedFailure
import tweepy
import os
import datetime
import time


CK = os.environ.get('API_KEY')
CS = os.environ.get('API_KEY_SECRET')
AT = os.environ.get('ACCESS_TOKEN')
AS = os.environ.get('ACCESS_TOKEN_SECRET')
auth = tweepy.OAuthHandler(CK, CS)
auth.set_access_token(AT, AS)
api = tweepy.API(auth)



class make_csv:
    def __init__(self,filename):
        self.filename=filename
        # csvファイルの作成とヘッダーの書き込み
        with open(self.filename,mode="w",encoding="utf-8") as file:
            writer=csv.writer(file) # writerオブジェクトを作成
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
                ] # ヘッダー
            writer.writerow(header) # ヘッダーを書き込む
    def make(self,tweet):
        # csvファイルの作成とヘッダーの書き込み
        with open(self.filename,mode="a",encoding="utf-8") as file:
            writer=csv.writer(file) # writerオブジェクトを作成

            if 'RT' in tweet.text:
                RT=True
            else:
                RT=False
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
            writer.writerow(body) # を書き込む
def search(api,word,lang):
    now = datetime.datetime.now()
    file_name = 'result_{0}_{1}.csv'.format(word,now.strftime('%Y-%m-%d_%H-%M'))
    mc = make_csv(file_name)
    try:
        tweet_data = api.search(q=word, count=100, lang=lang)
    except tweepy.TweepError as tweeperror:
        print(tweeperror)
    for tweet in tweet_data:
        mc.make(tweet)
    next_max_id = tweet_data[-1].id
    i = 1
    time.sleep(1)
    while True:
        i += 1
        print('検索ページ：' + str(i))
        try:
            tweet_data = api.search(q=word, count=100, max_id=next_max_id-1, lang=lang)
        except tweepy.error.TweepError as tweeperror:
            print(tweeperror)
            time.sleep(60)
            continue
        try:
            next_max_id = tweet_data[-1].id
            post_date = tweet_data[-1].created_at + datetime.timedelta(hours=+9)
        except IndexError as ie:
            print(ie)
            break
        for tweet in tweet_data:
            mc.make(tweet)
        if (post_date - now) > datetime.timedelta(days=7):
            break
        else:
            time.sleep(1)

wordlist=[
    '鬼滅'
    ]
for word in wordlist:
    search(api,word,lang='ja')