#!/bin/bash

# Global Constants
PROJECT_PATH=/opt/DiscordBot
TOKEN_PATH=/etc/DiscordBot
SYSTEMD_PATH=/usr/lib/systemd/system/discordbot.service

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
systemctl disable discordbot 2>/dev/null
systemctl kill -s SIGKILL discordbot 2>/dev/null
systemctl stop discordbot 2>/dev/null
rm -f $SYSTEMD_PATH &&
echo "[+] Finished"
