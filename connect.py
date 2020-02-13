import numpy as np
import itertools

class Board():
    def __init__(self, rows, cols):
        self.dim = (rows, cols)
        self.board = np.zeros(self.dim)
        self.is_complete = False
        self.winner_id = -1
        #self.test_board()

    def check_state(self):
        for i in range(self.dim[0]-3):
            for j in range(self.dim[1]-3):
                current_splice = self.board[i:i+4, j:j+4]

                diag_trace = np.einsum("ii->", current_splice)
                row_sum = np.einsum("ij->i", current_splice)
                is_winner, player_id = self.check_winner(row_sum, diag_trace)
                if(is_winner):
                    self.is_complete = True
                    self.winner = player_id
                    print("GAME OVER")
                    print(self.board)
                    return
        
                transpose_splice = np.einsum("ji", current_splice)
                diag_trace = np.einsum("ii->", transpose_splice)
                row_sum = np.einsum("ij->i", transpose_splice)
                is_winner, player_id = self.check_winner(row_sum, diag_trace)
                if(is_winner):
                    self.is_complete = True
                    self.winner = player_id

    def check_winner(self, row_sum, diag_trace):
        if(diag_trace == 4 or 4 in row_sum):
            self.is_complete = True
            return True, 1
        return False, -1

    def update_state(self, col, player_val):
        player_token = player_val
        token_added = False
        for i in range(self.dim[0]):
            if(self.board[self.dim[0]-i-1, col] == 0):
                self.board[self.dim[0]-i-1, col] = player_token
                token_added = True
                return
        print("error")

    def test_board(self):
        for i,j in itertools.product(range(4), range(4)):
            self.board[i,j] = 1
        print(str(self.board))

    def __str__(self):
        board_disp = ""
        for i in self.board:
            board_disp += str(i)+"\n"
        return board_disp

active_board = Board(8,8)
player_value = 1
col_counter = 1
while(active_board.is_complete == False):
    active_board.update_state(col_counter%7, player_value)
    player_value = player_value * -1
    active_board.check_state()
    col_counter += 1
