## DC-rip bot

#### Installing

[python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) required

```
$ pip install python-telegram-bot --upgrade
```

#### Usage

```
usage: telegram_bot.py [-h] [-i INTERVAL] bot_token host services

positional arguments:
  bot_token    Telegram bot token
  host         Host address
  services     Comma separated service:port. Example: nginx:80,bind:53
  
optional arguments:
  -h, --help   show this help message and exit
  -i INTERVAL  Availability check interval in seconds. Default is 60
```
