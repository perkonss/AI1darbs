from enum import Enum
class State(Enum):
    mainMenu = 'mainMenu'
    inGame = 'inGame'
    tutorial = 'tutorial'
    win = 'win'
    lost = 'lost'

currentState = State.mainMenu
