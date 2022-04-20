import pygame
from jumpingHorses.constants import BUTTON_COLOR, SELECTED_COLOR

class Button():
    def __init__(self, x, y, width, height, font, text):
        self.x = x
        self.y = y
        self.text = text
        text_surf = font.render(text, True, (0, 0, 0))
        self.button_image = pygame.Surface((width, height))
        self.button_image.fill(BUTTON_COLOR)
        self.button_image.blit(text_surf, text_surf.get_rect(center = (width // 2, height // 2)))
        self.hover_image = pygame.Surface((width, height))
        self.hover_image.fill(BUTTON_COLOR)
        self.hover_image.blit(text_surf, text_surf.get_rect(center = (width // 2, height // 2)))
        pygame.draw.rect(self.hover_image, SELECTED_COLOR, self.hover_image.get_rect(), 3)
        self.image = self.button_image
        self.rect = pygame.Rect(x, y, width, height)
        self.clicked = False

    def update(self, event_list):
        self.clicked = False
        hover = self.rect.collidepoint(pygame.mouse.get_pos())
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if hover and event.button == 1:
                    self.clicked = True
        
        self.image = self.button_image
        if hover:
            self.image = self.hover_image

    def draw(self, surface):
        surface.blit(self.image, self.image.get_rect(topleft = (self.x,self.y)))