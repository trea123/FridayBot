#!/bin/bash

# Global Constants (ONLY NEED TO CHANGE THESE)
PROJECT_NAME=FridayBot
SERVICE_NAME=fridaybot

###################################################

# Path Constants
PROJECT_PATH=/opt/$PROJECT_NAME
TOKEN_PATH=/etc/$PROJECT_NAME
SYSTEMD_PATH=/usr/lib/systemd/system/$SERVICE_NAME.service

# Checks if user is root when running install
if [ `id -u` != 0 ]; then
    echo "[!] Must be run as root" >&2
    exit 1
fi

# Wipes old project and recreates directory
echo "[*] Wiping old project directory" &&
rm -rf $PROJECT_PATH &&

# Wipes old token configuration directory
echo "[*] Wiping old token configuration directory" &&
rm -rf $TOKEN_PATH &&

# Wipes old systemd service
echo "[*] Wiping old systemd service" &&
systemctl disable $SERVICE_NAME 2>/dev/null
systemctl kill -s SIGKILL $SERVICE_NAME 2>/dev/null
systemctl stop $SERVICE_NAME 2>/dev/null
rm -f $SYSTEMD_PATH &&
echo "[+] Finished"
