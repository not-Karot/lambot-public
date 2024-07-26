from configparser import ConfigParser

config = ConfigParser()
config.read('./config.ini')

# CLASH OF CLANS API
# Your Clash of Clash Developer Account email & password will be used to auto-generate a Key,
# so don't worry about creating a new Key
coc_dev_email = ""  # Clash of Clans Developer Account email
coc_dev_password = ""  # Clash of Clans Developer Account password
coc_key_names = config.get(config.get('CONFIGURATION', 'current_version'), 'coc_key_names')

#DISCORD DEVELOPER
discord_bot_token = config.get(config.get('CONFIGURATION', 'current_version'), 'discord_bot_token') # 59 character Bot Token from your Discord App
prefix = config.get(config.get('CONFIGURATION', 'current_version'), 'bot_prefix')

#DATABASE
db_user= ""
db_password=""
db_host=""
db_name= ""
