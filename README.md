# 🤖 Cry_Ass — Crypto Analyst Telegram Bot

Cry_Ass is a fun, fast, and functional **Telegram bot** that analyzes cryptocurrencies and returns:
- 📈 Price analysis
- 📰 News-based insights
- 🧾 Final summary report
- 📊 Market graph
- 🔘 Inline keyboard navigation

Built using Python and the Telegram Bot API, this project is designed to be modular and extendable for your own crypto data analysis needs.

---

## 🚀 Features

- **/start command** — presents ticker options with inline buttons (BTC, ETH, SOL, DOGE)
- **/custom SYMBOL** — supports user-defined ticker symbols like `/custom SHIB`
- **📉 Market Chart** — auto-generated using `yfinance` & `matplotlib`
- **🔄 Back Button** — after showing results, user can go back and select another ticker
- **Environment-secured API Token** — uses `os.environ` to manage sensitive keys

---

## 🧰 Technologies Used

| Tool | Purpose |
|------|---------|
| [`python-telegram-bot`](https://python-telegram-bot.org) | Bot framework |
| `matplotlib` | Plot market charts |
| `yfinance` | Get historical crypto data |
| `asyncio` | Handle delays and animations |
| `os`, `sys` | Environment handling & imports |
| `VS Code` | Primary IDE |

---

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/Cry_Ass-Telegram-Bot.git
cd Cry_Ass-Telegram-Bot

# (Optional) Create virtual environment
python -m venv crypto
source crypto/bin/activate  # for macOS/Linux
crypto\Scripts\activate.bat  # for Windows

# Install dependencies
pip install -r requirements.txt
