import asyncio
from config import data
from tweet_handler import TweetHandler
from user_state import UserState
from telegram_handler import TelegramHandler
from twitter_profile import TwitterProfile

state = UserState()
telegram_handler = TelegramHandler()
twitter_profile = TwitterProfile(data)

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
                        f"🐦 Новий твіт від @{data['request_data']['profile']['variables_userByScreenName']['screen_name']}:\n\n"
                        f"{tweet['text']}\n\n"
                        f"🔗 {tweet['link']}"
                    )
                    sent = await telegram_handler.send_message(message)
                    if sent:
                        print(f"Tweet sent successfully: {tweet['id']}")
                        await asyncio.sleep(message_delay)  
                    else:
                        print(f"Failed to send tweet: {tweet['id']}")

            first_run = False
            
            # Profile changes check
            profile_data = await twitter_profile.check_profile()
            current_time = profile_data['current_time']
            
            if profile_data['status'] == 'error':
                if profile_data.get('code') == 429:
                    print(f"[{current_time}] Rate limit reached (429). Waiting {current_delay} seconds...")
                    await asyncio.sleep(current_delay)
                    current_delay = min(current_delay * 2, max_delay)
                    continue
                    
                error_message = f"❌ Помилка: {profile_data.get('code', 'Unknown error')}"
                print(f"[{current_time}] {error_message}")
                await telegram_handler.send_message(error_message)
                if profile_data.get('code', 500) >= 500:
                    await asyncio.sleep(current_delay)
                    current_delay = min(current_delay * 2, max_delay)
                continue
            
            current_delay = base_delay
            
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
            current_delay = min(current_delay * 2, max_delay)
        
        await asyncio.sleep(current_delay)

if __name__ == "__main__":
    asyncio.run(main())

