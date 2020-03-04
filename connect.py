import numpy as np
from matplotlib import pyplot as plt

class Game():
    """
    This is a class for the main game run logic.

    Attributes:
        board (Board): The Board object which is associated to the Game.
        player_list (dict): Hash holding list of Player objects associated with player_ids.
        player_tokens (dict): Hash holding player_ids associated with player tokens.
    """

    def __init__(self, board):
        """
        Constructor for Game class.

        Parameters:
            board (Board): The Board objected associated with the Game instance.
        """

        self.board = board
        self.player_list = {}
        self.player_tokens = {}

    def add_player(self, player):
        """
        The function to add a player by id and token by player_id to the Game instance.

        Parameters:
            player (Player)
        """

        self.player_list[player.player_id] = player
        self.player_tokens[player.token_value] = player.player_id

    def play(self):
        """
        The function to execute the main game logic of the game.
        """

        player_turn = 0
        while(self.board.is_complete == False):
            # Gets the current player whose turn it is and the respective token value
            current_player = self.player_list[player_turn % len(self.player_list)]
            print("%s's Turn" %current_player.player_name)
            token_val = current_player.token_value

            # Updates the state of the board which a prompt to the user handling exceptions
            updated = self.board.update_state(current_player.get_move(self.board), token_val)
            while(not updated):
                updated = self.board.update_state(current_player.get_move(self.board), token_val)

            # Checks the state of the board and goes to next player
            self.board.check_state()
            player_turn += 1
            print(self.board)
            print()

        # Plots the Board once the game is over.
        if(self.board.winner_id == -1):
            print("The Game is a Draw!")
            self.plot_board(False)
        else:
            print("The winner is: %s" %self.player_list[self.board.winner_id].player_name)
            self.plot_board(True)

    def plot_board(self, winner_exists):
        """
        Plots the board when the game is over.

        Parameters:
            winner_exists (Boolean): Whether there is a winner.
        """

        # Generating a greyscale colour for each of the n players
        colours = np.linspace(0, 0.8, len(self.player_list))

        # Plotting the player tokens on the graph
        for i in range(self.board.dim[0]):
            for j in range(self.board.dim[1]):
                if(not self.board.board[i][j] == 0):
                    current_player_id = self.player_tokens[self.board.board[i][j]]
                    plt.scatter(j+1, self.board.dim[0]-i, color=str(colours[current_player_id]))

        # If winner_exists then the winning line is plotted
        if(winner_exists):
            win_line = self.board.winning_indices
            winning_line_xs = [win_line[0][1]+1, win_line[1][1]+1]
            winning_line_ys = [self.board.dim[0]-win_line[0][0], self.board.dim[0]-win_line[1][0]]
            plt.plot(winning_line_xs, winning_line_ys)

        # Plotting requirements
        plt.xlim(0, self.board.dim[1]+1)
        plt.ylim(0, self.board.dim[0]+1)
        plt.show()


