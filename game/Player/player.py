from typing import Tuple, List, Optional
from random import choice
from time import monotonic
import sys
from Logic.logic import TicTacToe

class NormalPlayer:

    def __init__(self, player: str):
        self.player = player

    def make_move(self, row: int, pos: int, game: TicTacToe) -> None:
        game.fill_board(row, pos, self.player)

class Computer:

    def __init__(self, player: str):
        self.ai = player
        self.human =  'O' if player == 'X' else 'X' 

    def make_move(self, game: TicTacToe) -> Tuple[int, int]:
        if not game.full_board():
            list_of_choices = [(i, j) for i in range(3) for j in range(3) if game.board[i][j] is None]
            row, pos = choice(list_of_choices)
            return row, pos
        return (None, None)

class SmartComputer(Computer):
    def __init__(self, player : str) :
        super().__init__(player)
        self.count: int = 0

    def evaluate_state(self, state: TicTacToe, is_ai: bool) -> int:
        ai_player, ai_win_state = state.winner(self.ai)
        human_player, human_win_state = state.winner(self.human)

        if is_ai:
            if ai_win_state:
                return 1
            elif human_win_state:
                return -1
        else:
            if human_win_state:
                return -1
            elif ai_win_state:
                return 1

        if state.full_board():
            return 0

        return None

    def best_move(self, state: TicTacToe) -> Tuple[int, int]:
        start = monotonic()
        best_score = float('-inf')
        best_move = (None, None)

        for i in range(3):
            for j in range(3):
                if state.board[i][j] is None:
                    state.board[i][j] = self.ai
                    score = self.minimax(state, False,  float('-inf'), float('inf'), 1)
                    state.board[i][j] = None
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        end = monotonic() - start
        print (('%d node explored in %.3f sec. \n') % (self.count, end))
        return best_move

    def minimax(self, state: TicTacToe, is_maximizing: bool, a: int, b: int, depth: int) -> int:
        result = self.evaluate_state(state, is_maximizing)
        self.count += 1
        if result is not None:
            return result

        if depth == 9 or state.full_board() :  # Maximum depth reached
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for i in range(3):
                for j in range(3):
                    if state.board[i][j] is None:
                        state.board[i][j] = self.ai
                        score = self.minimax(state, False, a, b, depth + 1)
                        state.board[i][j] = None
                        best_score = max(score, best_score)
                        if best_score > b:
                            break
                        a = max(a, best_score)

            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if state.board[i][j] is None:
                        state.board[i][j] = self.human
                        score = self.minimax(state, True, a, b ,depth + 1)
                        state.board[i][j] = None
                        best_score = min(score, best_score)
                        if best_score < a:
                            break
                        b = min(b, best_score)
            return best_score
