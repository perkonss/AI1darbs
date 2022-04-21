#šeit tiek definētas visas konstantes, lai vēlāk būtu vieglāk nomainīt lietas
import pygame

#dziļums
DEPTH = 3

#spēles loga izmēri
HEIGHT = 800
WIDTH =  800
LETTER_GAP_SIZE = 40
INFO_SIZE = 300
TOTAL_WIDTH = WIDTH + LETTER_GAP_SIZE + INFO_SIZE
TOTAL_HEIGHT = HEIGHT + LETTER_GAP_SIZE
PLAYING_WIDTH = WIDTH + LETTER_GAP_SIZE
PLAYING_HEIGHT = HEIGHT
#cik daudz kolonnu un rindu būs spēlē
ROWS = 8
COLS = 8
#cik liela būs viena rūtiņa; rūtiņu krāsa
SQUARE_SIZE = HEIGHT //ROWS
BLACK_SQUARE = (24, 10, 10)#(51,102,0)
WHITE_SQUARE = (175,187,242)#(204, 255, 153)

#nodefinē kādas būs spēlētāju krāsas; cik liela atstarpe būs starp kauliņu un rūtiņas malu; kauliņa kontūras izmēru un krāsu
WHITE_PIECE = (255,255,255)
BLACK_PIECE = (0,0,0)
GAP = 18
OUTLINE_SIZE = 3
OUTLINE_COLOR = (127,127,127)
#gājiena izvēles krāsa un lielums
MOVE_COLOR = (51, 153, 255)
MOVE_RADIUS = 15
#main menu lietas
MAIN_MENU_COLOR = (94,43,255)#(255, 204, 102)
BUTTON_COLOR = (192,76,253)#(255, 153, 204)
SELECTION_COLOR = (192,76,253)#(255, 153, 204)
SELECTED_COLOR = (252,109,171)#(51, 204, 51)
TEXT_COLOR = (243,250,225)
FONT_SIZE = 50

#sākuma spēlētājs
starting_player = ("Random", (122,122,122), (122,122,122)) #(lietotaja nosaukums, kurš sāk spēli; cilvēka krāsa; datora krāsa)
