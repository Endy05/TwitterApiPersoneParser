import requests
import json
from typing import List, Dict, Any
from config import data

class TweetHandler:
    def __init__(self):
        self.url = "https://x.com/i/api/graphql/qRZZ3tIWQobwfvBFTnToOA/UserTweets"
        self.last_tweet_id = None
        self.processed_tweets = set()  
        self.max_tweets_per_check = 3  

        # Get configuration from config
        self.variables = data['request_data']['profile']['variables_userTweets']
        self.features = data['request_data']['profile']['features_userTweets']
        self.headers = data['request_data']['profile']['headers']
        self.cookies = data['request_data']['profile']['cookies']
        
        self.field_toggles = {
            "withArticlePlainText": False
        }

        self.params = {
            "variables": json.dumps(self.variables),
            "features": json.dumps(self.features),
            "fieldToggles": json.dumps(self.field_toggles)
        }

    def get_latest_tweets(self) -> List[Dict[str, Any]]:
        try:
            response = requests.get(self.url, headers=self.headers, params=self.params, cookies=self.cookies)
            if response.status_code == 200:
                tweets_data = response.json()
                instructions = tweets_data['data']['user']['result']['timeline']['timeline']['instructions']
                entries = []
                
                for instruction in instructions:
                    if 'entries' in instruction:
                        entries = instruction['entries']
                        break
                
                tweet_list = []
                for entry in entries:
                    if 'tweet' in entry['entryId'].lower():
                        try:
                            tweet_data = entry['content']['itemContent']['tweet_results']['result']
                            tweet_id = tweet_data['rest_id']
                            tweet_text = tweet_data['legacy']['full_text']
                            tweet_link = f"https://twitter.com/andytrotw/status/{tweet_id}"
                            
                            tweet_list.append({
                                'id': tweet_id,
                                'text': tweet_text,
                                'link': tweet_link
                            })
                            print(f"Found tweet: {tweet_id}")
                        except (KeyError, TypeError) as e:
                            print(f"Error processing tweet: {e}")
                            continue
                
                return tweet_list
            else:
                print(f"Error getting tweets: {response.status_code}")
                return []
        except Exception as e:
            print(f"Exception in get_latest_tweets: {e}")
            return []

    def get_new_tweets(self):
        tweets = self.get_latest_tweets()
        if not tweets:
            return []

        new_tweets = []
        for tweet in tweets:
            tweet_id = tweet['id']
            if tweet_id not in self.processed_tweets:
                new_tweets.append(tweet)
                self.processed_tweets.add(tweet_id)

        if self.last_tweet_id is None:
            self.last_tweet_id = tweets[0]['id']
            return [] 

        return new_tweets[:self.max_tweets_per_check]

    def print_last_tweets(self, count=3):
        tweets = self.get_latest_tweets()
        if not tweets:
            print("No tweets found.")
            return

        print(f"\nLast {count} tweets:")
        print("-" * 50)

        for tweet in tweets[:count]:
            print(f"Tweet ID: {tweet['id']}")
            print(f"Content: {tweet['text']}")
            print(f"Link: {tweet['link']}")
            print("-" * 50)
