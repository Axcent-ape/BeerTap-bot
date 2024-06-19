# BeerTap-bot
clicker for [https://t.me/BeerCoinTap_Bot](https://t.me/BeerCoinTap_Bot/beertapapp?startapp=_6008239182)

More crypto themes and softs in telegram: [ApeCryptor](https://t.me/+_xCNXumUNWJkYjAy "ApeCryptor") 🦧
Additional soft information: https://t.me/ApeCryptorSoft/96

## Functionality
| Functional                                                     | Supported |
|----------------------------------------------------------------|:---------:|
| Multithreading                                                 |     ✅     |
| Binding a proxy to a session                                   |     ✅     |
| Auto-pou                                                       |     ✅     |
| Random sleep time between accounts; pours                      |     ✅     |
| Support pyrogram .session                                      |     ✅     |
| Get statistics for all accounts                                |     ✅     |

## Settings data/config.py
| Setting                      | Description                                                                                    |
|------------------------------|------------------------------------------------------------------------------------------------|
| **API_ID / API_HASH**        | Platform data from which to launch a Telegram session                                          |
| **DELAYS-ACCOUNT**           | Delay between connections to accounts (the more accounts, the longer the delay)                |
| **DELAYS-POUR**              | Delay between pour beers                                                                       |
| **PINTS**                    | pints for requests                                                                             |
| **PROXY_TYPES-TG**           | Proxy type for telegram session                                                                |
| **PROXY_TYPES-REQUESTS**     | Proxy type for requests                                                                        |
| **WORKDIR**                  | directory with session                                                                         |
| **TIMEOUT**                  | timeout in seconds for checking accounts on valid                                              |

## Requirements
- Python 3.9 (you can install it [here](https://www.python.org/downloads/release/python-390/)) 
- Telegram API_ID and API_HASH (you can get them [here](https://my.telegram.org/auth))

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
## Usage
1. Run the bot:
   ```bash
   python main.py
   ```
