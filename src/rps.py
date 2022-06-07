import random

rps_choice = ("rock", "paper", "scissors")

def rps_rand() -> str:
    return rps_choice[random.randrange(0, 2)]
