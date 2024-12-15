import random

rps_intro = 'Best of three!\n' + \
            'Respond with "rock", "paper", "scissors" to play or "quit" to forfeit\n' + \
            'You can also respond with :rock:, :page_facing_up:, or :scissors:\n\nReady? Rock, Paper, Scissors, Shoot!\n'

rps_keyword = ("rock", "paper", "scissors", "quit", "\U0001FAA8", "\U0001F4C4", "\U00002702")

rps_choice = ("rock", "paper", "scissors")
rps_echoice = ("\U0001FAA8", "\U0001F4C4", "\U00002702")
coin_choice = ("Heads", "Tails")

def rps_rand() -> str:
    return random.choice(rps_choice)

def rps_erand() -> str:
    return random.choice(rps_echoice)

'''
rps_winner

returns: True on user win, False on bot win
'''
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