class Board():
    """
    This is a class for the Board and associated with Board logic.

    Attributes:
        dim (tuple): The board dimensions.
        board (ndarray): The board with given dimensions.
        winning_indices (list): Starting and ending of winning line.
        is_complete (Boolean): Flag is game is over.
        winner_id (int): The id of the winning player.
    """

    def __init__(self, rows, cols):
        """
        Constructor for Board class.

        Parameters:
            rows (int): Number of rows in board.
            cols (int): Number of columnss in board.
        """

        self.dim = (rows, cols)
        self.board = np.zeros(self.dim)
        self.winning_indices = []
        self.is_complete = False
        self.winner_id = -1

    def check_state(self):
        """
        The function to check if there is a winner and set the winning line co-ordinates.
        """

        # Split the board in all possible 4x4 subgrids
        for i in range(self.dim[0]-3):
            for j in range(self.dim[1]-3):
                current_splice = self.board[i:i+4, j:j+4]

                # Check if the subgrid contains a winning condition and set winning indices
                if(self.check_winner(current_splice)):
                    self.set_winning_indices(current_splice, i, j, False)
                    return
        
                # Do the same for a rotated subgrid to reuse code for checking diagonal and rows
                # but now for reverse diagonal and columns
                rotated_splice = np.rot90(current_splice)
                if(self.check_winner(rotated_splice)):
                    self.set_winning_indices(rotated_splice, i, j, True)
                    return 

    def check_winner(self, current_splice):
        """
        The function to check if the 4x4 subgrid contains a winner in row or diagonal.

        Return:
            Boolean: Only True if a winner is found (game over).
        """

        # Using Einstein Summation method for more efficient trace and row sum calculation
        diag_trace = np.einsum("ii->", current_splice)
        row_sum = np.einsum("ij->i", current_splice)

        # Check if trace is equal to one of the player win conditions
        if(diag_trace in Player.win_conditions):
            self.is_complete = True
            self.winner_id = Player.win_conditions[diag_trace]
            return True

        # Check if row sum contains any of the player win conditions
        for val in row_sum:
            if(val in Player.win_conditions):
                self.is_complete = True
                self.winner_id = Player.win_conditions[val]
                return True

    def set_winning_indices(self, current_splice, row, col, rotated):
        """
        This function sets the starting and ending indices for the winning line.

        Parameters:
            current_splice (ndarray): The 4x4 subgrid containing the winning line.
            row (int): Row of the first element in the subgrid.
            col (int): Column of the first element in the subgrid.
            rotated (Boolean): Whether the given subgrid is rotated for vertical/reverse diagonal checking.
        """

        # If the winning line is a diagonal, it sets the appropriate indices for the winning line
        diag_trace = np.einsum("ii->", current_splice)
        if(diag_trace in Player.win_conditions):
            if(not rotated):
                self.winning_indices = [(row, col), (row+3, col+3)]
            else:
                self.winning_indices = [(row, col+3), (row+3, col)]
            return 

        # If the winning line is row (column for rotated), it sets the appropriate indices for the winning line
        row_sum = np.einsum("ij->i", current_splice)
        for i in range(4):
            if(row_sum[i] in Player.win_conditions):
                if(not rotated):
                    self.winning_indices = [(row+i, col), (row+i, col+3)]
                else:
                    self.winning_indices = [(row, col+3-i), (row+3, col+3-i)]
                return 


    def update_state(self, col, player_token):
        """
        This function adds a token to the board if possible by handling errors.

        Parameters:
            col (int): Column to insert the token.
            player_token (float): The player token value.

        Return:
            Boolean: True if token was successfully added or board is full. False otherwise.
        """

        # Checks if board is full
        if(np.count_nonzero(self.board == 0) == 0):
            self.is_complete = True
            print("Board Full")
            return True

        # Checks if column is full and prints error if human choice
        if(self.board[0][col] != 0):
            if(player_token > 1):
                print("Column Full! Pick another Column!")
            return False

        # Adds token to lowest available row in column
        for i in range(self.dim[0]):
            if(self.board[self.dim[0]-i-1, col] == 0):
                self.board[self.dim[0]-i-1, col] = player_token
                return True

    def __str__(self):
        """
        __str__ function for the Board class.

        Internally tokens are actually represented as 10^(visible_token) to avoid summing errors.
        Hence, this function converts the internal token_values to those more human readable.

        Returns:
            String: String representation of the board.
        """

        repr_arr = np.copy(self.board)

        # Converts board to human readable log10 values because internally token values 
        # are stored as 10^(player_id) and AI ids are negative.
        for i in range(self.dim[0]):
            for j in range(self.dim[1]):
                if(not repr_arr[i][j] == 0):
                    repr_arr[i][j] = np.log10(repr_arr[i][j])
        return np.array2string(repr_arr)

class Player():
    """
    This is a class for the Player object.

    Attributes:
        player_name (str): Name of the Player.
        player_id (int): Internal unique player id.
        token_value (float): Internal token value.
        win_condition (float): Sum for which the player wins a 4x4 subgrid.

    Class Attributes:
        win_conditions (dict): Hash all player_ids indexed by win conditions.
    """

    win_conditions = {}

    def __init__(self, player_name, player_id, token_value):
        """
        Constructor for Player class.

        Parameters:
            player_name (str): Name of the Player.
            player_id (int): Player id given.
            token_value (int): Human readable token value.
        """

        self.player_name = player_name
        self.player_id = player_id
        self.token_value = 10**token_value
        self.win_condition = 10**token_value * 4
        Player.win_conditions[self.win_condition] = self.player_id

    def get_move(self, board):
        """
        This functions queries the player for an input column and handles errors.

        Parameters:
            board (ndarray): The current board the player is playing on.
        """

        # Gets a valid input from the player
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
    """
    This function sets up the Game, Board and Players.
    """

    # Getting board dimensions and initialises the Game object.
    print("Welcome to Connect 4!")
    board_size = str(input("Enter Board size (n,m): ")).split(",")
    live_game = Game(Board(int(board_size[0]), int(board_size[1])))

    # Get number of human players and adds them to the Game object
    no_of_players = int(input("Enter Number of Players: "))
    for i in range(no_of_players):
        player_name = input("Enter Player Name: ")
        live_game.add_player(Player(player_name, i, i+1))

    # Gets number of AI players and adds them to the Board object with negative tokense
    no_of_ais = int(input("Enter Number of AIs: "))
    for i in range(no_of_ais):
        ai_name = "Computer "+str(i)
        live_game.add_player(AI(ai_name, no_of_players+i, -i-1))

    print("\nGame Start!\n")

    # Starts the Game logic
    live_game.play()

start_game()
