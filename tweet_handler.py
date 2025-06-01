import requests
import json
from typing import List, Dict, Any

class TweetHandler:
    def __init__(self):
        self.url = "https://x.com/i/api/graphql/qRZZ3tIWQobwfvBFTnToOA/UserTweets"
        self.last_tweet_id = None
        self.processed_tweets = set()  
        self.max_tweets_per_check = 3  

        self.variables = {
            "userId": "1647171304192196610",
            "count": 20,
            "includePromotedContent": True,
            "withQuickPromoteEligibilityTweetFields": True,
            "withVoice": True,
        }
        self.features = {
            "rweb_video_screen_enabled": False,
            "profile_label_improvements_pcf_label_in_post_enabled": True,
            "rweb_tipjar_consumption_enabled": True,
            "verified_phone_label_enabled": False,
            "creator_subscriptions_tweet_preview_api_enabled": True,
            "responsive_web_graphql_timeline_navigation_enabled": True,
            "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
            "premium_content_api_read_enabled": False,
            "communities_web_enable_tweet_community_results_fetch": True,
            "c9s_tweet_anatomy_moderator_badge_enabled": True,
            "responsive_web_grok_analyze_button_fetch_trends_enabled": False,
            "responsive_web_grok_analyze_post_followups_enabled": True,
            "responsive_web_jetfuel_frame": False,
            "responsive_web_grok_share_attachment_enabled": True,
            "articles_preview_enabled": True,
            "responsive_web_edit_tweet_api_enabled": True,
            "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
            "view_counts_everywhere_api_enabled": True,
            "longform_notetweets_consumption_enabled": True,
            "responsive_web_twitter_article_tweet_consumption_enabled": True,
            "tweet_awards_web_tipping_enabled": False,
            "responsive_web_grok_show_grok_translated_post": False,
            "responsive_web_grok_analysis_button_from_backend": False,
            "creator_subscriptions_quote_tweet_preview_enabled": False,
            "freedom_of_speech_not_reach_fetch_enabled": True,
            "standardized_nudges_misinfo": True,
            "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
            "longform_notetweets_rich_text_read_enabled": True,
            "longform_notetweets_inline_media_enabled": True,
            "responsive_web_grok_image_annotation_enabled": True,
            "responsive_web_enhance_cards_enabled": False,
        }
        self.field_toggles = {
            "withArticlePlainText": False
        }

        self.headers = {
            "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
            "Content-Type": "application/json",
            "x-csrf-token": "token",
            "x-twitter-active-user": "yes",
            "x-twitter-auth-type": "OAuth2Session",
            "x-twitter-client-language": "uk",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
            "accept-language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7",
            "referer": "https://x.com/"
        }

        self.cookies = {
            "auth_token": "token",
            "ct0": "token",
            "guest_id": "token"
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
