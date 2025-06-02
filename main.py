import asyncio
from config import data
from tweet_handler import TweetHandler
from user_state import UserState
from telegram_handler import TelegramHandler
from twitter_profile import TwitterProfile
from thread_manager import ThreadManager
from rate_limiter import RateLimiter
 
async def main():
    # Initialize components
    state = UserState()
    telegram_handler = TelegramHandler()
    tweet_handler = TweetHandler(data)  # Pass config data
    twitter_profile = TwitterProfile(data)
    thread_manager = ThreadManager()
    limeter = RateLimiter()

    limiter_tweet, limeter_profile = limeter.get_rate_limit()
    print(f"Rate limit for tweets: {limiter_tweet} seconds")
    print(f"Rate limit for profile: {limeter_profile} seconds")

    # Add workers to thread manager with correct method names
    thread_manager.add_worker("tweets", tweet_handler.get_latest_tweets, interval=limiter_tweet)
    thread_manager.add_worker("profile", twitter_profile.check_profile, interval=limeter_profile)

    print("Starting monitoring...")
    thread_manager.start()

    # Add rate limit notification state
    rate_limit_notified = False

    try:
        while True:
            try:
                tweets = thread_manager.get_result("tweets")
                profile_data = thread_manager.get_result("profile")

                if tweets:
                    print(f"\nFound {len(tweets)} new tweets")
                    for tweet in tweets:
                        message = (
                            f"🐦 A new tweet from @{data['request_data']['profile']['variables_userByScreenName']['screen_name']}:\n\n"
                            f"{tweet['text']}\n\n"
                            f"🔗 {tweet['link']}\n\n"
                            f"🕒 Created at : {tweet['created_at']}"
                        )
                        sent = await telegram_handler.send_message(message)
                        if sent:
                            print(f"Tweet sent successfully: {tweet['id']}")
                        else:
                            print(f"Failed to send tweet: {tweet['id']}")

                if profile_data:
                    current_time = profile_data['current_time']
                    
                    if profile_data['status'] == 'error':
                        if profile_data.get('code') == 429:
                            print(f"[{current_time}] Rate limit reached (429). Waiting...")
                            if not rate_limit_notified:
                                await telegram_handler.send_message("⚠️ Досягнуто ліміт запитів (429). Моніторинг буде продовжено автоматично після відновлення доступу.")
                                rate_limit_notified = True
                            await asyncio.sleep(5)
                            continue
                        
                        print(f"[{current_time}] ❌ Помилка: {profile_data.get('code', 'Unknown error')}")
                        if profile_data.get('code', 500) >= 500:
                            await asyncio.sleep(5)
                        continue
                    
                    # Reset rate limit notification state when successful
                    rate_limit_notified = False
                    
                    # Debug logging
                    print(f"\n[{current_time}] Перевірка профілю:")
                    print(f"Ім'я: {profile_data['name']}")
                    print(f"Username: {profile_data['username']}")
                    print(f"Avatar: {profile_data['avatar_url']}")
                    print(f"Banner: {profile_data['banner_url']}")
                    print("-" * 50)

                    if state.name is not None:
                        changes = state.get_changes(
                            profile_data['name'],
                            profile_data['username'],
                            profile_data['avatar_url'],
                            profile_data['banner_url']
                        )
                        if changes:
                            print(f"[{current_time}] Виявлено зміни в профілі!")
                            for change_message in changes:
                                await telegram_handler.send_message(change_message)
                                print(f"Надіслано повідомлення про зміну:\n{change_message}")

                    state.name = profile_data['name']
                    state.username = profile_data['username']
                    state.avatar_url = profile_data['avatar_url']
                    state.banner_url = profile_data['banner_url']
            
            except Exception as e:
                print(f"Error in main loop: {e}")
                await asyncio.sleep(5)

    finally:
        thread_manager.stop()

if __name__ == "__main__":
    asyncio.run(main())

