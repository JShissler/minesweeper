from random import randint
from copy import deepcopy
from string import ascii_uppercase

class Board:

    def __init__(self, width, height, difficulty):
        self.starting_board_state = []
        self.playing_board_state = []
        self.display_board_state = []
        self.total_mines = 0
        self.unmarked_mines = 0
        self.first_move = True
        self.height = height
        self.width = width

        self.check_givens(max_width, max_height, min_width, min_height)

        self.initialize_boards()
        self.generate_board(difficulty)
        self.convert_board_starting_to_playing()

    # Make sure given width and height fall within desired values
    def check_givens(self, max_width, max_height, min_width, min_height):
        if self.width > max_width:
            self.width = max_width
        if self.height > max_height:
            self.height = max_height
        if self.width < min_width:
            self.width = min_width
        if self.height < min_height:
            self.height = min_height

    # Populate starting board with all 1's and display board with all X's
    def initialize_boards(self):
        for height in range(self.height):
            starting_row = []
            display_row = []
            for width in range(self.width):
                starting_row.append(1)
                display_row.append('X')
            self.starting_board_state.append(starting_row)
            self.display_board_state.append(display_row)

    # Convert an amount of squares in the starting board to mines based on the chosen difficulty
    def generate_board(self, difficulty, add_one = False):
        easy = 0.12
        medium = 0.16
        expert = 0.20
        total_squares = self.width * self.height
        if add_one == False:
            pool_of_mines = 0
            if difficulty == 'Easy':
                pool_of_mines = total_squares * easy
            if difficulty == 'Medium':
                pool_of_mines = total_squares * medium
            if difficulty == 'Expert':
                pool_of_mines = total_squares * expert
            pool_of_mines = round(pool_of_mines)
            self.total_mines = pool_of_mines
            self.unmarked_mines = pool_of_mines
        else:
            pool_of_mines = 1
        while pool_of_mines > 0:
            while True:
                rand_height = randint(0, self.height - 1)
                rand_width = randint(0, self.width - 1)
                if self.starting_board_state[rand_height][rand_width] == 1:
                    self.starting_board_state[rand_height][rand_width] = 0
                    pool_of_mines += -1
                    break

    # Generates the playing board based on the mines in the starting board
    def convert_board_starting_to_playing(self):
        self.playing_board_state = []
        for height in range(self.height):
            playing_row = []
            for width in range(self.width):
                converted_square = ''
                count = 0
                # Check if square is a mine
                if self.starting_board_state[height][width] == 0:
                    converted_square = 'M'
                # Calculate surrounding mines if the square isn't a mines
                else:
                    for step in range(-1,2):
                        for square in range(-1,2):
                            try:
                                height_index = height + step
                                width_index = width + square
                                if height_index >= 0 and width_index >= 0:
                                    if self.starting_board_state[height_index][width_index] == 0:
                                        count += 1
                            except IndexError:
                                pass
                    converted_square = str(count)
                playing_row.append(converted_square)
            self.playing_board_state.append(playing_row)

    def draw_board(self, board):
        row_increment = 0
        # Draw game board rows
        for row in board:
            line = ""
            row_label = chr(ord('A') + row_increment)
            for square in row:
                line += (" " + str(square))
            if row_label == 'A':
                print(row_label + " |" + line + " | " + row_label + "      Total Mines: " + str(self.total_mines))
            elif row_label == 'B':
                print(row_label + " |" + line + " | " + row_label + "   Unmarked Mines: " + str(self.unmarked_mines))
            else:
                print(row_label + " |" + line + " | " + row_label)
            row_increment += 1
        # Draw bottom label rows
        line1 = "   -"
        line2 = "   "
        line3 = "                     "
        for column in range(1, self.width + 1):
            line1 += "--"
            line2 += " " + str(column)[0]
            if column >= 10:
                line3 += " " + str(column)[1]
        print(line1)
        print(line2)
        print(line3)

    def check_victory(self):
        temp_display_board = deepcopy(self.display_board_state)
        temp_display_board = [[x.replace('?','M') for x in l] for l in temp_display_board]
        temp_display_board = [[x.replace('X','M') for x in l] for l in temp_display_board]
        if temp_display_board == self.playing_board_state:
            return True
        else:
            return False

    def update_board(self, height, width, marking):
        # Handle marking or unmarking of a square
        if marking:
            if self.display_board_state[height][width] != '?':
                self.display_board_state[height][width] = '?'
                self.unmarked_mines += -1
            else:
                self.display_board_state[height][width] = 'X'
                self.unmarked_mines += 1

            victory = self.check_victory()
            if victory:
                return [False, True]
            # Return True for the game still being active and False for no victory
            else:
                return [True, False]
        
        # Prevent losing on first move; Moves the mine chosen and updates the playing board
        if self.first_move and self.starting_board_state[height][width] == 0:
            self.starting_board_state[height][width] = 2
            self.generate_board('', True)
            self.convert_board_starting_to_playing()
        self.first_move = False

        # Ends the game if a mine is chosen
        if self.starting_board_state[height][width] == 0:
            # Return False for the game no longer being active and False for no victory
            return [False, False]

        # Handle updating chosen square and updating surrounding squares if a 0 was chosen or revealed
        else:
            # Determine if the square should reveal other squares; if it is not a 0 then it will only display itself
            if self.playing_board_state[height][width] != '0':
                self.display_board_state[height][width] = self.playing_board_state[height][width]
            # Cycle through revealing 0's and surrounding numbers if a 0 is chosen
            else:
                self.display_board_state[height][width] = self.playing_board_state[height][width]
                while True:
                    temp_board = deepcopy(self.display_board_state)
                    for cylce_height in range(self.height):
                        for cycle_width in range(self.width):
                            if self.display_board_state[cylce_height][cycle_width] == '0':
                                for step in range(-1,2):
                                    for square in range(-1,2):
                                        try:
                                            height_index = cylce_height + step
                                            width_index = cycle_width + square
                                            if height_index >= 0 and width_index >= 0:
                                                self.display_board_state[height_index][width_index] = self.playing_board_state[height_index][width_index]
                                        except IndexError:
                                            pass
                    if temp_board == self.display_board_state:
                        break
            # Return False for the game no longer being active and True for victory
            victory = self.check_victory()
            if victory:
                return [False, True]
            # Return True for the game still being active and False for no victory
            else:
                return [True, False]


        

