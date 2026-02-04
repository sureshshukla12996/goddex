#!/bin/bash

# DexScreener Token Monitor Start Script
# DexScreener टोकन मॉनिटर स्टार्ट स्क्रिप्ट

echo "🚀 DexScreener Token Monitor शुरू हो रहा है / Starting..."

# Virtual environment चेक करें / Check virtual environment
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment नहीं मिला / Virtual environment not found"
    echo "कृपया पहले setup.sh चलाएं / Please run setup.sh first"
    exit 1
fi

# .env फ़ाइल चेक करें / Check .env file
if [ ! -f ".env" ]; then
    echo "❌ .env फ़ाइल नहीं मिली / .env file not found"
    echo "कृपया .env.example से .env बनाएं और configuration भरें"
    echo "Please create .env from .env.example and fill in configuration"
    exit 1
fi

# Virtual environment activate करें / Activate virtual environment
source venv/bin/activate

# बॉट चलाएं / Run bot
echo "✅ बॉट शुरू हो गया / Bot started"
echo "बंद करने के लिए Ctrl+C दबाएं / Press Ctrl+C to stop"
echo ""

python3 token_scraper.py
