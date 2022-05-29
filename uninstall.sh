#!/bin/bash

# Global Constants
PROJECT_PATH=/opt/FridayBot
TOKEN_PATH=/etc/FridayBot
SYSTEMD_PATH=/usr/lib/systemd/system/fridaybot.service

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
systemctl disable fridaybot 2>/dev/null
systemctl kill -s SIGKILL fridaybot 2>/dev/null
systemctl stop fridaybot 2>/dev/null
rm -f $SYSTEMD_PATH &&
echo "[+] Finished"
