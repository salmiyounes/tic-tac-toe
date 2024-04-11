
from typing import List, Tuple, Optional

class TicTacToe:

    def __init__(self):
        self.board = [[None] * 3 for _ in range(3)]
        self.corner = [0, 2]

    def __repr__(self):
        return f'<TicTacToe board state: {self.board}>'

    def count_non_empty_places(self) -> int :
        count = 0
        for i in range(3) :
            for j in range(3) :
                if not self.board[i][j] is None :
                    count += 1
        return count 

    def fill_board(self, row: int, pos: int, player: str) -> None:
        if self.board[row][pos] is None: 
            self.board[row][pos] = player
        else:
            raise NotGoodMove('Click inside an empty space only')

    def full_board(self) -> bool:
        return all(self.board[i][j] is not None for i in range(3) for j in range(3))

    def clear_board(self) -> None:
        self.board = [[None] * 3 for _ in range(3)]

    def board_is_clear(self) -> bool:
        return all(self.board[i][j] is None for i in range(3) for j in range(3))

    def check_row(self, row: int, player: Optional[str] = None) -> bool:
        return all(self.board[row][i] == player for i in range(3))

    def check_col(self, pos: int, player: Optional[str] = None) -> bool:
        return all(self.board[i][pos] == player for i in range(3))

    def check_diag(self, player: str) -> bool:
        return (all(self.board[i][i] == player for i in range(3)) or
                all(self.board[i][2 - i] == player for i in range(3)))

    def winner(self, player: str) -> Tuple[Optional[str], bool]:
        for row in range(3):
            for pos in range(3):
                if self.board[row][pos] is not None:
                    if row == 1 and pos == 1:  # special case (1, 1)
                        if (self.check_col(pos, player) or
                            self.check_row(row, player) or
                            self.check_diag(player)):
                            return player, True
                    elif pos in self.corner:
                        if (self.check_col(pos, player) or
                            self.check_row(row, player) or
                            self.check_diag(player)):
                            return player, True
                    else:
                        if self.check_col(pos, player) or self.check_row(row, player):
                            return player, True
        return None, False
# Errors 

class NotGoodMove(Exception):
    pass