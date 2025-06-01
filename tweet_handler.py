import requests
import json
from typing import List, Dict, Any
from datetime import datetime
from config import data
from data_rotator import DataRotator

class TweetHandler:
    def __init__(self, config_data):
        self.url = "https://x.com/i/api/graphql/qRZZ3tIWQobwfvBFTnToOA/UserTweets"
        self.last_tweet_id = None
        self.initialized = False
        self.max_tweets_per_check = 3
        self.processed_tweets = set()

        # Get configuration from config
        self.variables = config_data['request_data']['profile']['variables_userTweets']
        self.features = config_data['request_data']['profile']['features_userTweets']
        
        # Create data rotator for auth data
        auth_data_list = [
            data for key, data in config_data['request_data']['profile']['list_changeData'].items()
            if key.startswith('data_')
        ]
        self.data_rotator = DataRotator(auth_data_list)

        self.field_toggles = {
            "withArticlePlainText": False
        }

        self.params = {
            "variables": json.dumps(self.variables),
            "features": json.dumps(self.features),
            "fieldToggles": json.dumps(self.field_toggles)
        }

    def get_latest_tweets(self) -> List[Dict[str, Any]]:
        """Thread-safe method for getting latest tweets"""
        try:
            current_time = datetime.now().strftime("%H:%M:%S")
            auth_data, auth_id = self.data_rotator.get_next()
            
            response = requests.get(self.url, headers=auth_data['headers'], 
                                 cookies=auth_data['cookies'], params=self.params)
            
            if response.status_code == 200:
                print(f"[{current_time}] Tweets received ({auth_id})")
                tweets_data = response.json()
                instructions = tweets_data['data']['user']['result']['timeline']['timeline']['instructions']
                entries = []
                
                for instruction in instructions:
                    if 'entries' in instruction:
                        entries = instruction['entries']
                        break
                
                new_tweets = []
                for entry in entries:
                    if 'tweet' in entry['entryId'].lower():
                        try:
                            tweet_data = entry['content']['itemContent']['tweet_results']['result']
                            tweet_id = tweet_data['rest_id']
                            
                            # Ініціалізація last_tweet_id при першому запуску
                            if not self.initialized:
                                self.last_tweet_id = tweet_id
                                self.initialized = True
                                return []
                            
                            # Перевіряємо чи твіт новіший за останній відомий
                            if self.last_tweet_id and int(tweet_id) > int(self.last_tweet_id):
                                tweet_text = tweet_data['legacy']['full_text']
                                tweet_link = f"https://twitter.com/andytrotw/status/{tweet_id}"
                                
                                new_tweets.append({
                                    'id': tweet_id,
                                    'text': tweet_text,
                                    'link': tweet_link
                                })
                                
                        except (KeyError, TypeError) as e:
                            print(f"Error processing tweet: {e}")
                            continue
                
                if new_tweets:
                    # Оновлюємо last_tweet_id найновішим твітом
                    self.last_tweet_id = new_tweets[0]['id']
                    
                return new_tweets
                
            else:
                print(f"Error getting tweets: {response.status_code} ({auth_id})")
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
