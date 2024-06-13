from copy import deepcopy

NUM_COLUMNS = 7
NUM_ROWS = 6
BLANK_CELL = '<>'
PLAYER_COLORS = {
    1: 'R',
    2: 'Y'
}
BLANK_BOARD = [[BLANK_CELL for _ in range(NUM_COLUMNS)] for _ in range(NUM_ROWS)]

history = []

class Board:
    def __init__(self, board):
        self.board = board

class Game:
    def __init__(self):
        self.board = Board(BLANK_BOARD).board
        self.current_player = 1
        self.game_over = False
        #self.history = [self.board]

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
        while col == '' or col not in ''.join([str(i) for i in range(1, NUM_COLUMNS + 1)]):
            col = input(f'Enter a number between 1 and {NUM_COLUMNS}: ')

        return int(col) - 1

    def undo(self):
        #print(self.history)
        print(self.board)
        print(history)
        #if self.history == [BLANK_BOARD]:
        if history == [BLANK_BOARD]:
            print('There is no history to undo.')
        else:
            '''
            self.history.pop()
            self.board = self.history[-1]
            '''
            history.pop()
            self.board = history[-1]
            self.animate()
            game.current_player = 2 if game.current_player == 1 else 1

def play(game):
    #game.board = Board(game.history[-1]).board
    history.append(BLANK_BOARD)
    game.animate()

    while not game.game_over:
        #history.append(BLANK_BOARD)
        #game.board = Board(game.history[-1]).board
        game.board = history[-1]

        col = input(f'Player {game.current_player} - enter column: ')
        while col.lower() == 'undo':
            game.undo()
            col = input(f'Player {game.current_player} - enter column: ')
        
        col = game.validate_column(col)

        while game.board[0][col] != BLANK_CELL:
            col = input(f'Column {col} is already full. Please choose another column: ')
            col = game.validate_column(col)

        row = NUM_ROWS - 1
        while game.board[row][col] != BLANK_CELL:
            row -= 1
        print('history before move')
        print(history)
        current_board = deepcopy(game.board)
        history[-1] = current_board
        game.board[row][col] = PLAYER_COLORS[game.current_player]

        #game.history.append(game.board)
        print('history after move')
        print(history)
        print('board')
        print(game.board)
        history.append(game.board)
        print('history after append')
        print(history)
        #game.history.append(game.history[-1])
        game.animate()

        result = game.has_consecutive_k(4)
        if result[0]:
            print(f'Player {game.current_player} wins!')
            game.game_over = True

        game.current_player = 2 if game.current_player == 1 else 1


if __name__ == "__main__":
    game = Game()
    play(game)
