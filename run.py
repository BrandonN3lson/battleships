import random
from random import randint

class Board:
    """
    Class for the grid layout of the battleship game
    """
    def __init__(self,size):
        self.size = size
        self.grid = [["~" for x in range(size)]  for y in range(size)]

    def display_grid (self):
        """
        Method for displaying empty grid.
        Using map() to iterate over range of grid size.
        and convert numbers to strings to be printed for x (column) co_ordinate.
        Using enumerate() to iterate over the row of the grid and place A,B,C etc..
        for y (row) co_ordinates.
        """
        # first" " = aligns numbers to grid.
        # second" "= space between numbers
        
        print("   "+" ".join(map(str,range(1, self.size + 1))))
        for index, row in enumerate(self.grid):
            print(chr(ord("A") + index) + "  " + " ".join(row))

#sub_class for user display grid
class UserGrid(Board):
    def __init__(self,size):
        super().__init__(size)
        self.user_ships = []
        self.user_shots = []
    
    
    def user_guesses(self, opponent_grid):
            while True:

                user_guess = input("Enter Co-ordinates, eg, A3, B4, C5...:\n").upper()
                
                #validate user guess is within parameters
                if len(user_guess) < 2 or not user_guess[0].isalpha() or not user_guess[1:].isdigit():
                    print("invalid input, guess length has to be 2, starting with a letter followed by a number\n")
                    print("example: A1, B2, C3..." )
                    print("Please enter again:\n")
                    continue

                row = ord(user_guess[0]) - ord("A")
                column = int(user_guess[1:]) - 1

                #validates that user guess is within range of grid
                if row < 0 or row >= self.size or column < 0 or column >= self.size:
                    print(f"Your guess {user_guess} is outside grid. Please enter again:\n")
                    continue

                if (row,column) in self.user_shots:
                    print("You've already guessed this. please try again:\n")
                    continue

                
                self.user_shots.append((row,column))
                #opponent_grid referencing function argument when opponent display is passed into function
                if opponent_grid.grid[row][column] == "@":
                    opponent_grid.grid[row][column] = "X"
                    print("\nUser: HIT!")
                    break
                    
                else:
                    opponent_grid.grid[row][column] = "o"
                    print("\neUser: MISSED")
                    break
                
                
                


#sub_class for opponent display grid
class OpponentGrid(Board):
    def __init__(self,size):
        super().__init__(size)
        self.opponent_ships = []
        self.opponent_shots = []

    def hide_ships (self):
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

    def display_hidden_grid (self):
        """displays grid with hidden ships"""

        hidden_grid = self.hide_ships()
        print("   "+" ".join(map(str,range(1, self.size + 1))))
        for index, row in enumerate(hidden_grid):
            print(chr(ord("A") + index) + "  " + " ".join(row))
    
    def opponent_guess (self,user_grid):
        while True:
                row = randint(1,self.size - 1)
                column = randint(1,self.size - 1)

                if (row,column) in self.opponent_shots:
                    continue

                self.opponent_shots.append((row,column))

                if user_grid.grid[row][column] == "@":
                    user_grid.grid[row][column] = "X"
                    print("Enemy: HIT!")
                    break
                else:
                    user_grid.grid[row][column] = "o"
                    print("Enemy: MISSED")
                    break




    
