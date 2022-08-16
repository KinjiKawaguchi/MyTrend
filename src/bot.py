import sys
import tweepy
import os

CK = os.environ.get('API_KEY')
CS = os.environ.get('API_KEY_SECRET')
AT = os.environ.get('ACCESS_TOKEN')
AS = os.environ.get('ACCESS_TOKEN_SECRET')
print(CK,CK,AT,AS)
auth = tweepy.OAuthHandler(CK, CS)
auth.set_access_token(AT, AS)
api = tweepy.API(auth)

timeline = api.home_timeline()
print(timeline)
#api.update_status("私の名前はMyTrend。よろしくお願いします。")