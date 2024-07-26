import coc
import traceback
import creds
from database.database import BotDatabase
import discord
from discord.ext import commands
import nest_asyncio
nest_asyncio.apply()
description = ""

# Il prefisso del bot in minuscolo
prefix = creds.prefix

# Crea la connessione con le API di COC usando la libreria coc.py

# Tutte le estensioni, i comandi del bot
initial_extensions = (
    "command.WarManager",
    "command.UpgradeManager",
)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True


class MyBot(commands.Bot):

    def __init__(self):
        super().__init__(command_prefix=prefix+' ',
                         description=description,
                         case_insensitive=True,
                         intents=intents
                         )
        coc_client = coc.login(creds.coc_dev_email, creds.coc_dev_password, client=coc.EventsClient,
                               key_names=creds.coc_key_names)

        self.coc = coc_client

        # Instanzia il database
        self.dbconn = BotDatabase()

    async def on_ready(self):
        print(f"Bot is logged in as {self.user} ID: {self.user.id}")

    async def on_command_error(self, context, exception):
        await context.send(exception)

    async def custom_load_extensions(self):
        # Carica tutte le estensioni, i file nella cartella comandi
        for extension in initial_extensions:
            try:
                await self.load_extension(extension)
            except Exception as extension:
                traceback.print_exc()

    async def setup_hook(self):
        await self.custom_load_extensions()

if __name__ == "__main__":
    try:
        bot = MyBot()
        bot.run(creds.discord_bot_token)
    except:
        traceback.print_exc()
