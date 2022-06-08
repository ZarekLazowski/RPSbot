import random

rps_keyword = ("rock", "paper", "scissors", "quit")

rps_choice = ("rock", "paper", "scissors")
coin_choice = ("Heads", "Tails")

def rps_rand() -> str:
    return random.choice(rps_choice)

def rps_winner(bot: str, usr: str) -> str:
    # Convert string to indices
    usr = rps_choice.index(usr.lower())
    bot = rps_choice.index(bot.lower())

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