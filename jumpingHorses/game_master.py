import pygame
import jumpingHorses.constants as Constants
from .constants import BLACK_PIECE, WHITE_PIECE, MOVE_COLOR, MOVE_RADIUS, SQUARE_SIZE, WIDTH, HEIGHT, LETTER_GAP_SIZE, OUTLINE_SIZE
from .board import Board
from menu.main_menu import MainMenu
import menu.gameState as GameState

class GameMaster:
    #inicializē
    def __init__(self, surface):
        self._init()
        self.surface = surface
    #atjaunina to, kas redzams ekrānā
    def update(self):
        self.board.draw(self.surface)
        if self.selectedPiece != None:
            self.draw_valid_moves(self.valid_moves)
    #sāk no jauna spēli
    def reset(self):
        self._init()
    #notīra esošo stāvokli
    def _init(self):
        self.selectedPiece = None
        self.turn = WHITE_PIECE
        self.board = Board()
        self.valid_moves = {}
    #pārbauda, vai var izvēlēties
    def select(self, pos):
        if LETTER_GAP_SIZE < pos[0] < WIDTH+LETTER_GAP_SIZE and pos[1] < HEIGHT:
            row, col = self.get_row_col_from_mouse(pos)
            if self.selectedPiece:#ja kaut kas jau ir izvēlēts
                result = self._move(row, col)#tad to pabīda, ja ir legāls gājiens
                self.selectedPiece = None
                if not result:#ja neidzodas pabīdīt(izvēlas neiespējamu gājienu, vai kaut ko citu), tad selecto pa jaunam
                    self.selectedPiece = None
                    self.select(pos)
                    return True
            #ja kaut kas tiek izvēlēts pirmo reizi, vai tika izvēlēts kaut kas, kas nebija iespējams gājiens
            piece = self.board.get_piece(row, col)
            if piece != 0 and piece.color == self.turn:
                self.selectedPiece = piece
                self.valid_moves = self.board.get_valid_moves(piece)
                return True
        self.selectedPiece = None
        return False
    #pārvieto kauliņu
    def _move (self, row, col):
        piece = self.board.get_piece(row,col)
        if self.selectedPiece and piece == 0 and (row,col) in self.valid_moves:
            self.board.move(self.selectedPiece, row, col)
            self.change_turn()
        else:
            return False

        return True
    #samaina gājienu
    def change_turn(self):
        self.valid_moves = {}
        if self.turn == BLACK_PIECE:
            self.turn = WHITE_PIECE
        else:
            self.turn = BLACK_PIECE

    #uzzīmē legālos gājienus
    def draw_valid_moves(self, moves):
        pygame.draw.circle(self.surface, (0,255,0), (self.selectedPiece.x, self.selectedPiece.y), self.selectedPiece.radius+OUTLINE_SIZE, 5)
        for move in moves:
            row, col = move
            pygame.draw.circle(self.surface, MOVE_COLOR, (col*SQUARE_SIZE + SQUARE_SIZE//2, row*SQUARE_SIZE + SQUARE_SIZE//2) , MOVE_RADIUS)

    #atgriež rindu un kolonnu atkarībā no peles pozīcijas
    def get_row_col_from_mouse(self, pos):
        x, y = pos
        row = y // SQUARE_SIZE
        col = (x - LETTER_GAP_SIZE) // SQUARE_SIZE
        return row, col
    #dators veic gājienu
    def ai_move(self, board):
        self.board = board
        self.change_turn()
    #pārbauda, vai ir uzvarētājs
    def check_winner(self):
        if self.board.winner() == Constants.starting_player[1]:
            GameState.currentState = GameState.State.win
        elif self.board.winner() == Constants.starting_player[2]:
            GameState.currentState = GameState.State.lost

    def get_board(self):
        #print("get_board called")
        #self.board.print_board()
        return self.board
