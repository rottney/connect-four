import os
from termcolor import colored
from copy import deepcopy


NUM_COLUMNS = 7
NUM_ROWS = 6
BLANK_CELL = colored("o", "blue")
PLAYER_COLORS = {
    1: colored("1", "red"),
    2: colored("2", "yellow")
}
BLANK_BOARD = [[BLANK_CELL for _ in range(NUM_COLUMNS)] for _ in range(NUM_ROWS)]

def cls():
    os.system("cls" if os.name == "nt" else "clear")


class Game:
    def __init__(self):
        self.board = deepcopy(BLANK_BOARD)
        self.current_player = 1
        self.game_over = False
        self.history = [self.board]

    def animate(self):
        cls()

        for row in self.board:
            print("\t".join(cell for cell in row))

        print(f"\nPlayer {self.current_player} turn")
    
    def swap_player(self):
        self.current_player = 2 if self.current_player == 1 else 1

    def undo(self):
        if self.history == [BLANK_BOARD]:
            print("There is no history to undo.")
        else:
            self.history.pop()
            self.board = self.history[-1]
            self.swap_player()
            self.animate()

    def has_consecutive_k(self, k):
        def check_consecutive(x, y, dx, dy, k):
            current = self.board[x][y]

            for i in range(1, k):
                new_x, new_y = x + i * dx, y + i * dy

                if not (0 <= new_x < NUM_ROWS and 0 <= new_y < NUM_COLUMNS) or \
                        self.board[new_x][new_y] != current:
                    return False
                
            return current in PLAYER_COLORS.values()
        
        for i in range(NUM_ROWS):
            for j in range(NUM_COLUMNS):
                if check_consecutive(i, j, 0, 1, k) or \
                   check_consecutive(i, j, 1, 0, k) or \
                   check_consecutive(i, j, 1, 1, k) or \
                   check_consecutive(i, j, 1, -1, k):
                    return True
                
        return False

    def validate_column(self, col):
        while col == "" or col not in "".join([str(i) for i in range(1, NUM_COLUMNS + 1)]):
            col = input(f"Enter a number between 1 and {NUM_COLUMNS}: ")

            if col.lower() == "undo":
                self.undo()

        return int(col) - 1


def play(game):
    game.animate()

    while not game.game_over:
        game.board = game.history[-1]

        col = input(f"Player {game.current_player} - enter column: ")
        while col.lower() == "undo":
            game.undo()
            col = input(f"Player {game.current_player} - enter column: ")
        
        col = game.validate_column(col)
        while game.board[0][col] != BLANK_CELL:
            col = input(f"Column {col} is already full. Please choose another column: ")
            if col.lower() == "undo":
                game.undo()
            col = game.validate_column(col)

        row = NUM_ROWS - 1
        while game.board[row][col] != BLANK_CELL:
            row -= 1
        
        current_board = deepcopy(game.board)
        game.history[-1] = current_board
        game.board[row][col] = PLAYER_COLORS[game.current_player]
        game.history.append(game.board)

        result = game.has_consecutive_k(4)
        if result:
            game.animate()
            print(f"Player {game.current_player} wins!")
            game.game_over = True
        else:
            game.swap_player()
            game.animate()


if __name__ == "__main__":
    game = Game()
    play(game)