#Class for storing different ship nmes,sizes and method to position and place on grids.
class Ship:
    def __init__(self,name,size):
        self.name = name
        self.size = size
        self.position = []
    

    def place_ships(self,grid):
        """
        places ships on grid and randomly chooses orientation and position of ships.
        checks to make sure ships dont overlap eachother.
        creates symbole for ships
        """
        placed = False

        while not placed:
            orientation = random.choice(["horizontal", "vertical"])

            #orientates ships horizontally
            if orientation == "horizontal":
                row_position = randint(0, grid.size - 1)
                column_position = randint(0, grid.size - self.size)
                placed = True

                #validation for making sure ships dont overlap while being placed
                for i in range(self.size):
                    if grid.grid[row_position][column_position + i] != "~":
                        placed = False
                        break

            # asigning symbole @ for ships
                if placed:
                    for i in range(self.size):
                        grid.grid[row_position][column_position + i] = "@"
                        self.position.append((row_position,column_position + i))
            
            elif orientation == "vertical":
                row_position = randint(0, grid.size - self.size)
                column_position = randint(0,grid.size - 1)
                placed = True

                #validation for making sure ships dont overlap while being placed
                for i in range(self.size):
                    if grid.grid[row_position + i][column_position] != "~":
                        placed = False
                        break

            # asigning symbole @ for ships
                if placed :
                    for i in range(self.size):
                        grid.grid[row_position + i][column_position] = "@"
                        self.position.append((row_position + i, column_position))

        


def difficulty(user_choice):
    """
    defining types of battleships used and grid size 
    for different game difficulties:
        e = easy, m = medium, h = hard
    """
    carrier = Ship("Carrier", 5)
    battleship = Ship("Battleship", 4)
    cruiser = Ship("Cruiser", 3)
    submarine = Ship("Submarine", 3)
    destroyer = Ship("Destroyer", 2)

    user_ships = []
    opp_ships = []
    grid_size = 0

    if user_choice == "E":
        #easy difficulty
        grid_size = 6
        user_ships.extend([battleship, cruiser, destroyer])
        opp_ships.extend([battleship, cruiser, destroyer])
        
    elif user_choice == "M":
        #medium difficulty
        grid_size = 8
        user_ships.extend([carrier, battleship, cruiser, submarine, destroyer])
        opp_ships.extend([carrier, battleship, cruiser, submarine, destroyer])

    elif user_choice == "H":
        #hard difficulty
        grid_size = 10
        user_ships.extend([carrier, battleship, cruiser, submarine, destroyer])
        opp_ships.extend([carrier, battleship, cruiser, submarine, destroyer])
    else:
        print("\nUnrecognised choice!")
        return None,None,None


    return user_ships, opp_ships, grid_size



def play_battleships():
    """
    Main function to play game
    """ 
    print("\nwelcome to battleships\n")


    #get user input on difficulty
    while True:
        choice = input("Enter difficulty choice:\nEasy('E'), Medium('M') or Hard('H')\n").upper()
        user_ships, opp_ships ,grid_size = difficulty(choice)

        if user_ships is not None:
            break

    #initialize battlefield on users choice
    
    user_display = UserGrid(grid_size)
    opponent_display = OpponentGrid(grid_size)

    #place ships for user
    for ship in user_ships:
        ship.place_ships(user_display)
        user_display.user_ships.append(ship)

    #places ships for opponent
    for ship in opp_ships:
        ship.place_ships(opponent_display)
        opponent_display.opponent_ships.append(ship)

    def check_win(user_grid,opponent_grid):
        """
        checks result by comparing the amount of 'hits'("H") to
        the total number of ship parts on the opponent grid. 
        """
        user_hits = sum(row.count("X") for row in user_grid.grid)
        opponent_hits = sum(row.count("X") for row in opponent_grid.grid)

        user_ship_parts =sum(len(ship.position) for ships in user_grid.user_ships)
        opponent_ship_parts =sum(len(ship.position) for ships in opponent_grid.opponent_ships)

        if user_hits == opponent_ship_parts:
            print("You Win")
        elif opponent_hits == user_ship_parts:
            print("You Lose!")

    while True:
        
        print("\n       User:")
        print()
        user_display.display_grid()
        
        print("\n       Enemy:")
        print()
        opponent_display.display_hidden_grid()

        result = check_win(user_display, opponent_display)

        user_display.user_guesses(opponent_display)
        if result:
            print(result)
            break

        opponent_display.opponent_guess(user_display)
        
        if result:
            print(result)
            break
        
    
play_battleships()
