import random
from random import randint
from os import system, name


# define our clear function
def clear():

    # for windows
    if name == "nt":
        _ = system("cls")

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system("clear")


class Board:
    """
    Class for the grid layout of the battleship game
    """

    def __init__(self, size):
        self.size = size
        self.grid = [["~" for x in range(size)] for y in range(size)]

    def display_grid(self):
        """
        Method for displaying empty grid.
        Using map() to iterate over range of grid size.
        Convert numbers to strings to be printed
        for x (column) co_ordinate.
        Using enumerate() to iterate over
        the row of the grid and place A,B,C etc..
        for y (row) co_ordinates.
        """
        # first" " = aligns numbers to grid.
        # second" "= space between numbers
        print("   " + " ".join(map(str, range(1, self.size + 1))))
        for index, row in enumerate(self.grid):
            print(chr(ord("A") + index) + "  " + " ".join(row))


class UserGrid(Board):
    """
    sub_class for user display grid
    """
    def __init__(self, size):
        super().__init__(size)
        self.user_ships = []
        self.user_shots = []

    def user_guesses(self, opponent_grid):
        """
        function for user to input guess, input gets validated and amended to
        user_shots, once input is amended, opponent_grid is updated.
        """
        while True:
            user_guess = input("\nEnter Co-ordinates, eg, A3\n Enter:").upper()
            # to cancel game and go back to difficulty selection
            if user_guess == "END":
                clear()
                play_battleships()

            # validate user guess is within parameters
            if (
                len(user_guess) < 2
                or not user_guess[0].isalpha()
                or not user_guess[1:].isdigit()
            ):
                print("invalid input, guess length has to be 2," +
                      "starting with a letter followed by a number\n")
                print("example: A1, B2, C3...")
                print("Please enter again:\n")
                continue

            row = ord(user_guess[0]) - ord("A")
            col = int(user_guess[1:]) - 1

            # validates that user guess is within range of grid
            if row < 0 or row >= self.size or col < 0 or col >= self.size:
                print(f"Your guess {user_guess} is outside grid." +
                      "Please enter again:\n")
                continue

            if (row, col) in self.user_shots:
                print("You've already guessed this. please try again:\n")
                continue

            self.user_shots.append((row, col))
            if opponent_grid.grid[row][col] == "@":
                opponent_grid.grid[row][col] = "X"
                return "HIT!"
                break

            else:
                opponent_grid.grid[row][col] = "o"
                return "MISSED"
                break


class OpponentGrid(Board):
    """
    sub_class for opponent display grid
    """
    def __init__(self, size):
        super().__init__(size)
        self.opponent_ships = []
        self.opponent_shots = []
        self.possible_shots = [
            (row, column) for row in range(size) for column in range(size)
        ]
        # shuffles shots stored in possible_shots
        random.shuffle(self.possible_shots)

    def hide_ships(self):
        """
        function to hide ships on opponent grid.
        self.grid is sliced and copied to the variable hidden_grid to use
        intead to prevent any changes to be made to the main Board grid
        """
        hidden_grid = [row[:] for row in self.grid]

        for x in range(self.size):
            for y in range(self.size):
                if hidden_grid[x][y] == "@":
                    hidden_grid[x][y] = "~"
        return hidden_grid

    def display_hidden_grid(self):
        """displays grid with hidden ships"""

        hidden_grid = self.hide_ships()
        print("   " + " ".join(map(str, range(1, self.size + 1))))
        for index, row in enumerate(hidden_grid):
            print(chr(ord("A") + index) + "  " + " ".join(row))

    def opponent_guess(self, user_grid):
        """
        function that removes one of thee shuffled possible_shots,
        amends that shot to opponent_shot and updates user_grid.
        """
        while self.possible_shots:
            row, column = (
                self.possible_shots.pop()
            )  # removes random shot from possible_shot

            if (row, column) in self.possible_shots:
                continue

            self.opponent_shots.append(
                (row, column)
            )  # moves/adds shot to opponent_shot
            if user_grid.grid[row][column] == "@":
                user_grid.grid[row][column] = "X"
                return "HIT!"
                break
            else:
                user_grid.grid[row][column] = "o"
                return "MISSED"
                break

        if not self.possible_shots:
            print("Enemy has no more possible shots")


class Ship:
    """
    Class for storing different ship names,
    sizes and method to position and place on grids.
    """
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.position = []

    def place_ships(self, grid):
        """
        places ships on grid and randomly chooses orientation
        and position of ships.
        checks to make sure ships dont overlap eachother.
        creates symbole for ships
        """
        placed = False

        while not placed:
            orientation = random.choice(["horizontal", "vertical"])

            # orientates ships horizontally
            if orientation == "horizontal":
                row = randint(0, grid.size - 1)
                column = randint(0, grid.size - self.size)
                placed = True

                # validation for ships overlapping.
                for i in range(self.size):
                    if grid.grid[row][column + i] != "~":
                        placed = False
                        break

                # asigning symbole @ for ships
                if placed:
                    for i in range(self.size):
                        grid.grid[row][column + i] = "@"
                        self.position.append((row, column + i))

            elif orientation == "vertical":
                row = randint(0, grid.size - self.size)
                column = randint(0, grid.size - 1)
                placed = True

                # validation for ships overlapping.
                for i in range(self.size):
                    if grid.grid[row + i][column] != "~":
                        placed = False
                        break

                # asigning symbole @ for ships
                if placed:
                    for i in range(self.size):
                        grid.grid[row + i][column] = "@"
                        self.position.append((row + i, column))


