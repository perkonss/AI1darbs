import pygame
import jumpingHorses.constants as Constants
from jumpingHorses.constants import TOTAL_WIDTH, TOTAL_HEIGHT, FONT_SIZE, LETTER_GAP_SIZE, ROWS, COLS, WIDTH, INFO_SIZE, SQUARE_SIZE, HEIGHT, WHITE_PIECE, MAIN_MENU_COLOR
from .button import Button
import menu.gameState as GameState

class GameSecondary:
    def __init__(self, surface):
        self.surface = surface
        self.menu_color = MAIN_MENU_COLOR
        self.font = pygame.font.SysFont(None, FONT_SIZE)
        self.font_gaps = pygame.font.SysFont(None, LETTER_GAP_SIZE)
        self.font_time = pygame.font.SysFont(None, 30)
        self.setup()
        width = INFO_SIZE - LETTER_GAP_SIZE*2
        height = 50
        self.all_buttons =[Button(WIDTH+LETTER_GAP_SIZE*2, TOTAL_HEIGHT-LETTER_GAP_SIZE-height, width, height, self.font, "Atgriezties")]

    def update(self, event_list):    
        for button in self.all_buttons:
            button.update(event_list)
            button.draw(self.surface)
            if button.clicked == True:
                if button.text == "Atgriezties":
                    GameState.currentState = GameState.State.mainMenu
        pygame.display.update()

    def setup(self):
        if Constants.starting_player[1] == WHITE_PIECE:
            for i in range(COLS,0,-1): #uzzīmē ciparus
                self.draw_text(LETTER_GAP_SIZE//3, (COLS+1-i)*SQUARE_SIZE-0.5*SQUARE_SIZE-10, self.font_gaps, (0,0,0), str(i))
            for i in range(1, ROWS+1): #uzzīmē burtus
                self.draw_text((i-1)*SQUARE_SIZE+0.5*SQUARE_SIZE+LETTER_GAP_SIZE-10, HEIGHT+LETTER_GAP_SIZE//4, self.font_gaps, (0,0,0), chr(i+64))
        else:
            for i in range(COLS,0,-1):#uzzīmē ciparus
                self.draw_text(LETTER_GAP_SIZE//3, i*SQUARE_SIZE-0.5*SQUARE_SIZE-10, self.font_gaps, (0,0,0), str(i))
            for i in range(ROWS+1, 1, -1):#uzzīmē burtus
                self.draw_text((ROWS+1-i)*SQUARE_SIZE+0.5*SQUARE_SIZE+LETTER_GAP_SIZE-10, HEIGHT+LETTER_GAP_SIZE//4, self.font_gaps, (0,0,0), chr(i+63))

    def draw_text(self, x, y, font, color, text):
        text = font.render(text, 1, color)
        text_place = text.get_rect()
        text_place.topleft = (x,y)
        self.surface.blit(text, text_place)

    def draw_time_human(self, time, text):
        rect = pygame.Rect(LETTER_GAP_SIZE+WIDTH, 200, INFO_SIZE, 100)
        self.surface.fill(self.menu_color, rect)
        self.draw_text(TOTAL_WIDTH - INFO_SIZE + 0.5*LETTER_GAP_SIZE, 200, self.font_time, (0,0,0), f'{text}')
        self.draw_text(TOTAL_WIDTH - INFO_SIZE + 0.5*LETTER_GAP_SIZE, 250, self.font_time, (0,0,0), f'{time:.3f}')
    
    def draw_time_ai(self, time, text):
        rect = pygame.Rect(LETTER_GAP_SIZE+WIDTH, 350, INFO_SIZE, 100)
        self.surface.fill(self.menu_color, rect)
        self.draw_text(TOTAL_WIDTH - INFO_SIZE + 0.5*LETTER_GAP_SIZE, 350, self.font_time, (0,0,0), f'{text}')
        self.draw_text(TOTAL_WIDTH - INFO_SIZE + 0.5*LETTER_GAP_SIZE, 400, self.font_time, (0,0,0), f'{time:.3f}')
    
    def win(self, average_time_human, average_time_ai):
        if GameState.currentState == GameState.State.win:
            self.menu_color = (51, 204, 51)
        else:
            self.menu_color = (204,51,51)

        rect = pygame.Rect(LETTER_GAP_SIZE+WIDTH, 0, INFO_SIZE, TOTAL_HEIGHT)
        self.surface.fill(self.menu_color, rect)
        self.draw_text(TOTAL_WIDTH - INFO_SIZE + 0.5*LETTER_GAP_SIZE, 170, self.font_time, (0,0,0), f'Vidējais ')
        self.draw_text(TOTAL_WIDTH - INFO_SIZE + 0.5*LETTER_GAP_SIZE, 320, self.font_time, (0,0,0), f'Vidējais ')
        self.draw_time_human(average_time_human, 'spēlētāja patērētais laiks:')
        self.draw_time_ai(average_time_ai, 'datora patērētais laiks:')
        if self.menu_color == (51, 204, 51):
            self.draw_text(TOTAL_WIDTH - INFO_SIZE + LETTER_GAP_SIZE, 50, self.font, (0,0,0), 'Uzvara!')
        else:
            self.draw_text(TOTAL_WIDTH - INFO_SIZE + LETTER_GAP_SIZE, 50, self.font, (0,0,0), 'Zaudējums!')



    
