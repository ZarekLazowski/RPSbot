A bot that plays RPS against you

---

# Setup

This bot uses `dotenv` library to load information about how this tool is being
run. In order to use this bot, you must:
 * Have your own discord bot account you manage
 * Have a file `.env` in the source folder with the following items
     * `DISCORD_TOKEN`: Token associated with your bot
     * `OWNER_ID`: Your discord user ID

# Commands
| Command | Implemented | Function |
|---------|-------------|----------|
| /rps    | Partially   | Play RPS with the bot |
| /stats  | Partially   | Display W/L ratio with user (can specify user) |
| /flip   | Yes         | Flip a coin, respond with "Heads" or "Tails" |

# TODO
- [x] Create Bot
- [ ] Implementation of /rps
- [x]    33/33/33 chance to choose rock paper or scissors
- [x]    Keep track of W/L for each user
- [ ]    Learning AI that attempts to predict move
- [ ] Implementation of /stats
- [x] Implementation of /flip