def easy(user_ships, opp_ships):
    """
    function to call list of ships used
    for easy difficulty
    """
    user_ships.extend([
            Ship("Battleship", 4),
            Ship("Cruiser", 3),
            Ship("Destroyer", 2)
    ])
    opp_ships.extend([
            Ship("Battleship", 4),
            Ship("Cruiser", 3),
            Ship("Destroyer", 2)
            ])


def medium(user_ships, opp_ships):
    """
    function to call list of ships used
    for medium difficulty
    """
    user_ships.extend([
            Ship("Carrier", 5),
            Ship("Battleship", 4),
            Ship("Cruiser", 3),
            Ship("Submarine", 3),
            Ship("Destroyer", 2),
        ])
    opp_ships.extend([
            Ship("Carrier", 5),
            Ship("Battleship", 4),
            Ship("Cruiser", 3),
            Ship("Submarine", 3),
            Ship("Destroyer", 2),
        ])


def hard(user_ships, opp_ships):
    """
    function to call list of ships used
    for hard difficulty
    """
    user_ships.extend([
            Ship("Carrier", 5),
            Ship("Battleship", 4),
            Ship("Cruiser", 3),
            Ship("Submarine", 3),
            Ship("Destroyer", 2),
        ])
    opp_ships.extend([
            Ship("Carrier", 5),
            Ship("Battleship", 4),
            Ship("Cruiser", 3),
            Ship("Submarine", 3),
            Ship("Destroyer", 2),
        ])


def difficulty(user_choice):
    """
    defining types of battleships used and grid size
    for different game difficulties:
        e = easy, m = medium, h = hard
    """
    user_ships = []
    opp_ships = []
    grid_size = 0

    if user_choice == "E":
        # easy difficulty
        grid_size = 6
        easy(user_ships, opp_ships)
    elif user_choice == "M":
        # medium difficulty
        grid_size = 8
        medium(user_ships, opp_ships)
    elif user_choice == "H":
        # hard difficulty
        grid_size = 10
        hard(user_ships, opp_ships)
    else:
        print("\nUnrecognised choice!")
        return None, None, None
    return user_ships, opp_ships, grid_size


def play_again():
    """
    function to play game again
    """
    replay = input("Would you like to play again? Yes('Y') or No('N')").upper()

    if replay == "Y":
        clear()
        play_battleships()
    elif replay == "N":
        clear()
        print("Thank you for playing!")
        play_again()


def play_battleships():
    """
    Main function to play game
    """
    print("\nwelcome to battleships")
    print("Find and destroy all Enemy ships to win.\n")


    # get user input on difficulty
    while True:
        choice = input(
            "Enter difficulty choice:\nEasy('E'), Medium('M') or Hard('H')\n"
        ).upper()
        user_ships, opp_ships, grid_size = difficulty(choice)

        if user_ships or opp_ships is not None:
            break

    # initialize battlefield on users choice

    user_display = UserGrid(grid_size)
    opponent_display = OpponentGrid(grid_size)

    # place ships for user
    for ship in user_ships:
        ship.place_ships(user_display)
        user_display.user_ships.append(ship)

    # places ships for opponent
    for ship in opp_ships:
        ship.place_ships(opponent_display)
        opponent_display.opponent_ships.append(ship)

    def check_win(user_grid, opponent_grid):
        """
        Get total number of ship parts left on the grid
        Once ship parts reaches 0, it returns "You win" or "You lose"
        """

        user_ship_parts = sum(row.count("@") for row in user_grid.grid)
        opponent_ship_parts = sum(row.count("@") for row in opponent_grid.grid)

        print(f"\nUser ship part left: {user_ship_parts}")
        print(f"Opponent ship parts left: {opponent_ship_parts}")

        if opponent_ship_parts == 0:
            return "You Win"
        elif user_ship_parts == 0:
            return "You Lose!"
        return None

    while True:
        print("\n_________User_________\n")
        user_display.display_grid()

        print("\n_________Enemy_________\n")
        opponent_display.display_hidden_grid()

        user_result = user_display.user_guesses(opponent_display)
        print(f"\nUser {user_result}")
        opp_result = opponent_display.opponent_guess(user_display)
        print(f"Enemy {opp_result}")
        print()

        result = check_win(user_display, opponent_display)
        if result:
            clear()
            print(result)
            play_again()


play_battleships()
