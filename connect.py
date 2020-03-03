import numpy as np
from matplotlib import pyplot as plt

class Game():
    def __init__(self, board):
        self.board = board
        self.player_list = {}
        self.player_tokens = {}

    def add_player(self, player):
        self.player_list[player.player_id] = player
        self.player_tokens[player.token_value] = player.player_id

    def play(self):
        player_turn = 0
        while(self.board.is_complete == False):
            current_player = self.player_list[player_turn % len(self.player_list)]
            print("%s's Turn" %current_player.player_name)
            token_val = current_player.token_value
            updated = self.board.update_state(current_player.get_move(self.board), token_val)
            while(not updated):
                updated = self.board.update_state(current_player.get_move(self.board), token_val)
            self.board.check_state()
            player_turn += 1
            print(self.board)
            print()

        if(self.board.winner_id == -1):
            print("The Game is a Draw!")
            self.plot_board(False)
        else:
            print("The winner is: %s" %self.player_list[self.board.winner_id].player_name)
            self.plot_board(True)

    def plot_board(self, winner_exists):
        colours = np.linspace(0, 0.8, len(self.player_list))
        for i in range(self.board.dim[0]):
            for j in range(self.board.dim[1]):
                if(not self.board.board[i][j] == 0):
                    current_player_id = self.player_tokens[self.board.board[i][j]]
                    plt.scatter(j+1, self.board.dim[0]-i, color=str(colours[current_player_id]))

        if(winner_exists):
            win_line = self.board.winning_indices
            winning_line_xs = [win_line[0][1]+1, win_line[1][1]+1]
            winning_line_ys = [self.board.dim[0]-win_line[0][0], self.board.dim[0]-win_line[1][0]]
            plt.plot(winning_line_xs, winning_line_ys)

        plt.xlim(0, self.board.dim[1]+1)
        plt.ylim(0, self.board.dim[0]+1)
        plt.show()


class Board():
    def __init__(self, rows, cols):
        self.dim = (rows, cols)
        self.board = np.zeros(self.dim)
        self.winning_indices = 0
        self.is_complete = False
        self.winner_id = -1

    def check_state(self):
        for i in range(self.dim[0]-3):
            for j in range(self.dim[1]-3):
                current_splice = self.board[i:i+4, j:j+4]

                if(self.check_winner(current_splice)):
                    self.set_winning_indices(current_splice, i, j, False)
                    return
        
                rotated_splice = np.rot90(current_splice)
                if(self.check_winner(rotated_splice)):
                    self.set_winning_indices(rotated_splice, i, j, True)
                    return 

    def check_winner(self, current_splice):
        diag_trace = np.einsum("ii->", current_splice)
        row_sum = np.einsum("ij->i", current_splice)

        if(diag_trace in Player.win_conditions):
            self.is_complete = True
            self.winner_id = Player.win_conditions[diag_trace]
            return True

        for val in row_sum:
            if(val in Player.win_conditions):
                self.is_complete = True
                self.winner_id = Player.win_conditions[val]
                return True

    def set_winning_indices(self, current_splice, row, col, rotated):
        diag_trace = np.einsum("ii->", current_splice)
        if(diag_trace in Player.win_conditions):
            if(not rotated):
                self.winning_indices = [(row, col), (row+3, col+3)]
            else:
                self.winning_indices = [(row, col+3), (row+3, col)]
            return 

        row_sum = np.einsum("ij->i", current_splice)
        for i in range(4):
            if(row_sum[i] in Player.win_conditions):
                if(not rotated):
                    self.winning_indices = [(row+i, col), (row+i, col+3)]
                else:
                    self.winning_indices = [(row, col+3-i), (row+3, col+3-i)]
                return 


    def update_state(self, col, player_token):
        if(np.count_nonzero(self.board == 0) == 0):
            self.is_complete = True
            print("Board Full")
            return True

        if(self.board[0][col] != 0):
            print("Column Full! Pick another Column!")
            return False

        for i in range(self.dim[0]):
            if(self.board[self.dim[0]-i-1, col] == 0):
                self.board[self.dim[0]-i-1, col] = player_token
                return True

    def __str__(self):
        repr_arr = np.copy(self.board)
        for i in range(self.dim[0]):
            for j in range(self.dim[1]):
                if(not repr_arr[i][j] == 0):
                    repr_arr[i][j] = np.log10(repr_arr[i][j])
        return np.array2string(repr_arr)

class Player():

    win_conditions = {}

    def __init__(self, player_name, player_id, token_value):
        self.player_name = player_name
        self.player_id = player_id
        self.token_value = 10**token_value
        self.win_condition = 10**token_value * 4
        Player.win_conditions[self.win_condition] = self.player_id

    def get_move(self, board):
        column_no = input("Which Column do you want to enter token: ")
        while(not column_no.isdigit() or not int(column_no) in range(board.dim[1])):
            column_no = input("Select a digit between 0 - %d: " %(board.dim[1]-1))
        return int(column_no)

class AI(Player):
    def __init__(self, player_name, player_id, token_value):
        super().__init__(player_name, player_id, token_value)

    def get_move(self, board):
        return np.random.randint(board.dim[1])

def start_game():
    print("Welcome to Connect 4!")
    board_size = str(input("Enter Board size (n,m): ")).split(",")
    live_game = Game(Board(int(board_size[0]), int(board_size[1])))

    no_of_players = int(input("Enter Number of Players: "))
    for i in range(no_of_players):
        player_name = input("Enter Player Name: ")
        live_game.add_player(Player(player_name, i, i+1))

    no_of_ais = int(input("Enter Number of AIs: "))
    for i in range(no_of_ais):
        ai_name = "Computer "+str(i)
        live_game.add_player(AI(ai_name, no_of_players+i, -i-1))

    print("\nGame Start!\n")

    live_game.play()

start_game()
