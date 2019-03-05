## DC-rip bot

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