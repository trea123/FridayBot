
# Discord Bot

Discord Bot is used to learn a combination of Python and the discord.py package.

---

## OS & Python Version Info

```bash
lsb_release -a
# Distributor ID: Kali
# Description:    Kali GNU/Linux Rolling
# Release:        2022.2
# Codename:       kali-rolling
```

*Tested using Python 3.10.4*

---

## Installation

*Development*

You need to set the bot token to an environment variable called **BOT_TOKEN** and then run the following commands to setup and start the bot:

```bash
export BOT_TOKEN="<YOUR_TOKEN_GOES_HERE>"  # or set BOT_TOKEN="<YOUR_TOKEN_GOES_HERE>" on windows
python3 -m venv venv
source venv/bin/activate # or .\venv\Scripts\activate.bat on windows
pip install --upgrade pip
pip install -r requirements.txt
python bot.py
```

---

*Production*

You need to run an installation script and pass the bot token to the installation script when prompted using the following commands to setup and start the bot:

```bash
sudo bash install.sh
```

Then, in production you can start and stop the bot using the following commands (after running the installation script):

```bash
systemctl start discordbot # starting bot systemd service
systemctl stop discordbot  # stopping bot systemd service
```

**Note**, for production the bot is designed to work on Linux systems only...

---

## Uninstall

To uninstall the bot from a *production* system, you can execute the following command:

```bash
sudo bash uninstall.sh
```
