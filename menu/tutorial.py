import pygame
from jumpingHorses.constants import MAIN_MENU_COLOR, BUTTON_COLOR, TOTAL_WIDTH, TOTAL_HEIGHT, FONT_SIZE
from .radio_buttons import RadioButton
from .button import Button
import menu.gameState as gameState

class Tutorial:
    def __init__(self, surface):
        self.surface = surface
        self.font = pygame.font.SysFont(None, FONT_SIZE)
        width = TOTAL_WIDTH//6
        self.setup()
        self.all_buttons =[Button(20, 20, width, 50, self.font, "Atpakaļ"),]

    def setup(self):
        self.surface.fill(MAIN_MENU_COLOR)     
        self.draw_text(self.surface, TOTAL_WIDTH//2 - 100, 50, self.font, (0,0,0), 'Pamācība')
       #self.draw_text(self.surface, 50, 150, self.font, (0,0,0), 'Spēles mērķis ir aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        self.draw_text(self.surface, 50, 150, self.font, (0,0,0), '     Spēles mērķis ir pārnest visus savus kauliņus uz pretējo')
        self.draw_text(self.surface, 50, 190, self.font, (0,0,0), 'spēles stūri. Sava gājiena laikā Tu vari pārvietot kādu')
        self.draw_text(self.surface, 50, 230, self.font, (0,0,0), 'no saviem kauliņiem par 1 lauciņu vai nu horizontāli, vai ')
        self.draw_text(self.surface, 50, 270, self.font, (0,0,0), 'vertikāli, vai arī vari lekt ar savu kauliņu pāri citam')
        self.draw_text(self.surface, 50, 310, self.font, (0,0,0), 'kauliņam, vienalga vai savam vai pretinieka. Šādu lēcienu')
        self.draw_text(self.surface, 50, 350, self.font, (0,0,0), 'var veikt pāri neierobežotam skaitam kauliņu, kamēr starp ')
        self.draw_text(self.surface, 50, 390, self.font, (0,0,0), 'kauliņiem ir 1 brīvs lauciņš.')
    def update(self, event_list):
        for button in self.all_buttons:
            button.update(event_list)
            button.draw(self.surface)
            if button.clicked == True:
                if button.text == "Atpakaļ":
                    gameState.currentState = gameState.State.mainMenu
            pygame.display.update()


    def draw_text(self, surface, x, y, font, color, text):
        text = font.render(text, 1, color)
        text_place = text.get_rect()
        text_place.topleft = (x,y)
        self.surface.blit(text, text_place)

