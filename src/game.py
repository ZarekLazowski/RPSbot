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
        self.rounds = 1
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
        
    def user_has_won(self) -> bool:
        '''
        A valid win will go until the user has accumulated 2 wins (BO3).

        Returns:
            `bool` Representing if the user has won this game
        '''
        return self.wins == 2

    def finish_game(self) -> str:
        '''
        Wrap up the RPS match, cleanup, save scores

        Returns:
            `str` Message indicating final game status
        '''
        results = ""

        # Determine win vs loss
        if self.user_has_won():
            results = " won this time"
            self.user.inc_wins()
        else:
            results = " is a loser"
            self.user.inc_loss()

        # Save statistics for future use
        self.user.save_file()
        
        # Return results as string for main channel
        return self.username + results

