# RPS bot, plays rock paper scissors against a user

import os, rps, asyncio, discord
from discord.ext import commands
from dotenv import load_dotenv

class RPSbot(commands.Bot):
    def __init__(self, command_prefix='/', self_bot=False):
        intents = discord.Intents.default()
        intents.message_content = True
        commands.Bot.__init__(self, command_prefix=command_prefix, self_bot=self_bot, intents=intents)
        self.command_setup()

    def __del__(self):
        # Call default delete command
        commands.Bot.__del__(self)

    async def on_ready(self):
        print(f'{self.user} has connected to Discord')

    async def do_rps_game(self, dm_channel) -> str:
        # Stat bookkeeping
        wins = 0
        loss = 0
        game = 1

        # Display introduction text
        pretext = rps.rps_intro

        # Keep playing until user or bot wins twice
        while wins < 2 and loss < 2:
            if wins == loss and game == 1:
                pretext += 'Game 1'
            else:
                pretext += str(wins) + ' to ' + str(loss) + '! Game ' + str(game)

            await dm_channel.send(pretext)

            # Check if a received command is valid
            def check(msg):
                if msg.content.isalpha():
                    return (msg.content.lower() in rps.rps_keyword) \
                        and msg.channel == dm_channel \
                        and msg.author != self.user
                else:
                    return (msg.content[0] in rps.rps_keyword) \
                    and msg.channel == dm_channel \
                    and msg.author != self.user

            # Display 'typing' while waiting for user input
            async with dm_channel.typing():
                try:
                    # Grab message when received, timeout after 30 sec
                    msg = await self.wait_for('message', check=check, timeout=30)

                # On timeout, mark loss and exit loop
                except(asyncio.TimeoutError):
                    await dm_channel.send('You took too long. This counts as forfeit')
                    loss = 2
                    break

                # User quits early
                if msg.content.lower() == 'quit':
                    await dm_channel.send('Coward')
                    break

                # Respond with same style (emote vs word)
                if msg.content.isalpha():
                    resp = rps.rps_rand()
                else:
                    resp = rps.rps_erand()
                
                # Send its choice
                await dm_channel.send(resp)

            # Check winner
            res = rps.rps_winner(resp, msg.content)

            # Do thing based on winner
            if res == 'bot':
                loss += 1
            elif res == 'usr':
                wins += 1
                
            # Increment game counter
            game += 1

            # Clear pretext
            pretext = ''
        
        # Report who won and who lost
        if wins == 2:
            await dm_channel.send('ggs, I\'ll train harder')
            return 'win'
        else:
            await dm_channel.send('ggs, better luck next time')
            return 'lose'

    def command_setup(self):
        # Play Rock, Paper, Scissors with a user in their DMs
        @self.command(name='rps')
        async def rps_cmd(context):
            # Start DM with user
            dm_channel = await context.author.create_dm()

            # Do the game in DMs
            res = await self.do_rps_game(dm_channel) 

            # Report back to the guild who won/lost. TODO: Add logic to keep track of user stats
            if res == 'lose':
                report = context.author.display_name + ' is a loser'
            else:
                report = context.author.display_name + ' won this time'

            await context.channel.send(report)
        
        # Flip a coin for the user
        @self.command(name='flip')
        async def flip_cmd(context):
            # Determine side and send back to user
            await context.send(rps.coin_flip())


if __name__ == '__main__':
    # Load bot token from environment
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    # Create bot object
    bot = RPSbot()

    # Run bot
    bot.run(TOKEN)