import numpy as np

class Game():
    def __init__(self, board):
        self.board = board
        self.player_list = {}

    def add_player(self, player):
        player_token = player.player_id
        self.player_list[player_token] = player

    def play(self):
        player_turn = 0
        while(self.board.is_complete == False):
            current_player = self.player_list[player_turn % len(self.player_list)]
            token_val = current_player.token_value
            updated = self.board.update_state(self.get_input(), token_val)
            if(updated):
                self.board.check_state()
                player_turn += 1
            print(self.board)

    def get_input(self):
        column_no = int(input("Which Column do you want to enter token: "))
        return column_no


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
            print("The winner is: " + str(self.winner_id))
            return True

        for val in row_sum:
            if(val in Player.win_conditions):
                self.is_complete = True
                self.winner_id = Player.win_conditions[val]
                print("The winner is: " + str(self.winner_id))
                return True

    def update_state(self, col, player_token):
        if(np.count_nonzero(self.board == 0) == 0):
            self.is_complete = True
            print("Board Full")
            return True

        for i in range(self.dim[0]):
            if(self.board[self.dim[0]-i-1, col] == 0):
                self.board[self.dim[0]-i-1, col] = player_token
                return True
        print("Column Full")
        return False

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

live_game = Game(Board(8, 8))
new_player = Player("test", 0, -1)
live_game.add_player(Player("test", 0, -1))
live_game.add_player(Player("test1", 1, 1))
live_game.play()
