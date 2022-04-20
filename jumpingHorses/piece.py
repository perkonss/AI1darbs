import pygame
from .constants import SQUARE_SIZE, OUTLINE_SIZE, OUTLINE_COLOR, GAP, WHITE_PIECE, BLACK_PIECE
#kauliņa klase
class Piece:
    #inicializē
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.x = 0
        self.y = 0
        self.radius = SQUARE_SIZE//2 - GAP
        self.calculate_position()
    #aprēķina savu pozīciju
    def calculate_position(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE//2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE//2
    #kauliņš uzzīmē sevi
    def draw(self, window):
        pygame.draw.circle(window, OUTLINE_COLOR, (self.x, self.y), self.radius + OUTLINE_SIZE)
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)
    def move(self, row, col):
        self.row = row
        self.col = col
        self.calculate_position()

    def __repr__(self):
        if self.color == WHITE_PIECE:
            return f"{self.row+1} {self.col+1} W"
        else:
            return f"{self.row+1} {self.col+1} B"


