import os, rps, asyncio
from user import user_stats

class game_session():
    username: str
    user:     user_stats
    rounds:   int
    wins:     int
    loss:     int

    def __init__(self, username: str):
        self.username = username
        self.user = user_stats(username)
        self.rounds = 0
        self.wins = 0
        self.loss = 0

    def update_stats(self, winner: str):
        self.rounds += 1
        
        if winner == "usr":
            self.wins += 1
        elif winner == "bot":
            self.loss += 1

    def continue_game(self) -> bool:
        if self.wins < 2 and self.loss < 2:
            return True
        else:
            return False

    def round_start(self):
        if self.rounds == 1:
            return "Game 1"
        else:
            return str(self.wins) + " to " + str(self.loss) + "! Game " + str(self.rounds)

    '''
    Wrap up the RPS match, cleanup, save scores
    '''
    def finish_game(self) -> str:
        results = ""

        # Determine win vs loss
        if self.wins > self.loss:
            results = " won this time"
            self.user.inc_wins()
        else:
            results = " is a loser"
            self.user.inc_loss()

        # Save statistics for future use
        self.user.save_info()
        
        # Return results as string for main channel
        return self.username + results

