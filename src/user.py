import os, rps, asyncio

class user_stats():
    username:    str
    tot_matches: int
    num_win:     int
    num_loss:    int

    def __init__(self, username:str):
        self.username = username

        self.load_info()
    
    def get_filename(self):
        return self.username + ".stats"

    '''
    Save game stat info into a human-readable format
    '''
    def save_info(self):
        # Open stats file, create if it doesn't exist
        with open(self.get_filename(), "w+") as stat_file:
            stat_file.write(f"{self.tot_matches}\n{self.num_win}\n{self.num_loss}")


    '''
    Load game stat info from stat file
    '''
    def load_info(self):
        with open(self.get_filename(), "r") as stat_file:
            # If this is a new user init the stats to 0
            if not stat_file:
                self.tot_matches = 0
                self.num_win = 0
                self.num_loss = 0
                return
            
            # Otherwise parse the file for their information
            lines = stat_file.readlines()

            self.tot_matches = int(lines[0])
            self.num_win = int(lines[1])
            self.num_loss = int(lines[2])

    def inc_wins(self):
        self.num_win += 1
        self.tot_matches += 1
    
    def inc_loss(self):
        self.num_loss += 1
        self.tot_matches += 1
