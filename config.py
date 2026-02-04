"""
Configuration file for DexScreener Token Monitor
DexScreener टोकन मॉनिटर के लिए कॉन्फ़िगरेशन फ़ाइल
"""

import os
from dotenv import load_dotenv

# .env फ़ाइल लोड करें / Load .env file
load_dotenv()

# Telegram Configuration / टेलीग्राम कॉन्फ़िगरेशन
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')

# DexScreener Configuration / DexScreener कॉन्फ़िगरेशन
DEXSCREENER_URL = os.getenv('DEXSCREENER_URL', 'https://dexscreener.com/new-pairs?rankBy=pairAge&order=asc')

# Monitoring Configuration / मॉनिटरिंग कॉन्फ़िगरेशन
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', '10'))  # सेकंड में / in seconds

# Selenium Configuration / Selenium कॉन्फ़िगरेशन
SELENIUM_OPTIONS = {
    'headless': True,  # हेडलेस मोड (GUI के बिना) / Headless mode (without GUI)
    'disable_gpu': True,
    'no_sandbox': True,
    'disable_dev_shm_usage': True,
    'window_size': '1920,1080',
}

# Logging Configuration / लॉगिंग कॉन्फ़िगरेशन
LOG_DIR = 'logs'
LOG_FILE = 'token_monitor.log'
LOG_LEVEL = 'INFO'

# Data Storage Configuration / डेटा स्टोरेज कॉन्फ़िगरेशन
DATA_DIR = 'data'
SENT_TOKENS_FILE = 'sent_tokens.json'

# Rate Limiting / रेट लिमिटिंग
MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))  # अधिकतम पुनः प्रयास / Maximum retries
RETRY_DELAY = 5  # सेकंड में देरी / Delay in seconds
PAGE_LOAD_TIMEOUT = int(os.getenv('PAGE_LOAD_TIMEOUT', '15'))  # पेज लोड टाइमआउट / Page load timeout

# Display Configuration / डिस्प्ले कॉन्फ़िगरेशन
CONTRACT_ADDRESS_DISPLAY_LENGTH = 20  # कॉन्ट्रैक्ट एड्रेस प्रदर्शन लंबाई / Contract address display length
DYNAMIC_CONTENT_WAIT = 3  # डायनामिक कंटेंट के लिए इंतज़ार (सेकंड) / Dynamic content wait (seconds)
