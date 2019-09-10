# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 12:55:26 2019

@author: Navnit Singh
"""

import twitter
api=twitter.Api(consumer_key='---',
                consumer_secret='---',
                access_token_key='---',
                access_token_secret='---')
print(api.VerifyCredentials())

twitter_data_raw=[]

def create_test_data(search_string):
    try:
        tweets_fetched=api.GetSearch(search_string, count=2000)
        print("fetched")
        for status in tweets_fetched:
            if status.retweet_count>0:
                if status.text not in twitter_data_raw:
                    twitter_data_raw.append(status.text)
            else:
                twitter_data_raw.append(status.text)
            if len(twitter_data_raw)==100:
                break
    except:
        print("sorry")
        return None

create_test_data("missionmangal")

import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

twitter_data=[]
remove=['at_user','url']

for tweet in twitter_data_raw:
    review=re.sub('((www\.[^\s]+)|(https?://[^\s]+))','url',tweet)
    review=re.sub('@[^\s]+','at_user',review)
    review=re.sub(r'#([\^s]+)', r'\1', review)
    review=re.sub('[^a-zA-Z]','  ',review)
    review=review.lower()
    review=review.split()
    ps=PorterStemmer()
    review=[ps.stem(word) for word in review if word not in set(stopwords.words('english')) and word not in remove]
    review=' '.join(review)
    twitter_data.append(review)


result=[]
from textblob import TextBlob
for check_tweet in twitter_data:
    analysis=TextBlob(check_tweet)
    if analysis.sentiment.polarity>0:
        res='positive'
    elif analysis.sentiment.polarity==0:
        res='neutral'
    else:
        res='negative'
    result.append(res)

pos=result.count('positive')
neg=result.count('negative')
neu=result.count('neutral')

for i in range(43):
    if result[i]=='negative':
        print(i)
