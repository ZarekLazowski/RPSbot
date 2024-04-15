# RPS bot, plays rock paper scissors against a user

import os, rps, asyncio, discord
from discord.ext import commands
from dotenv import load_dotenv
from user import user_stats
from game import game_session

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

    '''
    Run RPS logic
    '''
    async def do_rps_game(self, dm_channel: discord.DMChannel, game: game_session):
        # Display introduction text
        output = rps.rps_intro

        # Keep playing until user or bot wins twice
        while game.continue_game():
            output += game.round_start()

            await dm_channel.send(output)

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
            game.update_stats(res)

            # Clear pretext
            output = ''
        
        # Report who won and who lost
        if game.wins == 2:
            await dm_channel.send('ggs, I\'ll train harder')
        else:
            await dm_channel.send('ggs, better luck next time')

    def command_setup(self):
        # Play Rock, Paper, Scissors with a user in their DMs
        @self.command(name='rps')
        async def rps_cmd(context: commands.context):
            # Start DM with user
            dm_channel = await context.author.create_dm()
            
            # Grab user stats and create a new session
            game = game_session(context.author.display_name)

            # Do the game in DMs
            await self.do_rps_game(dm_channel, game)

            report = game.finish_game()
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