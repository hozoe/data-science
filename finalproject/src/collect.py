import os
import tweepy as tw
import pandas as pd


consumer_key= 'MMbnXsuvnnzxuGSlbhQrLTctK'
consumer_secret= 'SBp9BP2glx63DGKqcOAv40TXEG7K0lA1aOwMqgiAqRwdJDuQSw'
access_token= '277973579-ONIrveN5wRw0WFzDvS19O9J2TbLNKiVGVdQDzAHp'
access_token_secret= 'suFMSt6Z4UaA9yZl8KESZpduMISZIAJXCRRa0xW3TLrXF'

def search_tweets():
    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth)
    search_words = "#DuneMovie" + " -filter:retweets" #filter retweets, also can add more keywords/hashtags
    '''the new search_tweets method only can look for tweets within the past 7 days from the moment you are scraping the tweets so maybe set
    num_tweets to be larger like 3000 and then filter by the dates to get 3 days of tweets'''
    num_tweets = 20
    results = api.search_tweets(q=search_words,lang="en",until = "2021-11-30", result_type = 'mixed', count = num_tweets)
    dates = [] 
    tweets = []
    users = []
    for tweet in results:
        dates.append(tweet.created_at)
        tweets.append(tweet.text)
        users.append(tweet.id)
    
    df = pd.DataFrame(columns=['user','date','tweets'])
    df['user'] = users
    df['date'] = dates
    df['tweets'] = tweets
    df.to_csv(os.path.join('..','data','tweets.csv'),index=False)

    
def main():
    search_tweets()

if __name__ == "__main__":
    main()