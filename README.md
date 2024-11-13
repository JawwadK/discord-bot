# Say Hello to Jawwad Bot

A feature-rich Discord bot built with discord.py that includes economy features, music playback, reminders, and various utility commands.

## 🌟 Features

### Basic Commands
- Greeting and interaction commands
- Random memes, jokes, and cat pictures
- Magic 8-ball and other fun utilities
- Server information display
- Dice rolling and coin flipping

### Economy System
- Virtual currency management
- Daily rewards
- Work command with cooldown
- Banking system (deposit/withdraw)
- Slots minigame
- User-to-user transactions

### Music Player
- YouTube playback support
- Queue system
- Basic controls (play, pause, resume, skip)
- Channel management (join/leave)
- Queue display
- High-quality audio streaming

### Reminder System
- One-time reminders
- Recurring reminders
- Reminder list management
- Flexible time formats (years, days, hours, minutes)
- Personal reminder notifications

## 📋 Requirements

- Python 3.8 or higher
- discord.py
- yt-dlp
- FFmpeg
- Other dependencies (listed in requirements.txt)

## 🚀 Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd discord-bot
```

2. **Install required packages**
```bash
pip install -r requirements.txt
```

3. **Install FFmpeg**
- Windows: Download from the official website and add to PATH
- Linux: `sudo apt-get install ffmpeg`
- macOS: `brew install ffmpeg`

4. **Create a config.py file**
```python
TOKEN = 'your-discord-bot-token'
```

5. **Run the bot**
```bash
python bot.py
```

## 💻 Command Usage

### Basic Commands
```
!help           - Show all available commands
!ping           - Check if bot is responsive
!info           - Display bot information
!meme           - Get a random meme
!cat            - Get a random cat picture
!8ball          - Ask the magic 8-ball a question
!joke           - Get a random joke
!quote          - Get a random server quote
!trivia         - Start a trivia question
```

### Economy Commands
```
!balance        - Check your balance
!daily          - Claim daily reward
!work           - Work to earn coins
!deposit        - Deposit money to bank
!withdraw       - Withdraw money from bank
!give           - Give coins to another user
!slots          - Play the slot machine
```

### Music Commands
```
!play           - Play a song from YouTube
!pause          - Pause current song
!resume         - Resume playback
!skip           - Skip current song
!queue          - Show current queue
!join           - Join voice channel
!leave          - Leave voice channel
```

### Reminder Commands
```
!remind me      - Set a one-time reminder
!remind repeat  - Set a recurring reminder
!remind list    - List all your reminders
!remind clear   - Clear all your reminders
```

## ⚙️ Configuration

The bot uses a `config.py` file for sensitive information. Create this file with your Discord bot token:

```python
TOKEN = 'your-discord-bot-token'
```

## 📁 File Structure
```
discord-bot/
├── bot.py              # Main bot file
├── config.py           # Configuration file
├── requirements.txt    # Dependencies
├── README.md          # Documentation
└── cogs/
    ├── basic_commands.py    # Basic utility commands
    ├── economy.py          # Economy system
    ├── music_playback.py   # Music player
    ├── reminders.py        # Reminder system
    └── help.py            # Custom help command
```

## 🚨 Error Handling

The bot includes comprehensive error handling for:
- Invalid commands
- Missing permissions
- Invalid arguments
- Command cooldowns
- API failures
- Music playback issues

## 🔧 Maintenance

To maintain the bot:
1. Regularly check for discord.py updates
2. Monitor error logs
3. Update API endpoints if needed
4. Backup the economy and reminder data files

## 📝 Notes

- The bot requires "Message Content" intent to be enabled in the Discord Developer Portal
- For music playback, ensure your server has enough bandwidth
- Economy and reminder data is stored locally in JSON files
- All commands use the '!' prefix by default

## 🤝 Contributing

Feel free to contribute to this project by:
1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 💪 Support

For support, please open an issue in the GitHub repository or contact the maintainer.
