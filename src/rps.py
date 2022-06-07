import random

rps_choice = ("rock", "paper", "scissors")
coin_choice = ("Heads", "Tails")

def rps_rand() -> str:
    return rps_choice[random.randint(0,2)]

def coin_flip() -> str:
    return coin_choice[random.randint(0,1)]