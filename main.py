import pygame
from jumpingHorses.constants import WIDTH, HEIGHT, SQUARE_SIZE, TOTAL_WIDTH, TOTAL_HEIGHT, LETTER_GAP_SIZE, MAIN_MENU_COLOR, starting_player, DEPTH
import jumpingHorses.constants as Constants
from jumpingHorses.game_master import GameMaster
from menu.main_menu import MainMenu
from menu.tutorial import Tutorial
from menu.game_secondary import GameSecondary
import menu.gameState as gameState
import computer.alphaBetaTree as ABTree
mainRunning = True
clock = pygame.time.Clock()
FPS = 30 #Frames Per Second
WINDOW = pygame.display.set_mode((TOTAL_WIDTH, TOTAL_HEIGHT)) #nodefinē spēles logu
pygame.display.set_caption('Jumping horses') #iedod spēles logam nosaukumu

playerOneTimes = []
playerTwoTimes = []

def main():
    pygame.init()
    while mainRunning:
        if gameState.currentState == gameState.State.mainMenu:
            main_menu()
        elif gameState.currentState == gameState.State.inGame:
            game()
        elif gameState.currentState == gameState.State.tutorial:
            tutorial()
        elif gameState.currentState == gameState.State.win:
            win()
        elif gameState.currentState == gameState.State.lost:
            win()


def game():
    #algroitma dziļums meklējams jumpingHorses.constants- DEPTH, nevajadzētu likt vairāk par 3
    run = True
    gameSurface = pygame.Surface((WIDTH, HEIGHT))
    WINDOW.fill(MAIN_MENU_COLOR)
    gameMaster = GameMaster(gameSurface)
    gameSecondary = GameSecondary(WINDOW)  
    oldState = gameState.currentState
    update_screen(gameMaster, gameSurface, oldState)  
    global playerOneTimes
    playerOneTimes.clear()
    global playerTwoTimes
    playerTwoTimes.clear()
    humanStartTime = pygame.time.get_ticks()
    #main game loop, kurā tiek loopotas visas iespējamās darbības
    while run:
        clock.tick(FPS)
        #cilvēka gājiens ar datora palīdzību
        #if gameMaster.turn == Constants.starting_player[1]:
        #    pygame.time.delay(300)
        #    turnStartTime = pygame.time.get_ticks()
        #    value, best_board = ABTree.alpha_beta_tree_maker(DEPTH, gameMaster.get_board(), True, Constants.starting_player[1], float('-inf'), float('inf'))
        #    gameMaster.ai_move(best_board)
        #    turnEndTime = pygame.time.get_ticks()
        #    timeTaken = (turnEndTime-turnStartTime)*0.001
        #    playerOneTimes.append(timeTaken)      
        #    gameSecondary.draw_time_human(timeTaken, 'Spēlētāja patērētais laiks:')
        #    update_screen(gameMaster, gameSurface)
        #    gameMaster.check_winner()
        #datora gājiens
        if run and gameMaster.turn == Constants.starting_player[2]:
            playerOneTimes.append((pygame.time.get_ticks() - humanStartTime)*0.001) #aizkomentē, ja cilvēka gājienu veic ai
            pygame.time.delay(300)
            turnStartTime = pygame.time.get_ticks()         
            value, best_board = ABTree.alpha_beta_tree_maker(DEPTH, gameMaster.get_board(), True, Constants.starting_player[2], float('-inf'), float('inf'))
            gameMaster.ai_move(best_board)
            turnEndTime = pygame.time.get_ticks()
            timeTaken = (turnEndTime-turnStartTime)*0.001
            playerTwoTimes.append(timeTaken)
            gameSecondary.draw_time_ai(timeTaken, 'Datora patērētais laiks:')
            update_screen(gameMaster, gameSurface)
            humanStartTime = pygame.time.get_ticks() #aizkomentē, ja cilvēka gājienu veic ai


        event_list = pygame.event.get()
        for event in event_list:
            #iziet no spēles(aizvēršanas X)
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                global mainRunning 
                mainRunning= False
                return

            #tiek piespiests kreisais peles klikšķis
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                gameMaster.select(pos)
        playerTime = (pygame.time.get_ticks() - humanStartTime)*0.001 #aizkomentē, ja cilvēka gājienu veic ai
        gameSecondary.draw_time_human(playerTime, 'Spēlētāja patērētais laiks:') #aizkomentē, ja cilvēka gājienu veic ai
        #atjauno ekrānu
        gameSecondary.update(event_list)
        update_screen(gameMaster, gameSurface)  
        gameMaster.check_winner()
        if oldState != gameState.currentState:
            run = False

def update_screen(gameMaster,gameSurface):
    gameMaster.update()
    WINDOW.blit(gameSurface, (LETTER_GAP_SIZE,0))
    pygame.display.update()


def main_menu():
    run = True
    mainMenu = MainMenu(WINDOW)
    #WINDOW.fill(MAIN_MENU_COLOR)
    oldState = gameState.currentState  
    while run:
        clock.tick(FPS)
        event_list = pygame.event.get()
        for event in event_list:
            #iziet no spēles(aizvēršanas X)
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                global mainRunning 
                mainRunning= False
                return

        mainMenu.update(event_list)
        if oldState != gameState.currentState:
            Constants.starting_player = mainMenu.get_starting_player()
            #print(Constants.starting_player)
            run = False



def tutorial():
    run = True
    tutorial = Tutorial(WINDOW)
    oldState = gameState.currentState  
    while run:
        clock.tick(FPS)
        event_list = pygame.event.get()
        for event in event_list:
            #iziet no spēles(aizvēršanas X)
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                global mainRunning 
                mainRunning= False
                return

        tutorial.update(event_list)
        if oldState != gameState.currentState:
            run = False

def win():
    run = True
    gameSecondary = GameSecondary(WINDOW)  
    oldState = gameState.currentState  
    gameSecondary.win(sum(playerOneTimes) / len(playerOneTimes), sum(playerTwoTimes) / len(playerTwoTimes))
    ##izprintē avg laiku, kas ir vajadzīgs gājienam
    #print("total play time first player: ", sum(playerOneTimes))
    #print("total moves for first player: ", len(playerOneTimes))
    #print("avg first player move time: ",sum(playerOneTimes) / len(playerOneTimes))
    #print("total play time second player: ", sum(playerTwoTimes))
    #print("total moves for second player: ", len(playerTwoTimes))
    #print("avg second player move time: ",sum(playerTwoTimes) / len(playerTwoTimes))
    while run:
        clock.tick(FPS)
        event_list = pygame.event.get()
        for event in event_list:
            #iziet no spēles(aizvēršanas X)
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                global mainRunning 
                mainRunning= False
                return

        gameSecondary.update(event_list)
        if oldState != gameState.currentState:
            run = False





main()
