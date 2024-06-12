NUM_COLUMNS = 7
NUM_ROWS = 6
BLANK_CELL = '<>'
PLAYER_COLORS = {
    1: 'R',
    2: 'Y'
}

class ConnectFour:
    def __init__(self):
        self.board = [[BLANK_CELL for _ in range(NUM_COLUMNS)] for _ in range(NUM_ROWS)]
        self.current_player = 1
        self.game_over = False
        self.history = []

    def animate(self):
        print()
        for row in self.board:
            print('\t'.join(cell for cell in row))
        print()

    def has_consecutive_k(self, k):
        for i in range(NUM_ROWS):
            for j in range(NUM_COLUMNS):
                if self._check_consecutive(i, j, 0, 1, k) or \
                   self._check_consecutive(i, j, 1, 0, k) or \
                   self._check_consecutive(i, j, 1, 1, k) or \
                   self._check_consecutive(i, j, 1, -1, k):
                    return True, PLAYER_COLORS[self.current_player]
        return False, ''

    def _check_consecutive(self, x, y, dx, dy, k):
        current = self.board[x][y]
        for i in range(1, k):
            new_x, new_y = x + i * dx, y + i * dy
            if not (0 <= new_x < NUM_ROWS and 0 <= new_y < NUM_COLUMNS) or self.board[new_x][new_y] != current:
                return False
        return current in PLAYER_COLORS.values()

    def validate_column(self, col):
        if col.lower() == 'undo':
            self.undo()
            
        while col == '' or col not in ''.join([str(i) for i in range(1, NUM_COLUMNS + 1)]):
            col = input(f'Enter a number between 1 and {NUM_COLUMNS}: ')

        return int(col) - 1

    def undo(self):
        if self.history == []:
            print('There is no history to undo.')
        else:
            self.history.pop()
            self.board = history[-1]
            self.animate(self.board)

    def play(self):
        self.animate()
        while not self.game_over:
            col = input(f'Player {self.current_player} - enter column: ')
            col = self.validate_column(col)

            while self.board[0][col] != BLANK_CELL:
                col = input(f'Column {col} is already full. Please choose another column: ')
                col = self.validate_column(col)

            row = NUM_ROWS - 1
            while self.board[row][col] != BLANK_CELL:
                row -= 1
            self.board[row][col] = PLAYER_COLORS[self.current_player]

            self.history.append(self.board)
            self.animate()

            result = self.has_consecutive_k(4)
            if result[0]:
                print(f'Player {self.current_player} wins!')
                self.game_over = True

            self.current_player = 2 if self.current_player == 1 else 1


if __name__ == "__main__":
    game = ConnectFour()
    game.play()
