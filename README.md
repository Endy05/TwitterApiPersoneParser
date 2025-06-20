# Twitter Profile & Tweet Monitor

Real-time monitoring system for Twitter/X profiles with multi-account support and Telegram notifications.

## Features

-   🔄 Profile Changes Monitoring:
    -   Avatar updates
    -   Banner updates
    -   Name changes
    -   Username changes
-   📱 Real-time Tweet Detection
-   📨 Telegram Notifications
-   🔁 Multiple Account Rotation
-   ⚡ Auto Rate Limit Handling
-   🔒 Environment Variables Support

## Requirements

-   Python 3.7+
-   Active Telegram bot
-   Twitter authentication credentials (multiple accounts supported)
-   pip packages:
    -   python-telegram-bot>=20.0
    -   python-dotenv
    -   requests
    -   aiohttp

## Setup

1.  Clone the repository:

    ```bash
    git clone https://github.com/yourusername/twitterParser.git
    cd twitterParser
    ```

2.  Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3.  Configure environment variables in `.env`:

    ```env
    TELEGRAM_BOT_TOKEN="your_bot_token"
    TELEGRAM_CHANNEL_ID="@your_channel"
    TWITTER_CSRF_TOKEN="your_csrf_token"
    TWITTER_AUTH_TOKEN="your_auth_token"
    TWITTER_GUEST_ID="your_guest_id"
    USER_ID="target_user_id"
    SCREEN_NAME="target_username"
    ```

4.  Run the monitoring system:

    ```bash
    python main.py
    ```

## Rate Limiting

The system automatically manages rate limits by:

-   Rotating between multiple Twitter auth tokens
-   Using smart delays between requests (18 requests per auth token for tweets)
-   Auto-adjusting intervals based on number of auth tokens

## Project Structure

```
twitterParser/
├── main.py              # Main application
├── config.py            # Configuration and auth data
├── tweet_handler.py     # Tweet monitoring
├── twitter_profile.py   # Profile monitoring
├── telegram_handler.py  # Telegram integration
├── thread_manager.py    # Multi-threading management
├── data_rotator.py     # Auth data rotation
├── user_state.py       # Profile state tracking
└── requirements.txt     # Dependencies
```

## Configuration

### Auth Data Rotation

The system supports multiple Twitter authentication configurations. Add new auth data sets in `config.py`:

```python
"list_changeData": {
    "data_1": { ... },
    "data_2": { ... },
    "data_N": { ... }
}
```

### Monitoring Intervals

Adjust intervals in `config.py`:

```python
INTERVAL = 3  # Default interval in seconds
```

## Error Handling

-   Automatic auth rotation on rate limits
-   Exponential backoff on errors
-   Console logging for debugging
-   Multiple auth tokens support

## Contributing

1.  Fork the repository
2.  Create feature branch
3.  Commit changes
4.  Push to branch
5.  Create Pull Request

## License

MIT License
