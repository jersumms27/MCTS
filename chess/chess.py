from state import State
from chess.piece import Piece, King, Queen, Rook, Knight, Bishop, Pawn
from typing import Type

class Chess(State):
    '''
    A representation of a Chess game state.

    Attributes:
        representation (list[list[Piece | None]]): The representation of the game state.
        player (int): Which player's turn it currently is at this state.
        is_terminal (bool): Whether this state is a terminal state or not.
    
    Methods:
        get_next_states: Get all possible next states.
        calculate_value: Calculate value of this game state (how good the state is relative to whose turn it is).
        is_terminal_state: Determine whether this is a terminal state or not.
        is_in_check: Determine whether `player` is in check.
        is_in_checkmate: Determine whether `player` is in checkmate.
        is_in_stalemate: Determine whether the game is in stalemate.
    '''

    default_board: list[list[Piece | None]] = [
        [Rook(2), Knight(2), Bishop(2), King(2), Queen(2), Bishop(2), Knight(2), Rook(2)],
        [Pawn(2) for _ in range(8)],
        [None for _ in range(8)],
        [None for _ in range(8)],
        [None for _ in range(8)],
        [None for _ in range(8)],
        [Pawn(1) for _ in range(8)],
        [Rook(1), Knight(1), Bishop(1), King(1), Queen(1), Bishop(1), Knight(1), Rook(1)]
    ]

    def __init__(self, representation: list[list[Piece | None]]=default_board, player: int=1) -> None:
        '''
        Create a Chess state.

        Parameters:
            representation (list[list[Piece | None]]): A 2D array representing the board.
            player (int): Whose turn it is at this state.
        '''

        super().__init__(representation, player)
    
    def get_next_states(self) -> set[State]:
        '''
        Get states from taking all possible available actions.

        Returns:
            set[State]: All possible states.
        '''

        return set([Chess(board, 3 - self.player) for board in self.get_next_boards()])
    
    def get_next_boards(self) -> list[list[list[Piece | None]]]:
        boards: list[list[list[Piece | None]]] = []
        for row in range(len(self.representation)):
            for col in range(len(self.representation[row])):
                piece: Piece | None = self.representation[row][col]
                if piece is not None and piece.player == self.player:
                    potential_boards: list[list[list[Piece | None]]] = piece.get_potential_boards(self.representation, (row, col))

                    for board in potential_boards:
                        if not self.is_in_check(board, self.player):
                            boards.append(board)

        return boards
    
    def calculate_value(self, player: int) -> float:
        '''
        Calculate the value of the game at this current state.

        Parameters:
            player (int): Whose turn it is in the actual game.
        
        Returns:
            float: The value of this game state (will always be between -1 and 1).
        '''

        if self.is_in_checkmate(self.representation, player):
            return -1.0
        if self.is_in_checkmate(self.representation, 3 - player):
            return 1.0
        if self.is_in_stalemate(self.representation, player):
            return 0.0
        
        piece_vals: dict[Type[Piece], float] = {
            Pawn: 1.0,
            Knight: 3.0,
            Bishop: 3.0,
            Rook: 5.0,
            Queen: 8.0
        }

        value: float = 0.0
        for row in self.representation:
            for piece in row:
                if piece is not None and not isinstance(piece, King):
                    if piece.player == player:
                        value += piece_vals[type(piece)]
                    else:
                        value -= piece_vals[type(piece)]

        return value / 38.0
    
    def is_terminal_state(self) -> bool:
        '''
        Determine whether the game state is a terminal state.

        Returns:
            bool: Whether the game state is a terminal state or not.
        '''

        return self.is_in_stalemate(self.representation, 1) or self.is_in_stalemate(self.representation, 2) or self.is_in_checkmate(self.representation, 1) or self.is_in_checkmate(self.representation,2)
    
    def is_in_check(self, board: list[list[Piece | None]], player: int) -> bool:
        '''
        Determine whether `player` in the game state represented by `board` is in check.

        Parameters:
            board (list[list[Piece | None]]): Representation of Chess state.
            player (int): The player in question.
        
        Returns:
            bool: Whether `player` is in check or not.
        '''

        for row in range(len(board)):
            for col in range(len(board[row])):
                piece: Piece | None = board[row][col]

                if piece is not None and piece.player != player:
                    for new_board in piece.get_potential_boards(board, (row, col)):
                        new_pieces: set[Piece] = set()
                        for new_row in new_board:
                            new_pieces = new_pieces.union(set([new_piece for new_piece in new_row if new_piece is not None]))
                        
                        king: King | None = next((piece for piece in new_pieces if isinstance(piece, King) and piece.player == player), None)
                        if king is None:
                            return True
        
        return False
    
    def is_in_checkmate(self, board: list[list[Piece | None]], player: int) -> bool:
        '''
        Determine whether `player` in the game state represented by `board` is in checkmate.

        Parameters:
            board (list[list[Piece | None]]): Representation of Chess state.
            player (int): The player in question.
        
        Returns:
            bool: Whether `player` is in checkmate or not.
        '''

        if not self.is_in_check(board, player):
            return False

        boards: list[list[list[Piece | None]]] = self.get_next_boards()
        for new_board in boards:
            if not self.is_in_check(new_board, player):
                return False

        return True
    
    def is_in_stalemate(self, board: list[list[Piece | None]], player: int) -> bool:
        '''
        Determine whether `player` in the game state represented by `board` is in stalemate.

        Parameters:
            board (list[list[Piece | None]]): Representation of Chess state.
            player (int): The player in question.
        
        Returns:
            bool: Whether `player` is in stalemate or not.
        '''

        boards: list[list[list[Piece | None]]] = self.get_next_boards()
        for new_board in boards:
            if not self.is_in_check(new_board, player):
                return False

        return True
    
    def __str__(self) -> str:
        output: str = ''
        for row in range(len(self.representation)):
            for col in range(len(self.representation[row])):
                piece: Piece | None = self.representation[row][col]
                symbol: str = ' '

                if piece is not None:
                    symbol = str(piece)

                output += ' ' + symbol + ' '
                if col < len(self.representation[row]) - 1:
                    output += '|'
            
            if row < len(self.representation) - 1:
                output += '\n-------------------------------\n'

        return output