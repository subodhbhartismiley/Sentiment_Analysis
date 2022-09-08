“import re
import csv
import numpy as np
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import matplotlib.pyplot as plt
import random
import string
from nltk.corpus import wordnet as wn


# import preprocessor as p
# p.clean('Preprocessor is #awesome 👍 https://github.com/s/preprocessor')

class TwitterClient(object):
    def __init__(self):
        consumer_key = 'jbkZ2RmduoH7eh9WBpPUQWro3'
        consumer_secret = 'RpdmaKXShnzz8NdjlBG6vad88E3CebNtx5Gb03fkEvGCst1fIo'
        access_token = '585362387-kqPJV0ztt0Q1RVQdz77LTMhWV0CzNgk1cAJwmBHm'
        access_token_secret = 'jYfkksmxZybdn9pwpArAVWzSDpe0J4yaafU3EqQS9yJQ3'
        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        sent_tweet = ' '.join(re.sub(
            "(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|positive|Positive|POSITIVE|PoStive|negative|Negative|NEGATIVE",
            " ", tweet).split())
        return sent_tweet

    def get_tweet_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count=20000):
        tweets = []
        try:
            fetched_tweets = self.api.search(q=query + '-filter:retweets -filter:replies', count=count)
            for tweet in fetched_tweets:
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.text
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            return tweets

        except tweepy.TweepError as e:
            print("Error : " + str(e))


def plot():
    api = TwitterClient()
    print('enter queries \n')
    q1 = input('enter queries with OR logical for multiple else simple space for AND logic \n ')
    q = ''
    for ss in wn.synsets(q1):  # Each synset represents a diff concept.(synonyms of the word)
        q = ss.lemma_names()
        # print( ss.lemma_names())

    # Python program to convert a list to string using list comprehension. replace space with OR logic
    listToStr = ' '.join([str(elem) for elem in q])
    q = listToStr
    q = q.replace(' ', ' OR ')
    if q != '':
        q = q1 + " OR " + q
    q = q.replace(' OR OR ', ' OR ')
    # print(q)
    n = input('enter number of tweets to analyze \n')

    tweets = api.get_tweets(query=q + '-filter:retweets -filter:replies', count=n)
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']

    pt = format(100 * len(ptweets) / len(tweets))
    print("POSITIVE TWEET PERSENTAGE: ", pt)

    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']

    # for tweets of neutral sentiment
    nuttweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']

    nt = format(100 * len(ntweets) / len(tweets))
    print("NEGATIVE TWEET PERSENTAGE: ", nt)

    nut = format(100 * (len(tweets) - len(ntweets) - len(ptweets)) / len(tweets))
    print("NEUTRAL TWEET PERSENTAGE", nut)

    # for pie chart
    l = ['Positive', 'Negative', 'Neutral']
    sizes = [pt, nt, nut]
    colors = ['green', 'red', 'blue']
    explode = (0.1, 0, 0)  # explode 1st slice
    # textprops = {"fontsize":50} # Font size of text in pie chart
    # plt.setp(autotexts, size=8, weight="bold")

    # patches, texts =
    fig = plt.figure(figsize=(12, 7))

    # plt.pie(data, labels = cars)
    plt.pie(sizes, explode=explode, labels=l, colors=colors, textprops={'color': "lawngreen", 'fontsize': 13},
            autopct='%1.1f%%', shadow=True, startangle=45)
    '''plt.pie(sizes, explode=explode, labels=labels, colors=colors,
                autopct='%1.1f%%', shadow=True, startangle=40,textprops =textprops)
    '''

    plt.axis('equal')

    # random string without repeating letters
    def randomString2(stringLength):
        letters = string.ascii_lowercase
        return ''.join(random.sample(letters, stringLength))

    myfig = randomString2(6)
    plt.savefig('myfig')
    # print('myfig.png')
    plt.title('Sentiment Analysis Pie chart')
    plt.show()

    print("\n\nPOSITIVE TWEETS:")
    for tweet in ptweets[:10]:
        print(tweet['text'])
    print("\n\nNEGATIVE TWEETS:")
    for tweet in ntweets[:10]:
        print(tweet['text'])
    print("\n\nNeutral TWEETS:")
    for tweet in nuttweets[:10]:
        print(tweet['text'])


def main():
    plot()


if __name__ == "__main__":
    main()  ”