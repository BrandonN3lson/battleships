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
    
class UserGrid(Board):
    def __init__(self,size):
        super().__init__(size)
        self.user_ships = []
        self.user_shots = []

class OpponentGrid(Board):
    def __init__(self,size):
        super().__init__(size)
        self.opponent_ships = []
        self.opponent_shots = []


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

    if user_choice == "e":
        #easy difficulty

        grid_size = 6
        user_ships.extend([battleship, cruiser, destroyer])
        opp_ships.extend([battleship, cruiser, destroyer])
        

    elif user_choice == "m":
        #medium difficulty

        grid_size = 8
        user_ships.extend([carrier, battleship, cruiser, submarine, destroyer])
        opp_ships.extend([carrier, battleship, cruiser, submarine, destroyer])

    elif user_choice == "h":
        #hard difficulty
        grid_size = 10
        user_ships.extend([carrier, battleship, cruiser, submarine, destroyer])
        opp_ships.extend([carrier, battleship, cruiser, submarine, destroyer])

    return user_ships, opp_ships, grid_size


#get user input on difficulty
choice = input("Enter difficulty choice:\neasy('e'), medium('m') or hard('h')\n")


#initialize battlefield on users choice
user_ships, opp_ships ,grid_size = difficulty(choice)
user_display = UserGrid(grid_size)
opponent_display = OpponentGrid(grid_size)


#place ships for user
for ship in user_ships:
    ship.place_ships(user_display)
    user_display.user_ships.append(ship)

#places ships for user
for ship in opp_ships:
    ship.place_ships(opponent_display)
    opponent_display.opponent_ships.append(ship)


print("User Display:")
user_display.display_grid()
print("\nOpponent Display:")
opponent_display.display_grid()