class Player:
    def get_width():
        return int(input(f"Please enter desired board width (Minimum of {min_width} - Maximum of {max_width}): "))

    def get_height():
        return int(input(f"Please enter desired board width (Minimum of {min_height} - Maximum of {max_height}): "))

    def get_difficulty():
        while True:
            choice = input(f"Please enter number of desired difficulty: 1. Easy - 2. Medium - 3. Expert: ")
            choice = choice.lower()
            if choice == '1' or choice == 'easy':
                return 'Easy'
            elif choice == '2' or choice == 'medium':
                return 'Medium'
            elif choice == '3' or choice == 'expert':
                return 'Expert'
            else:
                print("Unknown choice. Please try choosing a difficulty again.")
    
    def choose_square(width, height):
        row = 0
        column = 0
        marking = False
        # Take input coordinates and if the square should be marked or not
        while True:
            clean_data = True
            choice = input(f"Please input the square you wish to check (E.g. A5). You may mark a square by putting an M at the end (E.g. A5M): ")
            if choice[-1] == 'M':
                row_choice = choice[0]
                column_choice = int(choice[1:-1]) - 1
                marking = True
            else:
                row_choice = choice[0]
                column_choice = int(choice[1:]) - 1
            # Convert and confirm that data is usable
            # Make sure the row choice is a valid and existing letter
            if type(row_choice) == type('String'):
                row_list = ascii_uppercase[0:height]
                row_choice = row_choice.upper()
                if row_choice in row_list:
                    row = row_list.index(row_choice)
                else:
                    print("It appears that you entered a letter row outside of the ones on the board.  Please try again.")
                    clean_data = False
            else:
                print("It appears that you did not enter a letter row as your first character. Please try again.")
                clean_data = False
            # Make sure the column choice is a valid and existing row
            if type(column_choice) == type(1):
                if column_choice < 0 or column_choice > width:
                    print("It appears that you entered a column number outside of the ones on the board.  Please try again.")
                    clean_data = False
                else:
                    column = column_choice
            else:
                print("It appears that you did not enter a number for your column row.  Please try again.")
                clean_data = False
            # Return data if it is usable
            if clean_data:
                return [row, column, marking]
    
    def play_again():
        choice = input("Would you like to play again? 1. Yes - 2. No: ")
        choice = choice.lower()
        if choice == '1' or choice == 'y' or choice == 'yes':
            return True
        elif choice == '2' or choice == 'n' or choice == 'no':
            return False
        else:
            print("Unknown choice. Please try entering 1 for Yes and 2 for No again.")

# Global variables
max_width = 32
max_height = 24
min_width = 6
min_height = 6

if __name__ == '__main__':
    playing = True
    while playing:
        game_active = True
        game_won = False
        result = []

        chosen_width = Player.get_width()
        chosen_height = Player.get_height()
        chosen_difficulty = Player.get_difficulty()

        player_board = Board(chosen_width, chosen_height, chosen_difficulty)

        while game_active:
            player_board.draw_board(player_board.display_board_state)
            chosen_square = Player.choose_square(player_board.width, player_board.height)
            player_row = chosen_square[0]
            player_column = chosen_square[1]
            player_marking = chosen_square[2]
            result = player_board.update_board(player_row, player_column, player_marking)
            game_active = result[0]
        
        did_win = result[1]
        if did_win == True:
            player_board.draw_board(player_board.display_board_state)
            print("Congratulations! You won!")
        else:
            player_board.draw_board(player_board.playing_board_state)
            print("Game over. You chose a mine and blew up.")
        playing = Player.play_again()