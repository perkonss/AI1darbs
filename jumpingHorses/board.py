import pygame
from copy import deepcopy
import jumpingHorses.constants as Constants
from .constants import ROWS, COLS, BLACK_SQUARE, WHITE_SQUARE, SQUARE_SIZE, WHITE_PIECE, BLACK_PIECE
from .piece import Piece
import menu.gameState as GameState

#Laukuma klase
class Board:
	#inicializēšana
	def __init__(self):
		#self.startingPlayer = starting_player #(vārds, human krāsa, ai krāsa)
		self.human_color = Constants.starting_player[1]
		print("human color:", self.human_color)
		self.AI_color = Constants.starting_player[2]
		print("ai color:", self.AI_color)
		self.board = [] #laukuma stāvoklis [[WHITE,BLACK,0,0,WHITE] [][]], sākumā tukšs
		self.create_board() #spēles sākumā izveido laukumu
	#uzzīmē visas rūtiņas  
	def draw_squares(self, surface):
		surface.fill(BLACK_SQUARE)
		for row in range(ROWS):
			for col in range(row % 2, COLS, 2): #fancy matemātika- range(sāk ar 1. vai 2. kolonnu; līdz kādam skaitlim inkrimentē, ar kādu soli)
				pygame.draw.rect(surface, WHITE_SQUARE, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
		#uzzīmē kvadrātu apkārt pils lauciņiem (9 sākuma lauciņi)
		pygame.draw.rect(surface, self.human_color, (0, COLS*SQUARE_SIZE-3*SQUARE_SIZE, 3*SQUARE_SIZE, 3*SQUARE_SIZE), 5)
		pygame.draw.rect(surface, self.AI_color, (ROWS*SQUARE_SIZE-3*SQUARE_SIZE, 0, 3*SQUARE_SIZE, 3*SQUARE_SIZE), 5)

	#spēles sākumā izvieto spēles kauliņus
	def create_board(self):
		for row in range(ROWS):
			self.board.append([])
			for col in range (COLS):
				if col > 4:
					if row < 3:
						self.board[row].append(Piece(row, col, self.AI_color))
					else: self.board[row].append(0)
				elif col < 3:
					if row > 4:
						self.board[row].append(Piece(row, col, self.human_color))
					else: self.board[row].append(0)
				else:
					self.board[row].append(0)
	#zīmē laukumu ar kauliņiem
	def draw(self,surface):
		self.draw_squares(surface)
		for row in range(ROWS):
			for col in range(COLS):
				piece = self.board[row][col]
				if piece != 0:
					piece.draw(surface)
	#pārvieto kauliņus
	def move(self, piece, row, col):
		#swapo izvēlēto kauliņu ar kauliņu, kas ir tā vietā(visticamākais 0)
		self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
		piece.move(row,col)
		self.winner()
	#atgriež visus kauliņus, vēlamajā krāsā
	def get_all_pieces(self, color):
			pieces = []
			for row in self.board:
				for piece in row:
					if piece != 0 and piece.color == color:
						pieces.append(piece)
			return pieces
	#atgriež visus kauliņus, visās krāsās
	def get_all_pieces_all_colors(self):
			pieces = []
			for row in self.board:
				for piece in row:
					if piece != 0:
						pieces.append(piece)
			return pieces
	#atgriež visus gājienus, kas spēlētājam ir iespējami
	def get_all_moves(self, board, color):
		moves=[]
		for piece in board.get_all_pieces(color):
			for move in board.get_valid_moves(piece):
				temp_board = deepcopy(board)
				temp_piece = temp_board.get_piece(piece.row,piece.col)
				new_board = temp_board.simulate_move(temp_board, temp_piece, move[0], move[1])
				moves.append(new_board)
		return moves

	#simulē gājienu, actualy nemainot patreizēju spēles laukumu
	def simulate_move(self, board, piece, row, col):       
		board.move(piece, row, col)
		return board

	#atgriež kauliņu, kas atrodas konkrētajā pozīcijā
	def get_piece(self, row, col):
		return self.board[row][col]
	#funkcija uz āru, lai dabūtu legālos gājienus
	def get_valid_moves(self, piece):
		moves = {}
		moves.update(self._get_valid_moves(piece.row, piece.col,[], 1))
		moves.update(self._get_valid_moves(piece.row, piece.col,[], 2))
		return moves
	#pārbauda, vai gājiens ir legāls
	def can_jump_from_to(self, old_row, old_col, new_row, new_col, step_size):
			#pārbauda, vai netiek iets ārpus laukuma
			if not (0 <= new_row < ROWS and 0 <= new_col < COLS):
				return False
			#pārbauda, vai netiek lekts pa diognāli
			if (abs(old_row - new_row) + abs(old_col - new_col) > step_size):
				return False
			new_loc = self.get_piece(new_row, new_col)
			#pārbauda, vai pozīcija nav aizņemta
			if new_loc != 0:
				return False
			#pārbauda, vai lēkšanas gadījumā, pa vidu ir kauliņš
			if step_size == 2:
				middle_row = (old_row + new_row) // 2
				middle_col = (old_col + new_col) // 2
				middle_piece = self.get_piece(middle_row, middle_col)
				if middle_piece == 0:
					return False		
			return True
	#atgriež visus legālos gājienus
	def _get_valid_moves(self, row, col, jumped_pieces, step_size):
		up, down, left, right = [x + y * step_size for x in [row, col] for y in [-1, +1]]

		moves = {}#datu tips- dictionary, lai saglabātu gājienu un jau pārlēktos kauliņus, otherwise bezgalīgā rekursija rastos

		for new_col in [col, left, right]:
			for new_row in [row, up, down]:
				if not self.can_jump_from_to(row, col, new_row, new_col, step_size): #ja nevar veikt gājienu, tad tālāk nemaz neskatās
					continue
				
				if step_size == 1:
					moves[(new_row, new_col)] = []
				else:
					middle_row = (new_row + row) // 2
					middle_col = (new_col + col) // 2
					if (middle_row, middle_col) in jumped_pieces:
						continue
					new_jumped_pieces = jumped_pieces.copy()
					new_jumped_pieces.append((middle_row, middle_col))
					moves[(new_row, new_col)] = new_jumped_pieces
					moves.update(self._get_valid_moves(new_row, new_col, new_jumped_pieces, step_size))
		
		return moves
	#atgriež uzvarētāja krāsu (no tās var noteikt uzvarētāja spēlētāju)
	def winner(self):
		if self.check_human_win():			
			return self.human_color
		if self.check_AI_win():
			return self.AI_color
		return None
	#pārbauda cilvēka uzvaras nosacījumus
	def check_human_win(self):
		for row in range(ROWS):
			for col in range (COLS):
				if col > 4:
					if row < 3:
						if self.get_piece(row, col) == 0:
							return False
						if self.get_piece(row, col).color != self.human_color:
							return False
		return True
	#pārbauda datora uzvaras nosacījumus
	def check_AI_win(self):
		for row in range(ROWS):
			for col in range (COLS):
				if col < 3:
					if row > 4:
						if self.get_piece(row, col) == 0:
							return False
						if self.get_piece(row, col).color != self.AI_color:
							return False
		return True

	positionsForAI = [[0  ,0  ,0  ,5  ,15 ,11 ,6 ,-3  ],
					  [0  ,0  ,10 ,20 ,30 ,12 ,11 ,6 ],
					  [10 ,20 ,30 ,40 ,31 ,13 ,12 ,11 ],
					  [40 ,60 ,70 ,65 ,45 ,31 ,30 ,15 ],
					  [70 ,80 ,85 ,75 ,65 ,40 ,20 ,5  ],
					  [105,100,100,85 ,70 ,30 ,10 ,0  ],
					  [106,105,100,80 ,60 ,20 ,0  ,0  ],
					  [111,106,105,70 ,40 ,10 ,0  ,0  ]]

	positionsForHuman=[[0  ,0  ,10	,40	,70	,105,106,111],
					   [0  ,0  ,20 ,60 ,80 ,100,105,106],
					   [0  ,10 ,30 ,70 ,85 ,100,100,105],
					   [5  ,20 ,40 ,65 ,75 ,85 ,80 ,70 ],
					   [15 ,30 ,31 ,45 ,65 ,70 ,60 ,40 ],
					   [11 ,12 ,13 ,31 ,40 ,30 ,20 ,10 ],
					   [6  ,11 ,12 ,30 ,20 ,10 ,0  ,0  ],
					   [-3  ,6 ,11 ,15 ,5  ,0  ,0,  0  ]]

	#funkcija datoram, spēles koka izveidei- maksimizēšana
	def evaluationAIMax(self):
		value = 0
		for piece in self.get_all_pieces_all_colors():
			if piece.color == self.AI_color:
				value += 2*self.positionsForAI[piece.row][piece.col]
			else:
				value -= self.positionsForHuman[piece.row][piece.col]
		return value
	#funkcija datoram, spēles koka izveidei- minimizēšana
	def evaluationAIMin(self):
		value = 0
		for piece in self.get_all_pieces_all_colors():
			if piece.color == self.AI_color:
				value -= self.positionsForAI[piece.row][piece.col]
			else:
				value += 2*self.positionsForHuman[piece.row][piece.col]
		return value
	#funkcija spēlētājam, spēles koka izveidei- maksimizēšana
	def evaluationHumanMax(self):
		value = 0
		for piece in self.get_all_pieces_all_colors():
			if piece.color == self.human_color:
				value += 2*self.positionsForHuman[piece.row][piece.col]
			else:
				value -= self.positionsForAI[piece.row][piece.col]
		return value
	#funkcija spēlētājam, spēles koka izveidei- minimizēšana
	def evaluationHumanMin(self):
		value = 0
		for piece in self.get_all_pieces_all_colors():
			if piece.color == self.human_color:
				value -= self.positionsForHuman[piece.row][piece.col]
			else:
				value += 2*self.positionsForAI[piece.row][piece.col]
		return value


	#funkcija, kas izvada uz ekrāna laukuma stāvokli
	def print_board(self):
		for i in range(Constants.ROWS):
			for j in range(Constants.COLS):
				#if self.get_piece(row, col).color != self.AI_color:
				if self.board[i][j] == 0:
					print("0|", end='')
				elif self.get_piece(i,j).color == BLACK_PIECE:
					print("B|", end='')
				elif self.get_piece(i,j).color == WHITE_PIECE:
					print("W|", end='')
			print()
