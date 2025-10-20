#!/bin/bash
set -e

APP_DIR="/home/quangminh/app"
LOG_FILE="/home/quangminh/deploy/deploy.log"

echo "=== Start $(date) ===" >> $LOG_FILE

cd $APP_DIR
git fetch origin
git reset --hard origin/main

pip3 install -r requirements.txt --break-system-packages >> $LOG_FILE 2>&1

sudo systemctl restart app.service

echo "=== Done $(date) ===" >> $LOG_FILE
