#!/bin/bash

# Project Path Constants
PROJECT_PATH=/opt/DiscordBot
PROJECT_ENTRY=${PROJECT_PATH}/bot.py
PROJECT_REQUIREMENTS=${PROJECT_PATH}/requirements.txt

# Virtual Environment Path Constants
VENV_PATH=${PROJECT_PATH}/venv
VENV_PYTHON=${VENV_PATH}/bin/python
VENV_ACTIVATE=${VENV_PATH}/bin/activate

# Current Path Constants
CURRENT_PATH=`pwd -P`
CURRENT_ENTRY=${CURRENT_PATH}/bot.py
CURRENT_REQUIREMENTS=${CURRENT_PATH}/requirements.txt

# Token Path Constants
TOKEN_PATH=/etc/DiscordBot
TOKEN_FILE=${TOKEN_PATH}/token.txt

# Systemd Service Path Constant
SYSTEMD_PATH=/usr/lib/systemd/system/discordbot.service

# Checks if user is root when running install
if [ `id -u` != 0 ]; then
    echo "[!] Must be run as root" >&2
    exit 1
fi

# Wipes old project and recreates directory
echo "[*] Wiping old project and recreating directory" &&
rm -rf $PROJECT_PATH &&
mkdir -p $PROJECT_PATH &&

# Installs a python3 virtual environment to the project path
echo "[*] Installing a python3 virtual environment to the project path" &&
python3 -m venv $VENV_PATH
if [ $? -ne 0 ]; then
    virtualenv $VENV_PATH
    if [ $? -ne 0 ]; then
        echo "[!] Failed to create Python virtual environment" >&2
        exit 2
    fi
fi

# Copy the DiscordBot source code to the project path
echo "[*] Copying the DiscordBot source code to the project path" &&
cp $CURRENT_ENTRY $PROJECT_PATH &&
cp $CURRENT_REQUIREMENTS $PROJECT_PATH &&

# Lock down the project permissions and ownership
echo "[*] Locking down the project permissions and ownership" &&
chown -R root:root $PROJECT_PATH &&
chmod 700 $PROJECT_PATH &&
chmod 600 $PROJECT_ENTRY &&

# Activate the Python virtual environment and install dependencies
echo "[*] Activating the Python virtual environment and installing dependencies" &&
source $VENV_ACTIVATE &&
pip install --upgrade pip &&
pip install -r $PROJECT_REQUIREMENTS
if [ $? -ne 0 ]; then
    echo "[!] Failed to install required packages." >&2
    exit 3
fi

# Clean up the unnecessary requirements file
echo "[*] Cleaning up the unnecessary requirements file" &&
rm -f $PROJECT_REQUIREMENTS &&

# Wipes old token configuration directory and recreates directory
echo "[*] Wiping old token configuration directory and recreating directory" &&
rm -rf $TOKEN_PATH &&
mkdir -p $TOKEN_PATH &&

# Query user for token
echo -n "[*] Enter the bot token: "
read BOT_TOKEN

# Save the token to configuration file
echo "[*] Saving the token to configuration file" &&
echo $BOT_TOKEN > $TOKEN_FILE &&
chown -R root:root $TOKEN_PATH &&
chmod 700 $TOKEN_PATH &&
chmod 600 $TOKEN_FILE &&

# Wipes old systemd service and recreates the service to manage the bot
echo "[*] Wiping old systemd service and recreating the service to manage the bot" &&
systemctl kill -s SIGKILL discordbot 2>/dev/null
systemctl stop discordbot 2>/dev/null
rm -f $SYSTEMD_PATH &&
cat << EOF > $SYSTEMD_PATH
[Unit]
Description="Discord Bot"

[Service]
WorkingDirectory=${PROJECT_PATH}
ExecStart=${VENV_PYTHON} ${PROJECT_ENTRY} --prod
Restart=always
RestartSec=2
TimeoutStopSec=0

[Install]
WantedBy=multi-user.target
EOF

# Enables automatic startup on boot and starts the service for this instance
echo "[*] Enabling automatic startup on boot and starting the service for this instance" &&
systemctl enable discordbot
systemctl start discordbot
echo "[+] Finished"
