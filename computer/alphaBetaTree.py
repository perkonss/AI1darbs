from jumpingHorses.constants import BLACK_PIECE, WHITE_PIECE, DEPTH
import jumpingHorses.constants as Constants
import random

MAX, MIN = float('inf'), float('-inf')
possibleMoves = [] #glabā pēdējos gājienus

def alpha_beta_tree_maker(depth, board, maximizingPlayer, color, alpha, beta):
    oppositeColor = opposite_color(color)
    if depth == 0 or board.winner() != None:
        if color == Constants.starting_player[2] and not maximizingPlayer:
            #print("human max")
            value = board.evaluationHumanMax() + random.randint(0, 4)
            return value, board

        elif color == Constants.starting_player[1] and not maximizingPlayer:
            #print("ai max")
            value = board.evaluationAIMax() + random.randint(0, 4)
            return value, board

        elif color == Constants.starting_player[2] and  maximizingPlayer:
            #print("human min")
            value = board.evaluationHumanMin() + random.randint(0, 4)
            return value, board

        elif color == Constants.starting_player[1] and  maximizingPlayer:
            #print("ai min")
            value = board.evaluationAIMin() + random.randint(0, 4)
            return value, board
    if maximizingPlayer:
        best = MIN
        best_board = None
        for newBoard in board.get_all_moves(board, color):
            value, generatedBoard = alpha_beta_tree_maker(depth-1, newBoard, False, oppositeColor, alpha, beta)
            #if depth == DEPTH: print(value, depth, generatedBoard.print_board()) #izvada augstākā līmeņa radiniekus 
            best = max(best, value)
            alpha = max(alpha, best)
            if value == best:
                best_board = newBoard   
            #pruning
            if beta <= best:
                break
        return best, best_board
    else:
        best = MAX
        best_board = None
        for newBoard in board.get_all_moves(board, color):
            value, generatedBoard = alpha_beta_tree_maker(depth-1, newBoard, True, oppositeColor, alpha, beta)
            #if depth == DEPTH: print(value, depth, generatedBoard.print_board())
            best = min(best, value)
            beta = min(beta, best)
            if value == best:
                best_board = newBoard
            if best <= alpha:
                break
        return best, best_board

def opposite_color(color):
    if color == WHITE_PIECE:
        return BLACK_PIECE
    else: 
        return WHITE_PIECE
