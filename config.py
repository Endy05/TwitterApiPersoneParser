from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")  

data = {
    "request_data": {
        "profile": {
            "variables_userByScreenName" : {
                "screen_name": "andytrotw"
            },

            "variables_userTweets" : {
                "userId": "1647171304192196610",
                "count": 20,
                "includePromotedContent": True,
                "withQuickPromoteEligibilityTweetFields": True,
                "withVoice": True,
            },

            "features_userByScreenName" : {
                "hidden_profile_subscriptions_enabled": True,
                "profile_label_improvements_pcf_label_in_post_enabled": True,
                "rweb_tipjar_consumption_enabled": True,
                "verified_phone_label_enabled": False,
                "subscriptions_verification_info_is_identity_verified_enabled": True,
                "subscriptions_verification_info_verified_since_enabled": True,
                "highlights_tweets_tab_ui_enabled": True,
                "responsive_web_twitter_article_notes_tab_enabled": True,
                "subscriptions_feature_can_gift_premium": True,
                "creator_subscriptions_tweet_preview_api_enabled": True,
                "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                "responsive_web_graphql_timeline_navigation_enabled": True
            },

            "features_userTweets" : {
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
            }, 
    
            "headers" : {
                "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
                "Content-Type": "application/json",
                "x-csrf-token": os.getenv("TWITTER_CSRF_TOKEN"),
                "x-twitter-active-user": "yes",
                "x-twitter-auth-type": "OAuth2Session",
                "x-twitter-client-language": "uk",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
                "accept-language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7",
                "referer": "https://x.com/"
            },

            "cookies" : {
                "auth_token": os.getenv("TWITTER_AUTH_TOKEN"),
                "ct0": os.getenv("TWITTER_CSRF_TOKEN"),
                "guest_id": os.getenv("TWITTER_GUEST_ID"),
            }
        }
    }
}
