#!/bin/bash

# DexScreener Token Monitor Setup Script
# DexScreener टोकन मॉनिटर सेटअप स्क्रिप्ट

echo "================================================"
echo "DexScreener Token Monitor Setup"
echo "DexScreener टोकन मॉनिटर सेटअप"
echo "================================================"

# रंग / Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# फंक्शन: संदेश प्रिंट करें / Function: Print message
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}➜ $1${NC}"
}

# चेक करें कि स्क्रिप्ट root के रूप में चल रही है / Check if running as root
if [ "$EUID" -eq 0 ]; then 
    print_info "root के रूप में चल रहा है / Running as root"
    SUDO=""
else
    SUDO="sudo"
fi

# 1. सिस्टम अपडेट करें / Update system
print_info "सिस्टम अपडेट कर रहे हैं / Updating system..."
$SUDO apt-get update -qq

# 2. Python3 और pip इंस्टॉल करें / Install Python3 and pip
print_info "Python3 और pip इंस्टॉल कर रहे हैं / Installing Python3 and pip..."
$SUDO apt-get install -y python3 python3-pip python3-venv > /dev/null 2>&1
if [ $? -eq 0 ]; then
    print_success "Python3 इंस्टॉल हो गया / Python3 installed"
else
    print_error "Python3 इंस्टॉल विफल / Python3 installation failed"
    exit 1
fi

# 3. Chrome/Chromium इंस्टॉल करें / Install Chrome/Chromium
print_info "Chrome/Chromium इंस्टॉल कर रहे हैं / Installing Chrome/Chromium..."
if ! command -v google-chrome &> /dev/null && ! command -v chromium-browser &> /dev/null; then
    # Chromium इंस्टॉल करने का प्रयास / Try to install Chromium
    $SUDO apt-get install -y chromium-browser chromium-chromedriver > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        # यदि Chromium विफल हो, तो Chrome इंस्टॉल करें / If Chromium fails, install Chrome
        print_info "Chrome इंस्टॉल कर रहे हैं / Installing Chrome..."
        wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
        $SUDO apt-get install -y ./google-chrome-stable_current_amd64.deb > /dev/null 2>&1
        rm google-chrome-stable_current_amd64.deb
    fi
    print_success "Browser इंस्टॉल हो गया / Browser installed"
else
    print_success "Browser पहले से इंस्टॉल है / Browser already installed"
fi

# 4. Virtual Environment बनाएं / Create virtual environment
print_info "Virtual environment बना रहे हैं / Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_success "Virtual environment बन गया / Virtual environment created"
else
    print_success "Virtual environment पहले से मौजूद है / Virtual environment already exists"
fi

# 5. Virtual environment activate करें और dependencies इंस्टॉल करें
# Activate virtual environment and install dependencies
print_info "Dependencies इंस्टॉल कर रहे हैं / Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
if [ $? -eq 0 ]; then
    print_success "Dependencies इंस्टॉल हो गए / Dependencies installed"
else
    print_error "Dependencies इंस्टॉल विफल / Dependencies installation failed"
    exit 1
fi

# 6. डायरेक्टरी बनाएं / Create directories
print_info "डायरेक्टरी बना रहे हैं / Creating directories..."
mkdir -p logs data
print_success "डायरेक्टरी बन गए / Directories created"

# 7. .env फ़ाइल चेक करें / Check .env file
if [ ! -f ".env" ]; then
    print_info ".env फ़ाइल नहीं मिली, .env.example से कॉपी कर रहे हैं / .env file not found, copying from .env.example..."
    cp .env.example .env
    print_success ".env फ़ाइल बन गई / .env file created"
    print_info "कृपया .env फ़ाइल में अपना Telegram bot token और chat ID भरें"
    print_info "Please fill in your Telegram bot token and chat ID in .env file"
else
    print_success ".env फ़ाइल मौजूद है / .env file exists"
fi

# 8. स्क्रिप्ट को executable बनाएं / Make scripts executable
print_info "स्क्रिप्ट को executable बना रहे हैं / Making scripts executable..."
chmod +x start.sh stop.sh
print_success "स्क्रिप्ट executable हो गए / Scripts are executable"

# 9. Systemd service सेटअप (वैकल्पिक) / Systemd service setup (optional)
print_info "Systemd service सेटअप करें? / Setup systemd service? (y/n)"
read -r setup_service

if [ "$setup_service" = "y" ] || [ "$setup_service" = "Y" ]; then
    print_info "Systemd service सेटअप कर रहे हैं / Setting up systemd service..."
    
    # Service file में पाथ अपडेट करें / Update paths in service file
    CURRENT_DIR=$(pwd)
    SERVICE_FILE="goddex.service"
    
    # Service file को systemd में कॉपी करें / Copy service file to systemd
    $SUDO cp $SERVICE_FILE /etc/systemd/system/
    
    # Service file में WorkingDirectory अपडेट करें / Update WorkingDirectory in service file
    $SUDO sed -i "s|/path/to/goddex|$CURRENT_DIR|g" /etc/systemd/system/$SERVICE_FILE
    $SUDO sed -i "s|User=youruser|User=$USER|g" /etc/systemd/system/$SERVICE_FILE
    
    # Systemd reload करें / Reload systemd
    $SUDO systemctl daemon-reload
    $SUDO systemctl enable goddex.service
    
    print_success "Systemd service सेटअप हो गई / Systemd service setup complete"
    print_info "Service शुरू करने के लिए: sudo systemctl start goddex"
    print_info "To start service: sudo systemctl start goddex"
else
    print_info "Systemd service सेटअप छोड़ दिया / Systemd service setup skipped"
fi

echo ""
echo "================================================"
print_success "सेटअप पूर्ण! / Setup Complete!"
echo "================================================"
echo ""
print_info "अगले कदम / Next Steps:"
echo "1. .env फ़ाइल में अपना Telegram configuration भरें"
echo "   Edit .env file with your Telegram configuration"
echo ""
echo "2. बॉट शुरू करने के लिए चलाएं / To start the bot, run:"
echo "   ./start.sh"
echo ""
echo "3. बॉट बंद करने के लिए चलाएं / To stop the bot, run:"
echo "   ./stop.sh"
echo ""
echo "4. या systemd service का उपयोग करें / Or use systemd service:"
echo "   sudo systemctl start goddex"
echo "   sudo systemctl stop goddex"
echo "   sudo systemctl status goddex"
echo ""
