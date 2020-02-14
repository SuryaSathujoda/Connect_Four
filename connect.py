import numpy as np
import itertools

class Board():
    def __init__(self, rows, cols):
        self.dim = (rows, cols)
        self.board = np.zeros(self.dim)
        self.is_complete = False
        self.winner_id = -1

    def check_state(self):
        for i in range(self.dim[0]-3):
            for j in range(self.dim[1]-3):
                current_splice = self.board[i:i+4, j:j+4]

                diag_trace = np.einsum("ii->", current_splice)
                row_sum = np.einsum("ij->i", current_splice)
                if(self.check_winner(row_sum, diag_trace)):
                    return
        
                transpose_splice = np.einsum("ji", current_splice)
                diag_trace = np.einsum("ii->", transpose_splice)
                row_sum = np.einsum("ij->i", transpose_splice)
                if(self.check_winner(row_sum, diag_trace)):
                    return 

    def check_winner(self, row_sum, diag_trace):
        if(diag_trace in Player.win_conditions):
            self.is_complete = True
            self.winner_id = Player.win_conditions[diag_trace]
            print(self.board)
            return True

        for val in row_sum:
            if(val in Player.win_conditions):
                self.is_complete = True
                self.winner_id = Player.win_conditions[diag_trace]
                print(self.board)
                return True

    def update_state(self, col, player_token):
        if(np.count_nonzero(self.board == 0) == 0):
            self.is_complete = True
            print(self.board)
            return

        for i in range(self.dim[0]):
            if(self.board[self.dim[0]-i-1, col] == 0):
                self.board[self.dim[0]-i-1, col] = player_token
                return
        #print("error")

    def __str__(self):
        board_disp = ""
        for i in self.board:
            board_disp += str(i)+"\n"
        return board_disp

class Player():

    win_conditions = {}

    def __init__(self, player_name, player_id, token_value):
        self.player_name = player_name
        self.player_id = player_id
        self.token_value = token_value
        self.win_condition = token_value * 4
        Player.win_conditions[self.win_condition] = self.player_id

active_board = Board(8,8)
player_value = 1
col_counter = 1

player_list = {}
player_list[1] = Player("p1", 1, -1) 
player_list[2] = Player("p2", 2, -2) 
player_list[3] = Player("p3", 3, -3) 

print(Player.win_conditions)

while(active_board.is_complete == False):
    for i in range(1,4):
        active_board.update_state(col_counter%8, player_list[i].player_id)
        active_board.check_state()
        col_counter += 1
