import telegram
import asyncio
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID

class TelegramHandler:
    def __init__(self):
        self.bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
        self.channel_id = TELEGRAM_CHANNEL_ID

    async def send_message(self, message, max_retries=3):
        for attempt in range(max_retries):
            try:
                await self.bot.send_message(
                    chat_id=self.channel_id, 
                    text=message, 
                    parse_mode='HTML'
                )
                return True
            except Exception as e:
                print(f"Attempt {attempt + 1}/{max_retries} failed: {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2)
        return False
