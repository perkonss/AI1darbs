import pygame
import random
from jumpingHorses.constants import MAIN_MENU_COLOR, BUTTON_COLOR, TOTAL_WIDTH, TOTAL_HEIGHT, FONT_SIZE, WHITE_PIECE, BLACK_PIECE
from .radio_buttons import RadioButton
from .button import Button
import menu.gameState as GameState
class MainMenu:
    def __init__(self, surface):
        self.surface = surface
        self.font = pygame.font.SysFont(None, FONT_SIZE)
        self.radioButtonGroup = self.setup_radio_buttons()
        width = TOTAL_WIDTH//4
        self.setup()
        self.all_buttons =[          
            Button(TOTAL_WIDTH//2 - width//2, 400, width, 100, self.font, "Sākt"),
            Button(TOTAL_WIDTH//2 - width//2, 600, width, 100, self.font, "Pamācība")]

    def setup(self):
        self.surface.fill(MAIN_MENU_COLOR)     
        self.draw_text(self.surface, TOTAL_WIDTH//2 - 100, 50, self.font, (0,0,0), 'Spēli sāk: ')

    def update(self, event_list):
        self.radioButtonGroup.update(event_list)
        self.radioButtonGroup.draw(self.surface)
        for button in self.all_buttons:
            button.update(event_list)
            button.draw(self.surface)
            if button.clicked == True:
                if button.text == "Sākt":
                    GameState.currentState = GameState.State.inGame
                if button.text == "Pamācība":
                    GameState.currentState = GameState.State.tutorial
        pygame.display.update()

    def setup_radio_buttons(self):   
        radioButtons=[
            RadioButton(TOTAL_WIDTH//8 - 50, 150, TOTAL_WIDTH//5, 50, self.font, "Nejauši"),
            RadioButton(TOTAL_WIDTH//3 + 70, 150, TOTAL_WIDTH//5, 50, self.font, "Cilvēks"),
            RadioButton(TOTAL_WIDTH//1.5 + 50, 150, TOTAL_WIDTH//5, 50, self.font, "Dators")
        ]
        for rb in radioButtons:
            rb.setRadioButtons(radioButtons)
        radioButtons[0].clicked = True
        radioButtonGroup = pygame.sprite.Group(radioButtons)
        return radioButtonGroup

    def draw_text(self, surface, x, y, font, color, text):
        text = font.render(text, 1, color)
        text_place = text.get_rect()
        text_place.topleft = (x,y)
        self.surface.blit(text, text_place)
    #atgriež katra spēlētāju krāsu, atkarībā no tā, ko izvēlas lietotājs
    def get_starting_player(self):
        player = self.get_selected_turn()
        randomValue = 'y'
        if player == "Nejauši":
            randomValue = random.choice(['a','b'])
        if player == "Cilvēks" or randomValue == 'a':
            vards = "Cilvēks"
            human_color = WHITE_PIECE
            AI_color = BLACK_PIECE
        elif player == "Dators" or randomValue == 'b':
            vards = "Dators"
            human_color = BLACK_PIECE
            AI_color = WHITE_PIECE
        playerInfo = (vards, human_color, AI_color)
        return playerInfo

    def get_selected_turn(self):
        for button in self.radioButtonGroup:
            if button.clicked ==True:
                return button.text

        
