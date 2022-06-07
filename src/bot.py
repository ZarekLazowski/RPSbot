# RPS bot, plays rock paper scissors against a user

import os, rps, asyncio
from discord.ext import commands
from dotenv import load_dotenv

class RPSbot(commands.Bot):
    def __init__(self, command_prefix='/', self_bot=False):
        commands.Bot.__init__(self, command_prefix=command_prefix, self_bot=self_bot)
        self.command_setup()

    async def on_ready(self):
        print(f'{self.user} has connected to Discord')

    def command_setup(self):
        @self.command(name='rps')
        async def rps_cmd(context):
            # Start DM with user
            dm_channel = await context.author.create_dm()

            await dm_channel.send('Rock, Paper, Scissors, Shoot!')

            try:
                def check(msg):
                    return any(opt in msg.content.lower() for opt in rps.rps_choice) and msg.channel == dm_channel

                # Wait for user to send message
                with dm_channel.typing():
                    # Grab message when received, timeout after 30 sec
                    msg = await self.wait_for('message', check=check, timeout=30)

                    # Send its choice
                    await dm_channel.send(rps.rps_rand())

                    # TODO: check to see if it won or not
            
            except(asyncio.TimeoutError):
                await dm_channel.send('You took too long')
                print('Timeout occured')


if __name__ == '__main__':
    # Load bot token from environment
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    # Create bot object
    bot = RPSbot()

    # Run bot
    bot.run(TOKEN)