import csv
import tweepy
import os
import datetime
from datetime import datetime,timezone,timedelta
import pytz

CK = os.environ.get('API_KEY')
CS = os.environ.get('API_KEY_SECRET')
AT = os.environ.get('ACCESS_TOKEN')
AS = os.environ.get('ACCESS_TOKEN_SECRET')
auth = tweepy.OAuthHandler(CK, CS)
auth.set_access_token(AT, AS)
api = tweepy.API(auth)

current_time = datetime.now(timezone.utc)
#ツイート取得時の引数指定
user = "pakkumannoteki"
params = {
    "count": 1,
    "exclude_replies": True,
    "include_rts": False
}
# 全ツイートを入れる空のリストを用意
all_tweets = []
flag = True
flag2 = True
#過去24時間のツイートの情報を配列に格納(非効率なので改善の余地あり)
while True:
    array = []
    if flag:
        array.extend(api.user_timeline(screen_name = user, params = params))
        flag = False
    else:
        array.extend(api.user_timeline(screen_name = user, params = params, max_id=all_tweets[-1].id-1))
    latest_tweet = array[0]
    tweet_time = latest_tweet.created_at
    #ツイートが過去24時間に行われたか?
    if not (current_time + timedelta(days=-1) < tweet_time):
        break
    if flag2:
        all_tweets.extend(api.user_timeline(screen_name = user, params = params))
        flag2 = False
    else:
        all_tweets.extend(api.user_timeline(screen_name = user, params = params, max_id=all_tweets[-1].id-1))
if(len(all_tweets)==0):
    print("過去24時間で行われたツイートはありませんでした。")


#過去24時間にされたツイートについてCSVファイルに出力
with open('all_tweets.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([
        'tweet_text', 
        'created_at', 
        'characters', 
        ])
    for tweet in all_tweets:
        #RTとリプライを含まない
        if (tweet.text.startswith('RT')) or (tweet.text.startswith('@')):
            continue
        else:
            #イギリスのtimezoneを設定するために再定義する
            utc_time = datetime(tweet.created_at.year, tweet.created_at.month,tweet.created_at.day, \
            tweet.created_at.hour,tweet.created_at.minute,tweet.created_at.second, tzinfo=timezone.utc)
            #タイムゾーンを日本時刻に変換
            jst_time = utc_time.astimezone(pytz.timezone("Asia/Tokyo"))
            tweet_time = jst_time
            tweet_characters = tweet.text 
            #urlを文字数にカウントしない
            if len(tweet.entities['urls']) > 0:
                tweet_characters = tweet_characters.strip(tweet.entities['urls'][0]['url']).strip()
            #encode非対応文字列を排除
            tweet.text = tweet.text.encode('cp932','ignore')
            tweet.text = tweet.text.decode('cp932')
            #CSVに出力(1ツイート分)
            writer.writerow([tweet.text, tweet_time,len(tweet_characters)])