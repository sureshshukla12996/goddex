#!/bin/bash

# DexScreener Token Monitor Stop Script
# DexScreener टोकन मॉनिटर स्टॉप स्क्रिप्ट

echo "🛑 DexScreener Token Monitor बंद हो रहा है / Stopping..."

# Process ढूंढें और बंद करें / Find and stop process
PID=$(pgrep -f "python3 token_scraper.py")

if [ -z "$PID" ]; then
    echo "⚠️  कोई चल रही प्रक्रिया नहीं मिली / No running process found"
    exit 0
fi

# Process को बंद करें / Stop the process
kill $PID

# इंतज़ार करें / Wait
sleep 2

# चेक करें कि बंद हो गया / Check if stopped
if pgrep -f "python3 token_scraper.py" > /dev/null; then
    echo "⚠️  प्रक्रिया अभी भी चल रही है, force kill कर रहे हैं / Process still running, force killing..."
    kill -9 $PID
fi

echo "✅ बॉट बंद हो गया / Bot stopped"
