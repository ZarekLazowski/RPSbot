# RPS bot, plays rock paper scissors against a user

import os
from discord.ext import commands
from dotenv import load_dotenv

# Load bot token from environment
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class RPSbot(commands.Bot):
    def __init__(self, command_prefix='/', self_bot=False):
        commands.Bot.__init__(self, command_prefix=command_prefix, self_bot=self_bot)
        self.command_setup()

    async def on_ready(self):
        print(f'{self.user} has connected to Discord')

    def command_setup(self):
        @self.command(name='rps')
        async def rps(context):
            # Start DM with user
            dm_channel = await context.author.create_dm()

            # DM test message
            content = 'Test message'
            await dm_channel.send(content)

bot = RPSbot()

bot.run(TOKEN)