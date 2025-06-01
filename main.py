import requests
import json
import asyncio
from datetime import datetime
import telegram
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID
from tweet_handler import TweetHandler

class UserState:
    def __init__(self):
        self.name = None
        self.username = None
        self.avatar_url = None
        self.banner_url = None

    def get_changes(self, new_name, new_username, new_avatar, new_banner):
        changes = []
        if self.avatar_url != new_avatar:
            changes.append(
                f"NEW AVA {new_username.upper()}\n"
                f"{new_avatar}\n\n"
                f"OLD AVA {new_username.upper()}\n"
                f"{self.avatar_url}"
            )
        if self.banner_url != new_banner and new_banner:  
            changes.append(
                f"NEW BANNER {new_username.upper()}\n"
                f"{new_banner}\n\n"
                f"OLD BANNER {new_username.upper()}\n"
                f"{self.banner_url or 'Default banner'}"
            )
        if self.name != new_name:
            changes.append(f"NAME CHANGING\n\n{self.name} ➜ {new_name}")
        if self.username != new_username:
            changes.append(f"USERNAME CHANGING\n\n@{self.username} ➜ @{new_username}")
        return changes

state = UserState()

bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

url = "https://x.com/i/api/graphql/xWw45l6nX7DP2FKRyePXSw/UserByScreenName"

variables = {
    "screen_name": "andytrotw"
}

features = {
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
}

headers = {
    "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
    "x-csrf-token": "token",
    "x-twitter-auth-type": "OAuth2Session",
    "x-twitter-active-user": "yes",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "accept-language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7",
    "referer": "https://x.com/"
}

cookies = {
    "auth_token": "token",
    "ct0": "token",
    "guest_id": "token",
}

params = {
    "variables": json.dumps(variables),
    "features": json.dumps(features),
    "fieldToggles": json.dumps({"withAuxiliaryUserLabels": True})
}

async def send_telegram_message(message, max_retries=3):
    for attempt in range(max_retries):
        try:
            await bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=message, parse_mode='HTML')
            return True
        except Exception as e:
            print(f"Attempt {attempt + 1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(2)
    return False

def get_full_avatar_url(url):
    if url and '_normal.' in url:
        return url.replace('_normal.', '.')
    return url

async def main():
    tweet_handler = TweetHandler()
    print("Starting tweet monitoring...")
    first_run = True
    base_delay = 5 
    current_delay = base_delay
    max_delay = 90 
    message_delay = 2  
    
    while True:
        try:
            new_tweets = tweet_handler.get_new_tweets()
            
            if not first_run and new_tweets:
                print(f"\nFound {len(new_tweets)} new tweets")
                for tweet in new_tweets:
                    message = (
                        f"🐦 Новий твіт від @{variables['screen_name']}:\n\n"
                        f"{tweet['text']}\n\n"
                        f"🔗 {tweet['link']}"
                    )
                    sent = await send_telegram_message(message)
                    if sent:
                        print(f"Tweet sent successfully: {tweet['id']}")
                        await asyncio.sleep(message_delay)  
                    else:
                        print(f"Failed to send tweet: {tweet['id']}")

            first_run = False
            
            # Profile changes check
            response = requests.get(url, headers=headers, cookies=cookies, params=params)
            current_time = datetime.now().strftime("%H:%M:%S")
            
            if response.status_code == 429:
                print(f"[{current_time}] Rate limit reached (429). Waiting {current_delay} seconds...")
                await asyncio.sleep(current_delay)
                current_delay = min(current_delay * 2, max_delay)  
                continue
            
            if response.ok:
                current_delay = base_delay 
                data = response.json()
                user = data["data"]["user"]["result"]
                name = user["core"]["name"]
                username = user["core"]["screen_name"]
                avatar_url = get_full_avatar_url(user.get("avatar", {}).get("image_url", None))
                
                banner_url = None
                if "profile_banner_url" in user.get("legacy", {}):
                    banner_url = f"{user['legacy']['profile_banner_url']}/600x200"
                
                # Debug logging
                print(f"\n[{current_time}] Перевірка профілю:")
                print(f"Ім'я: {name}")
                print(f"Username: {username}")
                print(f"Avatar: {avatar_url}")
                print(f"Banner: {banner_url}")
                print("-" * 50)

                if state.name is not None:
                    changes = state.get_changes(name, username, avatar_url, banner_url)
                    if changes:
                        print(f"[{current_time}] Виявлено зміни в профілі!")
                        for change_message in changes:
                            await send_telegram_message(change_message)
                            print(f"Надіслано повідомлення про зміну:\n{change_message}")

                state.name = name
                state.username = username
                state.avatar_url = avatar_url
                state.banner_url = banner_url

            else:
                error_message = f"❌ Помилка: {response.status_code}"
                print(f"[{current_time}] {error_message}")
                await send_telegram_message(error_message)
                if response.status_code >= 500:
                    await asyncio.sleep(current_delay)
                    current_delay = min(current_delay * 2, max_delay)
        
        except Exception as e:
            print(f"Error in main loop: {e}")
            current_delay = min(current_delay * 2, max_delay)
        
        await asyncio.sleep(current_delay)

if __name__ == "__main__":
    asyncio.run(main())

