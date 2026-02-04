"""
DexScreener Token Monitor Bot
DexScreener टोकन मॉनिटर बॉट
यह स्क्रिप्ट DexScreener पर नए टोकन की निगरानी करता है और टेलीग्राम पर सूचना भेजता है
This script monitors DexScreener for new tokens and sends notifications to Telegram
"""

import json
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from telegram import Bot
from telegram.error import TelegramError
import asyncio

import config


class TokenMonitor:
    """DexScreener टोकन मॉनिटर क्लास / DexScreener Token Monitor Class"""
    
    def __init__(self):
        """इनिशियलाइज़ेशन / Initialization"""
        self.setup_logging()
        self.setup_directories()
        self.sent_tokens = self.load_sent_tokens()
        self.driver = None
        self.bot = None
        self.logger.info("टोकन मॉनिटर शुरू हो रहा है / Token Monitor initializing")
        
    def setup_logging(self):
        """लॉगिंग सेटअप करें / Setup logging"""
        log_dir = Path(config.LOG_DIR)
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / config.LOG_FILE
        
        logging.basicConfig(
            level=getattr(logging, config.LOG_LEVEL),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def setup_directories(self):
        """आवश्यक डायरेक्टरी बनाएं / Create necessary directories"""
        Path(config.DATA_DIR).mkdir(exist_ok=True)
        Path(config.LOG_DIR).mkdir(exist_ok=True)
        
    def load_sent_tokens(self):
        """पहले से भेजे गए टोकन लोड करें / Load previously sent tokens"""
        sent_tokens_path = Path(config.DATA_DIR) / config.SENT_TOKENS_FILE
        try:
            if sent_tokens_path.exists():
                with open(sent_tokens_path, 'r') as f:
                    tokens = json.load(f)
                    self.logger.info(f"लोड किए गए टोकन: {len(tokens)} / Loaded tokens: {len(tokens)}")
                    return set(tokens)
        except Exception as e:
            self.logger.error(f"टोकन लोड करने में त्रुटि / Error loading tokens: {e}")
        return set()
    
    def save_sent_tokens(self):
        """भेजे गए टोकन सेव करें / Save sent tokens"""
        sent_tokens_path = Path(config.DATA_DIR) / config.SENT_TOKENS_FILE
        try:
            with open(sent_tokens_path, 'w') as f:
                json.dump(list(self.sent_tokens), f, indent=2)
            self.logger.debug("टोकन सेव किए गए / Tokens saved")
        except Exception as e:
            self.logger.error(f"टोकन सेव करने में त्रुटि / Error saving tokens: {e}")
    
    def setup_selenium(self):
        """Selenium WebDriver सेटअप करें / Setup Selenium WebDriver"""
        try:
            chrome_options = Options()
            
            if config.SELENIUM_OPTIONS['headless']:
                chrome_options.add_argument('--headless')
            if config.SELENIUM_OPTIONS['disable_gpu']:
                chrome_options.add_argument('--disable-gpu')
            if config.SELENIUM_OPTIONS['no_sandbox']:
                chrome_options.add_argument('--no-sandbox')
            if config.SELENIUM_OPTIONS['disable_dev_shm_usage']:
                chrome_options.add_argument('--disable-dev-shm-usage')
            if config.SELENIUM_OPTIONS['window_size']:
                chrome_options.add_argument(f"--window-size={config.SELENIUM_OPTIONS['window_size']}")
            
            # अतिरिक्त ऑप्शन / Additional options
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.logger.info("Selenium WebDriver सेटअप सफल / Selenium WebDriver setup successful")
            return True
        except Exception as e:
            self.logger.error(f"Selenium सेटअप में त्रुटि / Error setting up Selenium: {e}")
            return False
    
    def setup_telegram(self):
        """टेलीग्राम बॉट सेटअप करें / Setup Telegram Bot"""
        try:
            if not config.TELEGRAM_BOT_TOKEN or not config.TELEGRAM_CHAT_ID:
                self.logger.error("टेलीग्राम कॉन्फ़िगरेशन नहीं मिला / Telegram configuration not found")
                return False
            
            self.bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
            self.logger.info("टेलीग्राम बॉट सेटअप सफल / Telegram Bot setup successful")
            return True
        except Exception as e:
            self.logger.error(f"टेलीग्राम सेटअप में त्रुटि / Error setting up Telegram: {e}")
            return False
    
    async def send_telegram_message(self, message):
        """टेलीग्राम संदेश भेजें / Send Telegram message"""
        try:
            await self.bot.send_message(
                chat_id=config.TELEGRAM_CHAT_ID,
                text=message,
                parse_mode='HTML',
                disable_web_page_preview=False
            )
            self.logger.info("टेलीग्राम संदेश भेजा गया / Telegram message sent")
            return True
        except TelegramError as e:
            self.logger.error(f"टेलीग्राम संदेश भेजने में त्रुटि / Error sending Telegram message: {e}")
            return False
    
    def extract_token_info(self, row_element):
        """टोकन जानकारी निकालें / Extract token information"""
        try:
            html = row_element.get_attribute('innerHTML')
            soup = BeautifulSoup(html, 'html.parser')
            
            # टोकन लिंक निकालें / Extract token link
            link_elem = row_element.find_element(By.TAG_NAME, 'a')
            token_url = link_elem.get_attribute('href') if link_elem else None
            
            # टोकन नाम/सिंबल / Token name/symbol
            token_name = "N/A"
            try:
                name_elem = row_element.find_element(By.CSS_SELECTOR, '.ds-dex-table-row-col-token')
                token_name = name_elem.text.strip()
            except:
                pass
            
            # ब्लॉकचेन/चेन / Blockchain/chain
            chain = "N/A"
            try:
                chain_elem = row_element.find_element(By.CSS_SELECTOR, '.ds-dex-table-row-badge')
                chain = chain_elem.text.strip()
            except:
                pass
            
            # प्राइस / Price
            price = "N/A"
            try:
                price_elem = row_element.find_element(By.CSS_SELECTOR, '.ds-dex-table-row-col-price')
                price = price_elem.text.strip()
            except:
                pass
            
            # पेयर एज / Pair age
            age = "N/A"
            try:
                age_elem = row_element.find_element(By.CSS_SELECTOR, '.ds-dex-table-row-age')
                age = age_elem.text.strip()
            except:
                pass
            
            # कॉन्ट्रैक्ट एड्रेस (यदि उपलब्ध हो) / Contract address (if available)
            contract = "N/A"
            try:
                if token_url:
                    # URL से कॉन्ट्रैक्ट एड्रेस निकालें / Extract contract from URL
                    parts = token_url.split('/')
                    if len(parts) > 0:
                        contract = parts[-1]
            except:
                pass
            
            return {
                'name': token_name,
                'chain': chain,
                'price': price,
                'age': age,
                'url': token_url,
                'contract': contract,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception as e:
            self.logger.error(f"टोकन जानकारी निकालने में त्रुटि / Error extracting token info: {e}")
            return None
    
    def format_message(self, token_info):
        """टेलीग्राम संदेश फॉर्मेट करें / Format Telegram message"""
        message = f"""
🚀 <b>नया टोकन मिला! / New Token Found!</b> 🚀

💎 <b>टोकन / Token:</b> {token_info['name']}
⛓️ <b>ब्लॉकचेन / Chain:</b> {token_info['chain']}
💰 <b>प्राइस / Price:</b> {token_info['price']}
⏰ <b>एज / Age:</b> {token_info['age']}
📝 <b>कॉन्ट्रैक्ट / Contract:</b> <code>{token_info['contract']}</code>

🔗 <b>लिंक / Link:</b> {token_info['url']}

⏱️ <b>समय / Time:</b> {token_info['timestamp']}
"""
        return message.strip()
    
    def scan_for_new_tokens(self):
        """नए टोकन के लिए स्कैन करें / Scan for new tokens"""
        try:
            # पेज लोड करें / Load page
            self.driver.get(config.DEXSCREENER_URL)
            
            # पेज लोड होने का इंतज़ार करें / Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'body'))
            )
            
            # थोड़ा और इंतज़ार करें / Wait a bit more
            time.sleep(3)
            
            # नए टोकन खोजें / Find new tokens
            new_rows = self.driver.find_elements(By.CLASS_NAME, 'ds-dex-table-row-new')
            
            self.logger.info(f"मिले नए टोकन: {len(new_rows)} / Found new tokens: {len(new_rows)}")
            
            new_tokens_found = []
            
            for row in new_rows:
                try:
                    token_info = self.extract_token_info(row)
                    if token_info and token_info['url']:
                        # चेक करें कि पहले से नहीं भेजा गया / Check if not already sent
                        token_id = token_info['url']
                        if token_id not in self.sent_tokens:
                            new_tokens_found.append(token_info)
                            self.sent_tokens.add(token_id)
                            self.logger.info(f"नया टोकन: {token_info['name']} / New token: {token_info['name']}")
                except Exception as e:
                    self.logger.error(f"टोकन प्रोसेस करने में त्रुटि / Error processing token: {e}")
                    continue
            
            return new_tokens_found
            
        except TimeoutException:
            self.logger.warning("पेज लोड टाइमआउट / Page load timeout")
            return []
        except WebDriverException as e:
            self.logger.error(f"WebDriver त्रुटि / WebDriver error: {e}")
            return []
        except Exception as e:
            self.logger.error(f"स्कैन करने में त्रुटि / Error scanning: {e}")
            return []
    
    async def process_and_send_tokens(self, tokens):
        """टोकन प्रोसेस करें और भेजें / Process and send tokens"""
        for token_info in tokens:
            try:
                message = self.format_message(token_info)
                success = await self.send_telegram_message(message)
                if success:
                    self.logger.info(f"संदेश भेजा गया: {token_info['name']} / Message sent: {token_info['name']}")
                    # रेट लिमिटिंग / Rate limiting
                    await asyncio.sleep(1)
                else:
                    self.logger.warning(f"संदेश भेजने में विफल: {token_info['name']} / Failed to send: {token_info['name']}")
            except Exception as e:
                self.logger.error(f"टोकन भेजने में त्रुटि / Error sending token: {e}")
    
    async def run(self):
        """मुख्य लूप चलाएं / Run main loop"""
        self.logger.info("मॉनिटर शुरू हो रहा है / Monitor starting")
        
        # सेटअप / Setup
        if not self.setup_selenium():
            self.logger.error("Selenium सेटअप विफल / Selenium setup failed")
            return
        
        if not self.setup_telegram():
            self.logger.error("टेलीग्राम सेटअप विफल / Telegram setup failed")
            return
        
        # स्वागत संदेश / Welcome message
        welcome_msg = "🤖 <b>DexScreener टोकन मॉनिटर शुरू हुआ!</b>\n\n✅ बॉट सक्रिय है और नए टोकन की निगरानी कर रहा है।\n\n🤖 <b>DexScreener Token Monitor Started!</b>\n\n✅ Bot is active and monitoring for new tokens."
        await self.send_telegram_message(welcome_msg)
        
        retry_count = 0
        
        try:
            while True:
                try:
                    self.logger.info("नए टोकन के लिए स्कैन कर रहे हैं / Scanning for new tokens")
                    
                    # स्कैन करें / Scan
                    new_tokens = self.scan_for_new_tokens()
                    
                    # भेजें / Send
                    if new_tokens:
                        await self.process_and_send_tokens(new_tokens)
                        # सेव करें / Save
                        self.save_sent_tokens()
                        retry_count = 0  # रीसेट करें / Reset
                    
                    # इंतज़ार करें / Wait
                    self.logger.info(f"{config.CHECK_INTERVAL} सेकंड इंतज़ार कर रहे हैं / Waiting {config.CHECK_INTERVAL} seconds")
                    await asyncio.sleep(config.CHECK_INTERVAL)
                    
                except Exception as e:
                    retry_count += 1
                    self.logger.error(f"लूप में त्रुटि (प्रयास {retry_count}/{config.MAX_RETRIES}) / Error in loop (attempt {retry_count}/{config.MAX_RETRIES}): {e}")
                    
                    if retry_count >= config.MAX_RETRIES:
                        self.logger.error("अधिकतम पुनः प्रयास पहुंच गए / Maximum retries reached")
                        # WebDriver रीसेट करें / Reset WebDriver
                        if self.driver:
                            self.driver.quit()
                        self.setup_selenium()
                        retry_count = 0
                    
                    await asyncio.sleep(config.RETRY_DELAY)
                    
        except KeyboardInterrupt:
            self.logger.info("बंद हो रहा है / Shutting down")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """संसाधन साफ करें / Cleanup resources"""
        self.logger.info("संसाधन साफ कर रहे हैं / Cleaning up resources")
        if self.driver:
            self.driver.quit()
        self.save_sent_tokens()


def main():
    """मुख्य फंक्शन / Main function"""
    monitor = TokenMonitor()
    asyncio.run(monitor.run())


if __name__ == "__main__":
    main()
