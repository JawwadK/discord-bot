<div align="center">
  
# Jawwad Bot

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Discord.py](https://img.shields.io/badge/discord.py-v2.3.2-blue)](https://discordpy.readthedocs.io/en/stable/)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

🤖 A feature-rich Discord bot with music, economy, and reminder systems

</div>

## 📋 Features

### 🎵 Music System

- Play music from YouTube with high-quality audio
- Queue system with playlist support
- Basic controls (play, pause, skip, stop)
- Volume control and audio filters

### 💰 Economy System

- Virtual currency system
- Daily rewards
- Work and earn system
- Gambling games (slots, etc.)
- Bank system with deposits/withdrawals

### ⏰ Reminder System

- Set personal reminders
- Recurring reminders
- Customizable time formats
- Multiple reminder management

### 🎮 Fun Commands

- 8ball predictions
- Random memes
- Cat pictures
- Coin flip and dice rolls
- Server-specific quotes

## 📝 Commands

<details>
<summary>Click to see command list</summary>

### Music Commands

```
!play [url/search]  - Play music from YouTube
!pause             - Pause current track
!resume            - Resume playback
!skip              - Skip current track
!queue             - View music queue
!leave             - Leave voice channel
```

### Economy Commands

```
!balance           - Check your balance
!daily             - Claim daily reward
!work              - Work for coins
!deposit [amount]  - Deposit to bank
!withdraw [amount] - Withdraw from bank
!slots [amount]    - Play slots
```

### Reminder Commands

```
!remind me [time] [message]     - Set a one-time reminder
!remind repeat [time] [message] - Set a recurring reminder
!remind list                    - View your reminders
!remind clear                   - Clear all reminders
```

### Fun Commands

```
!8ball [question]  - Ask the magic 8ball
!meme              - Get a random meme
!cat               - Get a random cat picture
!flipcoin          - Flip a coin
!rolldice [sides]  - Roll a dice
!quote             - Get a server quote
```

</details>

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- A Discord Bot Token

### Installation

1. Clone the repository

```bash
git clone https://github.com/yourusername/jawwad-bot.git
cd jawwad-bot
```

2. Install required packages

```bash
pip install -r requirements.txt
```

3. Configure the bot

```bash
# Create config.py in the config directory with your bot token
TOKEN = 'your-bot-token-here'
```

4. Run the bot

```bash
python run.py
```

## 🌐 Hosting

This bot can be hosted on various platforms:

- Google Cloud Platform (Free Tier)
- Oracle Cloud
- Personal VPS
- Local machine

Detailed hosting instructions can be found in our [hosting guide](docs/hosting.md).

## 📂 Project Structure

```
jawwad-bot/
├── src/              # Source code
│   ├── bot.py       # Main bot file
│   ├── cogs/        # Command categories
│   └── utils/       # Utility functions
├── config/          # Configuration files
├── data/            # Data storage
└── logs/            # Log files
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [discord.py](https://github.com/Rapptz/discord.py)
- [youtube-dl](https://github.com/ytdl-org/youtube-dl)
- All the contributors and users of this bot

## 📞 Support

If you need help with the bot, feel free to:

- Open an issue on GitHub
- Join our [support server](your-discord-invite)
- Contact the developer on Discord

---

<div align="center">
Made with ❤️ by Jawwad Khan
</div>
