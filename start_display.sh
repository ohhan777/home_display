#!/bin/bash
# Home Display Startup Script

# Wait for X server to be ready
sleep 5

# Disable DPMS and screen blanking
export DISPLAY=:0
xset -dpms
xset s off
xset s noblank

echo "DPMS and screen blanking disabled"

# Start the home display application
cd /home/pi/home_display
python3 home_display.py

echo "Home Display started"
