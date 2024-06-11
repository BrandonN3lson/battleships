import random
from random import randint

class Board:
    def __init__(self,size):
        self.size = size
        self.grid = [["~" for x in range(size)]  for y in range(size)]

    def display_grid (self):
        """
        method for displaying empty grid.

        Using map() to iterate over range of grid size
        and convert numbers to strings to be printed for co_ordinate.

        Using enumerate() to iterate over the row of the grid and place A,B,C etc..
        for row co_ordinates.

        """
        # first" " = aligns numbers to grid.
        # second" "= space between numbers
        print("   "+" ".join(map(str,range(1, self.size + 1))))
        for index, row in enumerate(self.grid):
            print(chr(ord("A") + index) + "  " + " ".join(row))
    
class UserGrid(Board):
    def __init__(self,size):
        super().__init__(size)

class OpponentGrid(Board):
    def __init__(self,size):
        super().__init__(size)

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


#testing grid
user_display = UserGrid(10)
opponent_display = OpponentGrid(10)

ship1 = Ship("Destroyer", 3)
ship2 = Ship("Cruiser", 3)

ship1.place_ships(user_display)
ship2.place_ships(opponent_display)

print("User Display:\n")
user_display.display_grid()
print("\nOpponent Display:")
opponent_display.display_grid()