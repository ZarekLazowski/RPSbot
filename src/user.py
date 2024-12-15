import os
from pathlib import Path

class user_stats():
    username:    str
    tot_matches: int
    num_win:     int
    num_loss:    int

    stat_location:str = "stats"
    file_ext:str = ".stat"

    def __init__(self, username:str):
        self.username = username
        self.tot_matches = 0
        self.num_win = 0
        self.num_loss = 0

        path = self.get_filepath()

        if path.exists():
            self.load_file()
        else:
            self.save_file()
    
    def get_filepath(self):
        return Path(os.sep.join([self.stat_location, self.username + self.file_ext]))

    def save_file(self):
        '''
        Save game stat info into a human-readable format
        '''
        # Open stats file, create if it doesn't exist
        with open(self.get_filepath(), "w+") as stat_file:
            stat_file.write(f"{self.tot_matches}\n{self.num_win}\n{self.num_loss}")

    def load_file(self):
        '''
        Load game stat info from stat file
        '''
        with open(self.get_filepath(), "r") as stat_file:
            lines = stat_file.readlines()
            self.tot_matches = int(lines[0])
            self.num_win = int(lines[1])
            self.num_loss = int(lines[2])

    def inc_wins(self):
        '''
        Mark a won game (player's perspective)
        '''
        self.num_win += 1
        self.tot_matches += 1
    
    def inc_loss(self):
        '''
        Mark a lost game (player's perspective)
        '''
        self.num_loss += 1
        self.tot_matches += 1

    def dump_stats(self):
        '''
        Get a summary of the games against this user.

        Returns:
            `str` Summary of total number of games, number of wins, number of losses
        '''
        return f"{self.username} has played {self.tot_matches} games\n" + \
            f"They have won {self.num_win} games and lost {self.num_loss}"
