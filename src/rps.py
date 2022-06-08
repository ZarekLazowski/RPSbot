import random

rps_intro = 'Best of three!\nRespond with "rock", "paper", "scissors" to play\nYou can also respond with \U0001FAA8, \U0001F4C4, or \U00002702\n\nReady? Rock, Paper, Scissors, Shoot!\n'

rps_keyword = ("rock", "paper", "scissors", "quit", "\U0001FAA8", "\U0001F4C4", "\U00002702")

rps_choice = ("rock", "paper", "scissors")
rps_echoice = ("\U0001FAA8", "\U0001F4C4", "\U00002702")
coin_choice = ("Heads", "Tails")

def rps_rand() -> str:
    return random.choice(rps_choice)

def rps_erand() -> str:
    return random.choice(rps_echoice)

def rps_winner(bot: str, usr: str) -> str:
    # Convert string to indices
    # Word response
    if bot.isalpha():
        usr = rps_choice.index(usr.lower())
        bot = rps_choice.index(bot.lower())
    # Emote response
    else:
        usr = rps_echoice.index(usr[0])
        bot = rps_echoice.index(bot[0])

    # Determine winner
    # Tie
    if usr == bot:
        return 'tie'

    # User wins
    elif bot == ((usr + 2) % 3):
        return 'usr'

    # Bot wins
    else:
        return 'bot'

def coin_flip() -> str:
    return random.choice(coin_choice)