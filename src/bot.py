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
        # Play Rock, Paper, Scissors with a user in their DMs
        @self.command(name='rps')
        async def rps_cmd(context):
            # Start DM with user
            dm_channel = await context.author.create_dm()

            await dm_channel.send('Best of three! Rock, Paper, Scissors, Shoot!')

            # Stat bookkeeping
            wins = 0
            loss = 0
            game = 1

            # Keep playing until user or bot wins twice
            while wins < 2 and loss < 2:
                if wins == loss and game == 1:
                    await dm_channel.send('Game 1')
                else:
                    await dm_channel.send(str(wins) + ' to ' + str(loss) + '! Game ' + str(game))

                def check(msg):
                    return any(opt in msg.content.lower() for opt in rps.rps_keyword) \
                        and msg.channel == dm_channel \
                        and msg.author != self.user

                # Wait for user to send message
                with dm_channel.typing():
                    try:
                        # Grab message when received, timeout after 30 sec
                        msg = await self.wait_for('message', check=check, timeout=30)

                    # On timeout, mark loss and exit loop
                    except(asyncio.TimeoutError):
                        await dm_channel.send('You took too long. This counts as forfeit')
                        loss = 2
                        break

                    if msg.content.lower() == 'quit':
                        await dm_channel.send('Coward')
                        break

                    # Get RPS response
                    resp = rps.rps_rand()

                    # Send its choice
                    await dm_channel.send(resp)

                # Check winner
                res = rps.rps_winner(resp, msg.content.lower())

                # Do thing based on winner
                if res == 'bot':
                    loss += 1
                elif res == 'usr':
                    wins += 1
                    
                # Increment game counter
                game += 1

            # Post game wrapup. TODO: implement per user stat tracking
            if loss == 2:
                await dm_channel.send('ggs, better luck next time')
            elif wins == 2:
                await dm_channel.send('ggs, I\'ll train harder')
        
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