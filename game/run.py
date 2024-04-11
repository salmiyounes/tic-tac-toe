#! /usr/bin/env python3

import os
import sys
import time
import pygame
from Const.const import *
from pygame.locals import *
from pyautogui import confirm
from Logic.logic import TicTacToe
from Player.player import NormalPlayer, Computer, SmartComputer

class Play :

    def __init__(self) :
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('TicTacToe game')
        self.font = pygame.font.SysFont("Italic", 80)
        self.x_img = 'Images/Tc-X-min.png' 
        self.o_img = 'Images/Tc-O-min.png'
        self.FPS = pygame.time.Clock()
        assert os.path.isfile(self.o_img)
        assert os.path.isfile(self.x_img)

    def switch_player(self, player : str) -> str :
        return 'O' if player == 'X' else 'X'

    def draw_grid(self) :
        for i in range(3) :
            rect = (BLOCK_SIZE * i, BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            rect2 = (BLOCK_SIZE, BLOCK_SIZE * i, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(SCREEN, BLACK, rect, 1)
            pygame.draw.rect(SCREEN, BLACK, rect2, 1)
        pygame.display.flip()

    def restart(self, game : TicTacToe) -> None :
        game.clear_board()
        self.main_loop()
        return None

    def _message(self, player = None, Win = False, Draw = False, Retstart = False, game=False) -> None :
        if Win :
            SCREEN.fill(WHITE, (200, 650, 133, 34))
            msg = self.font.render('{} Wins !!'.format(player), True, BLACK)
            SCREEN.blit(msg, (200, 650))
        elif Draw :
            msg = self.font.render('Draw', True, BLACK)
            SCREEN.blit(msg, (220, 650))
        elif Retstart and game :
            self.restart(game)
        return None

    def draw_char(self, x : int , y : int, player : str, game : TicTacToe) -> None :
        assert ( (x in range(0, 3)) == True)
        assert ( (y in range(0, 3)) == True)
        if player == 'O' :
            img = pygame.image.load(self.o_img)
        elif player == 'X' :
            img = pygame.image.load(self.x_img)
        img = pygame.transform.scale(img, (BLOCK_SIZE, BLOCK_SIZE))
        SCREEN.blit(img, (y * BLOCK_SIZE, x * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        return None

    def human_computer(self, player1 : str, player2 : str, game : TicTacToe) :
        curr_player = player1
        geame_over = False
        while True :
            self.draw_grid()
            if curr_player == player1 :
                for event in pygame.event.get() :
                    if event.type == pygame.QUIT :
                        pygame.quit()
                        sys.exit()
                    if event.type == MOUSEBUTTONUP :
                        x, y = pygame.mouse.get_pos()
                        col, row = x // BLOCK_SIZE, y // BLOCK_SIZE
                        if game.board[row][col] is None and not geame_over :
                            self.draw_char(row, col, player1, game)
                            NormalPlayer(player1).make_move(row, col, game)
                            curr_player = self.switch_player(curr_player)
                        _, win = game.winner(player1) 
                        if win :
                            self._message(player1, Win=True)
                            geame_over = True
                        elif game.full_board() :
                            self._message(Draw=True)
                    if event.type == pygame.KEYDOWN: 
                        if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT :
                            self.restart(game)

            if curr_player == player2 :
                if not game.full_board() and not geame_over :
                    e_x, e_y = Computer(player2).make_move(game)
                    self.draw_char(e_x, e_y, player2, game)
                    _, check= game.winner(player2) 
                    if check :
                        self._message(player2, Win=True)
                        geame_over = True
                elif game.full_board() :
                    self._message(Draw=True)
                curr_player = self.switch_player(curr_player)
            pygame.display.flip()
            self.FPS.tick(60)

    def human_s_computer(self, player1 : str, player2 : str, game : TicTacToe) :
        curr_player = player1
        geame_over = False
        while True :
            self.draw_grid()
            if curr_player == player1 :
                for event in pygame.event.get() :
                    if event.type == pygame.QUIT :
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN  :
                        if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT :
                            self._message(Retstart=True, game=game)
                    if event.type == MOUSEBUTTONUP :
                        x, y = pygame.mouse.get_pos()
                        col, row = x // BLOCK_SIZE, y // BLOCK_SIZE
                        try :
                            if game.board[row][col] is None  and not geame_over :
                                self.draw_char(row, col, player1, game)
                                NormalPlayer(player1).make_move(row, col, game)
                                curr_player = self.switch_player(curr_player)
                        except TypeError as e :
                            pass
                        _, win = game.winner(player1) 
                        if win :
                            self._message(player1, Win=True)
                            geame_over = True
                        elif game.full_board() :
                            self._message(Draw=True)

            if curr_player == player2 :
                x, y = SmartComputer(curr_player).best_move(game)
                try :
                    if game.board[x][y] is None and not geame_over:
                        game.board[x][y] = curr_player
                        self.draw_char(x, y, curr_player, game)
                except TypeError as e :
                    pass
                _, check = game.winner(curr_player)
                if check :
                    self._message(curr_player, Win=True)
                    geame_over = True
                elif game.full_board() :
                    self._message(Draw=True)
                curr_player = self.switch_player(curr_player)
            pygame.display.flip()
            self.FPS.tick(60)
    def human_x_human(self, player1 : str, player2 : str, game : TicTacToe) :
        curr_player = player1
        geame_over = False

        while True :
            self.draw_grid()
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT :
                        self._message(Retstart=True, game=game)
                if event.type == MOUSEBUTTONUP :
                    x, y = pygame.mouse.get_pos()
                    col, row = x // BLOCK_SIZE, y // BLOCK_SIZE
                    if curr_player == player1 :
                        try :
                            if game.board[row][col] is None  and not geame_over :
                                self.draw_char(row, col, player1, game)
                                NormalPlayer(player1).make_move(row, col, game)
                                curr_player = self.switch_player(curr_player)
                        except TypeError as e :
                            pass
                        _, win = game.winner(player1) 
                        if win :
                            self._message(player1, Win=True)
                            geame_over = True
                        elif game.full_board() :
                            self._message(Draw=True)
                    elif curr_player == player2 :
                        try :
                            if game.board[row][col] is None  and not geame_over :
                                self.draw_char(row, col, player2, game)
                                NormalPlayer(player2).make_move(row, col, game)
                                curr_player = self.switch_player(curr_player)
                        except TypeError as e :
                            pass
                        _, win = game.winner(player2) 
                        if win :
                            self._message(player2, Win=True)
                            geame_over = True
                        elif game.full_board() :
                            self._message(Draw=True)

    def main_loop(self) :
        _confirm = confirm(text='Choose type of playing', buttons=BUTTONS)
        the_chosen_player = confirm(text='Choose player', buttons=PLAYERS)
        assert (_confirm is not None)
        assert (the_chosen_player is not None)
        global SCREEN
        SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        SCREEN.fill(WHITE)
        player1 = the_chosen_player # default player 'X'
        player2 = self.switch_player(the_chosen_player)
        game = TicTacToe() # get the game logic
        curr_player = player1 # i can add random choosing feature

        if _confirm == 'Dumb Computer' :
            self.human_computer(player1, player2, game)
        elif _confirm == 'Human vs Human' :
            self.human_x_human(player1, player2, game)
        elif _confirm == 'Smart Computer' :
            
            self.human_s_computer(player1, player2, game)


if __name__ == '__main__':
    Play().main_loop()

