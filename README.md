# 🚀 DexScreener Token Monitor Bot

<div align="center">

**Real-time Token Monitoring & Telegram Notifications**  
**रियल-टाइम टोकन मॉनिटरिंग और टेलीग्राम सूचनाएं**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

---

## 📖 Table of Contents / विषय सूची

- [English Documentation](#english-documentation)
  - [Overview](#overview)
  - [Features](#features)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Telegram Bot Setup](#telegram-bot-setup)
  - [Configuration](#configuration)
  - [Usage](#usage)
  - [Running on Server](#running-on-server)
  - [Troubleshooting](#troubleshooting)
- [हिंदी डॉक्युमेंटेशन](#hindi-documentation)
  - [अवलोकन](#अवलोकन)
  - [विशेषताएं](#विशेषताएं)
  - [आवश्यक चीजें](#आवश्यक-चीजें)
  - [इंस्टॉलेशन](#इंस्टॉलेशन)
  - [टेलीग्राम बॉट सेटअप](#टेलीग्राम-बॉट-सेटअप)
  - [कॉन्फ़िगरेशन](#कॉन्फ़िगरेशन)
  - [उपयोग](#उपयोग)
  - [सर्वर पर चलाना](#सर्वर-पर-चलाना)
  - [समस्या निवारण](#समस्या-निवारण)

---

# English Documentation

## 🌟 Overview

DexScreener Token Monitor is an automated bot that continuously monitors [DexScreener](https://dexscreener.com/) for new token listings and sends instant notifications to your Telegram group. The bot uses Selenium WebDriver to scrape the website and detects tokens with the `ds-dex-table-row-new` class.

### Key Highlights
- ⚡ Real-time monitoring
- 🤖 Automated Telegram notifications
- 💾 Persistent storage to avoid duplicates
- 🔄 Auto-restart on failure
- 📊 Detailed logging
- 🐧 Linux server compatible

## ✨ Features

- **Real-time Monitoring**: Continuously scans DexScreener for new tokens
- **Smart Detection**: Identifies new tokens using CSS class `ds-dex-table-row-new`
- **Comprehensive Data Extraction**:
  - Token name/symbol
  - Blockchain/chain
  - Current price
  - Pair age
  - DexScreener link
  - Contract address
- **Telegram Integration**: 
  - Formatted HTML messages with emojis
  - Instant notifications
  - Rate limiting to avoid API limits
- **Duplicate Prevention**: Maintains a record of sent tokens
- **Error Handling**: 
  - Automatic retry logic
  - WebDriver recovery
  - Comprehensive error logging
- **Server Ready**:
  - Headless Chrome support
  - Systemd service integration
  - Auto-start on boot

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Chrome or Chromium browser
- Ubuntu/Debian Linux (recommended for server)
- Telegram account

## 🛠️ Installation

### Method 1: Automatic Setup (Recommended)

1. **Clone the repository**
```bash
git clone https://github.com/sureshshukla12996/goddex.git
cd goddex
```

2. **Run setup script**
```bash
chmod +x setup.sh
./setup.sh
```

The setup script will:
- Install Python3 and pip
- Install Chrome/Chromium browser
- Create virtual environment
- Install all dependencies
- Create necessary directories
- Optionally set up systemd service

### Method 2: Manual Setup

1. **Clone the repository**
```bash
git clone https://github.com/sureshshukla12996/goddex.git
cd goddex
```

2. **Install system dependencies**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv chromium-browser
```

3. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

4. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

5. **Create directories**
```bash
mkdir -p logs data
```

## 🤖 Telegram Bot Setup

### Step 1: Create a Telegram Bot

1. Open Telegram and search for **@BotFather**
2. Send `/start` command
3. Send `/newbot` command
4. Follow the instructions:
   - Choose a name for your bot (e.g., "DexScreener Monitor")
   - Choose a username (must end with 'bot', e.g., "dexscreener_monitor_bot")
5. **Save the bot token** - you'll need this later

Example token: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz123456789`

### Step 2: Get Your Chat ID

#### For Personal Chat:
1. Search for **@userinfobot** on Telegram
2. Send `/start` command
3. Copy your **User ID**

#### For Group Chat:
1. Add your bot to the group
2. Send any message in the group
3. Visit: `https://api.telegram.org/bot<YourBOTToken>/getUpdates`
4. Look for `"chat":{"id":-123456789` in the response
5. Copy the chat ID (including the minus sign for groups)

### Step 3: Configure Environment Variables

1. **Copy the example environment file**
```bash
cp .env.example .env
```

2. **Edit the .env file**
```bash
nano .env
```

3. **Fill in your credentials**
```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz123456789
TELEGRAM_CHAT_ID=-1001234567890
DEXSCREENER_URL=https://dexscreener.com/
CHECK_INTERVAL=10
```

## ⚙️ Configuration

All configuration is done through the `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token from BotFather | Required |
| `TELEGRAM_CHAT_ID` | Your Telegram chat/group ID | Required |
| `DEXSCREENER_URL` | DexScreener website URL | `https://dexscreener.com/` |
| `CHECK_INTERVAL` | Seconds between each check | `10` |

Advanced configuration can be done in `config.py` for Selenium options, logging, etc.

## 🚀 Usage

### Start the Bot

**Option 1: Using start script**
```bash
./start.sh
```

**Option 2: Direct Python**
```bash
source venv/bin/activate
python3 token_scraper.py
```

**Option 3: Using systemd service** (if set up)
```bash
sudo systemctl start goddex
```

### Stop the Bot

**Option 1: Using stop script**
```bash
./stop.sh
```

**Option 2: Press Ctrl+C** (if running in foreground)

**Option 3: Using systemd service**
```bash
sudo systemctl stop goddex
```

### View Logs

**Real-time logs**
```bash
tail -f logs/token_monitor.log
```

**Service logs** (if using systemd)
```bash
sudo journalctl -u goddex -f
```

## 🖥️ Running on Server

### Setup as Background Service

1. **Run setup with systemd option**
```bash
./setup.sh
# Answer 'y' when asked about systemd service
```

2. **Verify service is enabled**
```bash
sudo systemctl status goddex
```

3. **Start the service**
```bash
sudo systemctl start goddex
```

4. **Enable auto-start on boot**
```bash
sudo systemctl enable goddex
```

### Service Management Commands

```bash
# Start service
sudo systemctl start goddex

# Stop service
sudo systemctl stop goddex

# Restart service
sudo systemctl restart goddex

# Check status
sudo systemctl status goddex

# View logs
sudo journalctl -u goddex -f

# Disable auto-start
sudo systemctl disable goddex
```

## 🔧 Troubleshooting

### Issue: Bot not detecting new tokens

**Solution:**
1. Check if DexScreener is accessible
2. Verify the CSS class `ds-dex-table-row-new` still exists
3. Check logs: `tail -f logs/token_monitor.log`
4. Try increasing `CHECK_INTERVAL` in `.env`

### Issue: Telegram messages not sending

**Solution:**
1. Verify bot token is correct
2. Verify chat ID is correct
3. Ensure bot is added to the group (for group chats)
4. Check bot permissions in the group
5. Test with: `https://api.telegram.org/bot<token>/getMe`

### Issue: Chrome/Chromium not found

**Solution:**
```bash
# Install Chromium
sudo apt-get install chromium-browser chromium-chromedriver

# Or install Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb
```

### Issue: Permission denied on scripts

**Solution:**
```bash
chmod +x setup.sh start.sh stop.sh
```

### Issue: Service fails to start

**Solution:**
1. Check service logs: `sudo journalctl -u goddex -xe`
2. Verify paths in `goddex.service` file
3. Ensure `.env` file exists and is configured
4. Check file permissions

## 📱 Telegram Message Format

The bot sends messages in the following format:

```
🚀 नया टोकन मिला! / New Token Found! 🚀

💎 टोकन / Token: TokenName (SYMBOL)
⛓️ ब्लॉकचेन / Chain: Ethereum
💰 प्राइस / Price: $0.000123
⏰ एज / Age: 5m
📝 कॉन्ट्रैक्ट / Contract: 0xabcd...
🔗 लिंक / Link: https://dexscreener.com/...
⏱️ समय / Time: 2024-01-15 10:30:45
```

## 📁 Project Structure

```
goddex/
├── token_scraper.py          # Main application
├── config.py                 # Configuration management
├── requirements.txt          # Python dependencies
├── README.md                 # Documentation
├── .env.example              # Environment variables template
├── .env                      # Your configuration (create from .env.example)
├── .gitignore                # Git ignore rules
├── setup.sh                  # Setup script
├── start.sh                  # Start script
├── stop.sh                   # Stop script
├── goddex.service            # Systemd service file
├── logs/                     # Log files directory
│   └── token_monitor.log     # Application logs
├── data/                     # Data storage directory
│   └── sent_tokens.json      # Sent tokens record
└── venv/                     # Python virtual environment
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## ⚠️ Disclaimer

This bot is for educational purposes only. Use responsibly and in accordance with DexScreener's terms of service. The authors are not responsible for any misuse or damages.

---

# Hindi Documentation

## 🌟 अवलोकन

DexScreener Token Monitor एक स्वचालित बॉट है जो [DexScreener](https://dexscreener.com/) पर नए टोकन लिस्टिंग की निरंतर निगरानी करता है और आपके टेलीग्राम ग्रुप में तुरंत सूचना भेजता है। यह बॉट Selenium WebDriver का उपयोग करके वेबसाइट को स्क्रैप करता है और `ds-dex-table-row-new` क्लास वाले टोकन का पता लगाता है।

### मुख्य विशेषताएं
- ⚡ रियल-टाइम मॉनिटरिंग
- 🤖 स्वचालित टेलीग्राम सूचनाएं
- 💾 डुप्लीकेट से बचने के लिए डेटा स्टोरेज
- 🔄 विफलता पर ऑटो-रीस्टार्ट
- 📊 विस्तृत लॉगिंग
- 🐧 Linux सर्वर संगत

## ✨ विशेषताएं

- **रियल-टाइम मॉनिटरिंग**: DexScreener पर नए टोकन के लिए निरंतर स्कैन करता है
- **स्मार्ट डिटेक्शन**: CSS क्लास `ds-dex-table-row-new` का उपयोग करके नए टोकन की पहचान करता है
- **व्यापक डेटा निष्कर्षण**:
  - टोकन नाम/सिंबल
  - ब्लॉकचेन/चेन
  - वर्तमान मूल्य
  - पेयर आयु
  - DexScreener लिंक
  - कॉन्ट्रैक्ट एड्रेस
- **टेलीग्राम इंटीग्रेशन**: 
  - इमोजी के साथ फॉर्मेटेड HTML संदेश
  - तुरंत सूचनाएं
  - API लिमिट से बचने के लिए रेट लिमिटिंग
- **डुप्लीकेट रोकथाम**: भेजे गए टोकन का रिकॉर्ड रखता है
- **एरर हैंडलिंग**: 
  - स्वचालित पुनः प्रयास तर्क
  - WebDriver रिकवरी
  - व्यापक एरर लॉगिंग
- **सर्वर के लिए तैयार**:
  - हेडलेस Chrome सपोर्ट
  - Systemd सर्विस इंटीग्रेशन
  - बूट पर ऑटो-स्टार्ट

## 📋 आवश्यक चीजें

- Python 3.8 या उच्चतर
- pip (Python package manager)
- Chrome या Chromium ब्राउज़र
- Ubuntu/Debian Linux (सर्वर के लिए अनुशंसित)
- टेलीग्राम अकाउंट

## 🛠️ इंस्टॉलेशन

### विधि 1: स्वचालित सेटअप (अनुशंसित)

1. **रिपॉजिटरी क्लोन करें**
```bash
git clone https://github.com/sureshshukla12996/goddex.git
cd goddex
```

2. **सेटअप स्क्रिप्ट चलाएं**
```bash
chmod +x setup.sh
./setup.sh
```

सेटअप स्क्रिप्ट निम्नलिखित करेगी:
- Python3 और pip इंस्टॉल करें
- Chrome/Chromium ब्राउज़र इंस्टॉल करें
- Virtual environment बनाएं
- सभी dependencies इंस्टॉल करें
- आवश्यक डायरेक्टरी बनाएं
- वैकल्पिक रूप से systemd सर्विस सेटअप करें

### विधि 2: मैनुअल सेटअप

1. **रिपॉजिटरी क्लोन करें**
```bash
git clone https://github.com/sureshshukla12996/goddex.git
cd goddex
```

2. **सिस्टम dependencies इंस्टॉल करें**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv chromium-browser
```

3. **Virtual environment बनाएं**
```bash
python3 -m venv venv
source venv/bin/activate
```

4. **Python dependencies इंस्टॉल करें**
```bash
pip install -r requirements.txt
```

5. **डायरेक्टरी बनाएं**
```bash
mkdir -p logs data
```

## 🤖 टेलीग्राम बॉट सेटअप

### चरण 1: टेलीग्राम बॉट बनाएं

1. टेलीग्राम खोलें और **@BotFather** खोजें
2. `/start` कमांड भेजें
3. `/newbot` कमांड भेजें
4. निर्देशों का पालन करें:
   - अपने बॉट के लिए एक नाम चुनें (जैसे, "DexScreener Monitor")
   - एक यूजरनेम चुनें ('bot' से समाप्त होना चाहिए, जैसे, "dexscreener_monitor_bot")
5. **बॉट टोकन सेव करें** - आपको इसकी बाद में आवश्यकता होगी

उदाहरण टोकन: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz123456789`

### चरण 2: अपनी Chat ID प्राप्त करें

#### व्यक्तिगत चैट के लिए:
1. टेलीग्राम पर **@userinfobot** खोजें
2. `/start` कमांड भेजें
3. अपनी **User ID** कॉपी करें

#### ग्रुप चैट के लिए:
1. अपने बॉट को ग्रुप में जोड़ें
2. ग्रुप में कोई भी संदेश भेजें
3. देखें: `https://api.telegram.org/bot<YourBOTToken>/getUpdates`
4. रिस्पांस में `"chat":{"id":-123456789` देखें
5. Chat ID कॉपी करें (ग्रुप के लिए माइनस साइन सहित)

### चरण 3: Environment Variables कॉन्फ़िगर करें

1. **उदाहरण environment फ़ाइल कॉपी करें**
```bash
cp .env.example .env
```

2. **.env फ़ाइल एडिट करें**
```bash
nano .env
```

3. **अपनी क्रेडेंशियल्स भरें**
```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz123456789
TELEGRAM_CHAT_ID=-1001234567890
DEXSCREENER_URL=https://dexscreener.com/
CHECK_INTERVAL=10
```

## ⚙️ कॉन्फ़िगरेशन

सभी कॉन्फ़िगरेशन `.env` फ़ाइल के माध्यम से किया जाता है:

| वेरिएबल | विवरण | डिफ़ॉल्ट |
|----------|--------|---------|
| `TELEGRAM_BOT_TOKEN` | BotFather से आपका Telegram बॉट टोकन | आवश्यक |
| `TELEGRAM_CHAT_ID` | आपकी Telegram चैट/ग्रुप ID | आवश्यक |
| `DEXSCREENER_URL` | DexScreener वेबसाइट URL | `https://dexscreener.com/` |
| `CHECK_INTERVAL` | प्रत्येक चेक के बीच सेकंड | `10` |

उन्नत कॉन्फ़िगरेशन Selenium options, logging आदि के लिए `config.py` में किया जा सकता है।

## 🚀 उपयोग

### बॉट शुरू करें

**विकल्प 1: start स्क्रिप्ट का उपयोग करें**
```bash
./start.sh
```

**विकल्प 2: सीधे Python**
```bash
source venv/bin/activate
python3 token_scraper.py
```

**विकल्प 3: systemd सर्विस का उपयोग करें** (यदि सेटअप हो)
```bash
sudo systemctl start goddex
```

### बॉट बंद करें

**विकल्प 1: stop स्क्रिप्ट का उपयोग करें**
```bash
./stop.sh
```

**विकल्प 2: Ctrl+C दबाएं** (यदि foreground में चल रहा हो)

**विकल्प 3: systemd सर्विस का उपयोग करें**
```bash
sudo systemctl stop goddex
```

### लॉग देखें

**रियल-टाइम लॉग**
```bash
tail -f logs/token_monitor.log
```

**सर्विस लॉग** (systemd उपयोग करते समय)
```bash
sudo journalctl -u goddex -f
```

## 🖥️ सर्वर पर चलाना

### बैकग्राउंड सर्विस के रूप में सेटअप करें

1. **systemd विकल्प के साथ सेटअप चलाएं**
```bash
./setup.sh
# systemd सर्विस के बारे में पूछे जाने पर 'y' उत्तर दें
```

2. **सर्विस enabled है, यह सत्यापित करें**
```bash
sudo systemctl status goddex
```

3. **सर्विस शुरू करें**
```bash
sudo systemctl start goddex
```

4. **बूट पर ऑटो-स्टार्ट सक्षम करें**
```bash
sudo systemctl enable goddex
```

### सर्विस मैनेजमेंट कमांड

```bash
# सर्विस शुरू करें
sudo systemctl start goddex

# सर्विस बंद करें
sudo systemctl stop goddex

# सर्विस रीस्टार्ट करें
sudo systemctl restart goddex

# स्थिति चेक करें
sudo systemctl status goddex

# लॉग देखें
sudo journalctl -u goddex -f

# ऑटो-स्टार्ट अक्षम करें
sudo systemctl disable goddex
```

## 🔧 समस्या निवारण

### समस्या: बॉट नए टोकन का पता नहीं लगा रहा

**समाधान:**
1. चेक करें कि DexScreener सुलभ है
2. सत्यापित करें कि CSS क्लास `ds-dex-table-row-new` अभी भी मौजूद है
3. लॉग चेक करें: `tail -f logs/token_monitor.log`
4. `.env` में `CHECK_INTERVAL` बढ़ाने का प्रयास करें

### समस्या: टेलीग्राम संदेश नहीं भेज रहा

**समाधान:**
1. सत्यापित करें कि बॉट टोकन सही है
2. सत्यापित करें कि चैट ID सही है
3. सुनिश्चित करें कि बॉट ग्रुप में जोड़ा गया है (ग्रुप चैट के लिए)
4. ग्रुप में बॉट अनुमतियां चेक करें
5. परीक्षण के साथ: `https://api.telegram.org/bot<token>/getMe`

### समस्या: Chrome/Chromium नहीं मिला

**समाधान:**
```bash
# Chromium इंस्टॉल करें
sudo apt-get install chromium-browser chromium-chromedriver

# या Chrome इंस्टॉल करें
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb
```

### समस्या: स्क्रिप्ट पर Permission denied

**समाधान:**
```bash
chmod +x setup.sh start.sh stop.sh
```

### समस्या: सर्विस शुरू नहीं हो रही

**समाधान:**
1. सर्विस लॉग चेक करें: `sudo journalctl -u goddex -xe`
2. `goddex.service` फ़ाइल में पाथ सत्यापित करें
3. सुनिश्चित करें कि `.env` फ़ाइल मौजूद है और कॉन्फ़िगर की गई है
4. फ़ाइल अनुमतियां चेक करें

## 📱 टेलीग्राम संदेश फॉर्मेट

बॉट निम्नलिखित फॉर्मेट में संदेश भेजता है:

```
🚀 नया टोकन मिला! / New Token Found! 🚀

💎 टोकन / Token: TokenName (SYMBOL)
⛓️ ब्लॉकचेन / Chain: Ethereum
💰 प्राइस / Price: $0.000123
⏰ एज / Age: 5m
📝 कॉन्ट्रैक्ट / Contract: 0xabcd...
🔗 लिंक / Link: https://dexscreener.com/...
⏱️ समय / Time: 2024-01-15 10:30:45
```

## 📁 प्रोजेक्ट संरचना

```
goddex/
├── token_scraper.py          # मुख्य एप्लिकेशन
├── config.py                 # कॉन्फ़िगरेशन प्रबंधन
├── requirements.txt          # Python dependencies
├── README.md                 # डॉक्युमेंटेशन
├── .env.example              # Environment variables टेम्पलेट
├── .env                      # आपका कॉन्फ़िगरेशन (.env.example से बनाएं)
├── .gitignore                # Git ignore नियम
├── setup.sh                  # सेटअप स्क्रिप्ट
├── start.sh                  # स्टार्ट स्क्रिप्ट
├── stop.sh                   # स्टॉप स्क्रिप्ट
├── goddex.service            # Systemd सर्विस फ़ाइल
├── logs/                     # लॉग फ़ाइल डायरेक्टरी
│   └── token_monitor.log     # एप्लिकेशन लॉग
├── data/                     # डेटा स्टोरेज डायरेक्टरी
│   └── sent_tokens.json      # भेजे गए टोकन रिकॉर्ड
└── venv/                     # Python virtual environment
```

## 🤝 योगदान

योगदान का स्वागत है! कृपया बेझिझक एक Pull Request सबमिट करें।

## 📄 लाइसेंस

यह प्रोजेक्ट MIT लाइसेंस के तहत लाइसेंस प्राप्त है।

## ⚠️ अस्वीकरण

यह बॉट केवल शैक्षिक उद्देश्यों के लिए है। जिम्मेदारी से उपयोग करें और DexScreener की सेवा की शर्तों के अनुसार। लेखक किसी भी दुरुपयोग या क्षति के लिए जिम्मेदार नहीं हैं।

---

<div align="center">

**Made with ❤️ for the Crypto Community**

**क्रिप्टो समुदाय के लिए ❤️ से बनाया गया**

</div>