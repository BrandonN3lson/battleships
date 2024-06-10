import random

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


user_display = UserGrid(10)
opponent_display = OpponentGrid(10)
print("User Display:\n")
user_display.display_grid()
print("\nOpponent Display:")
opponent_display.display_grid()