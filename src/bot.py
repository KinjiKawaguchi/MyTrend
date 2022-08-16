import csv
from distutils.archive_util import make_archive
from unittest import expectedFailure
import tweepy
import os
import datetime
from datetime import datetime,timezone
import pytz

def change_time_JST(u_time):
    #イギリスのtimezoneを設定するために再定義する
    utc_time = datetime(u_time.year, u_time.month,u_time.day, \
    u_time.hour,u_time.minute,u_time.second, tzinfo=timezone.utc)
    #タイムゾーンを日本時刻に変換
    jst_time = utc_time.astimezone(pytz.timezone("Asia/Tokyo"))
    # 文字列で返す
    str_time = jst_time.strftime("%Y-%m-%d_%H:%M:%S")
    return str_time

CK = os.environ.get('API_KEY')
CS = os.environ.get('API_KEY_SECRET')
AT = os.environ.get('ACCESS_TOKEN')
AS = os.environ.get('ACCESS_TOKEN_SECRET')
auth = tweepy.OAuthHandler(CK, CS)
auth.set_access_token(AT, AS)
api = tweepy.API(auth)

# 全ツイートを入れる空のリストを用意
user = "pakkumannoteki"
today = True

all_tweets = []
params = {
    "count": 1,
    "exclude_replies": True,
    "include_rts": False
}
latest_tweet = api.user_timeline(screen_name=user, params = params)
all_tweets.extend(latest_tweet)

print(latest_tweet)
with open('all_tweets.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([
        'tweet_text', 
        'created_at', 
        '#characters', 
        '#favorited', 
        '#retweeted', 
        'hasImage', 
        'hasBlogLink'
        ])
    for tweet in all_tweets:
        if (tweet.text.startswith('RT')) or (tweet.text.startswith('@')):
            continue # RTとリプライはスキップ
        else:
            tweet_time = change_time_JST(tweet.created_at)#ツイート時間を日本時間に変換
            has_image = 0 # 画像付きのツイートか
            has_bloglink = 0 # ブログへのリンク付きのツイートか
            tweet_characters = tweet.text # ツイートの文字列
            if 'media' in tweet.entities:
                has_image = 1
            if len(tweet.entities['urls']) > 0:
                # urlは、文字数としてカウントしない
                tweet_characters = tweet_characters.strip(tweet.entities['urls'][0]['url']).strip()
                if 'nishipy.com' in tweet.entities['urls'][0]['display_url']:
                    has_bloglink = 1
            writer.writerow([tweet.text, tweet_time,len(tweet_characters), tweet.favorite_count, tweet.retweet_count, has_image, has_bloglink])


"""

# 直近の200ツイート分を取得しておく
latest_tweets = api.user_timeline(screen_name=user,count=200,include_rts=False)
all_tweets.extend(latest_tweets)
while len(latest_tweets)>0 and today:
    latest_tweets = api.user_timeline(count=200, max_id=all_tweets[-1].id-1)
    all_tweets.extend(latest_tweets)
print(all_tweets)
"""






"""""
# 取得するツイートがなくなるまで続ける
for i in range(3):
    latest_tweets = api.user_timeline(screen_name="pakkumannoteki",count=200, max_id=all_tweets[-1].id-1)
    all_tweets.extend(latest_tweets)
"""

"""
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
"""