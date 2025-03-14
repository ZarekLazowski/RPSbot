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

    async def on_ready(self):
        print(f'{self.user} has connected to Discord')

    async def do_rps_game(self, dm_channel: discord.DMChannel, game: game_session):
        '''
        Run RPS logic
        '''
        # Display introduction text
        await dm_channel.send(rps.rps_intro)

        # Keep playing until user or bot wins twice
        while game.continue_game():
            await dm_channel.send(game.round_start())

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

            # Check winner and record stats
            game.update_stats(rps.rps_winner(resp, msg.content))
        
        # Say goodbye to the player
        if game.user_has_won():
            await dm_channel.send('ggs, I\'ll train harder')
        else:
            # On timeout or quit
            await dm_channel.send('ggs, better luck next time')

if __name__ == '__main__':
    # Load bot token from environment
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    OWNER_ID = os.getenv('OWNER_ID')

    # Create bot object
    bot = RPSbot()

    ############################################################################
    # Bot Commands
    ############################################################################
    @bot.hybrid_command(name='sync', description='Owner only. Syncs commands with discord')
    async def sync(context: commands.context):
        if str(context.author.id) == OWNER_ID:
            commands = await bot.tree.sync()
            print(f"Commands synced:\n{commands}")

            await context.send("Commands synced.")
        else:
            await context.send("Owner only command.")

    @bot.hybrid_command(name='rps', description='Play RPS in DMs with me')
    async def rps_cmd(context: commands.context):
        # Start DM with user
        dm_channel = await context.author.create_dm()
        
        # Grab user stats and create a new session
        game = game_session(context.author.display_name)

        # Do the game in DMs
        await bot.do_rps_game(dm_channel, game)

        # Report status of game to channel
        await context.channel.send(game.finish_game())

    @bot.hybrid_command(name='stats', description='Display RPS stats')
    async def stat_cmd(context: commands.context):
        user = user_stats(context.author.display_name)

        await context.send(user.dump_stats())

    # Flip a coin for the user
    @bot.hybrid_command(name='flip', description='Flip a coin')
    async def flip_cmd(context):
        # Determine side and send back to user
        await context.send(rps.coin_flip())

    # Run bot
    bot.run(TOKEN)
