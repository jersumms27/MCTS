from abc import ABC, abstractmethod
from typing import Type, Any

class Piece(ABC):
    '''
    A Chess Piece.

    Attributes:
        player (int): Which player this piece belongs to.
        has_moved (bool): Whether or not this piece has moved yet.

    Methods:
        get_potential_boards: Return set of all possible boards from moving this piece.
        get_directional_moves: Get all possible boards given directions and number of spaces.
        get_board_from_move: Get the board that results from a specific move.
        is_out_of_bounds: Determine whether the piece is out of bounds given position.
    '''

    def __init__(self, player: int) -> None:
        '''
        Create a piece.

        Parameters:
            player (int): Which player this piece belongs to.
        '''

        self.player: int = player
        self.has_moved: bool = False
    
    @abstractmethod
    def get_potential_boards(self, board: list[list['Piece | None']], position: tuple[int, int]) -> list[list[list['Piece | None']]]:
        '''
        Get all possible board states from moving this piece (not taking into account validity).

        Parameters:
            board (list[list[Piece | None]]): Current board state.
            position (tuple[int, int]): Current position of this piece.
        
        Returns:
            list[list[list[Piece | None]]]: Set of all possible board states from moving this piece.
        '''

        pass

    def get_directional_moves(self, board: list[list['Piece | None']], position: tuple[int, int], directions: set[tuple[int, int]], spaces: int) -> list[list[list['Piece | None']]]:
        '''
        Get all possible board states from moving this piece `spaces` number of spaces in the given `directions`.

        Parameters:
            board (list[list[Piece | None]]): Current board state.
            position (tuple[int, int]): Current position of this piece.
            directions (set[tuple[int, int]]): Which directions to move piece.
            spaces (int): How many squares in each direction to move.
        
        Returns:
            list[list[list[Piece | None]]]: Set of all possible board states from moving this piece in the given `directions`.
        '''

        moves: list[list[list[Piece | None]]] = []
        row: int = position[0]
        col: int = position[1]

        for dir in directions:
            end: bool = False
            for space in range(1, spaces + 1):
                if end:
                    break
                new_row: int = row + dir[0] * space
                new_col: int = col + dir[1] * space
            
                if self.is_out_of_bounds(new_row, new_col):
                    break
                piece: Piece | None = board[new_row][new_col]
                if not self.is_out_of_bounds(new_row, new_col):
                    if piece is None:
                        moves.append(self.get_board_from_move(board, position, (new_row, new_col)))
                    elif piece.player != self.player:
                        moves.append(self.get_board_from_move(board, position, (new_row, new_col)))
                        end = True
                    elif piece.player == self.player:
                        end = True

        return moves
    
    def get_board_from_move(self, board: list[list['Piece | None']], old_pos: tuple[int, int], new_pos: tuple[int, int]) -> list[list['Piece | None']]:
        '''
        Make a certain move with this piece.

        Parameters:
            board (list[list[Piece | None]]): Current state of the board.
            old_pos (tuple[int, int]): Current position of piece.
            new_pos (tuple[int, int]): New position of piece.
        
        Returns:
            list[list[Piece | None]]: Board after move is completed.
        '''

        new_board: list[list[Piece | None]] = [row[:] for row in board]
        piece: Piece | None = board[old_pos[0]][old_pos[1]]

        if piece is not None:
            piece.has_moved = True
        new_board[old_pos[0]][old_pos[1]] = None
        new_board[new_pos[0]][new_pos[1]] = piece

        return new_board
    
    
    def is_out_of_bounds(self, row: int, col: int) -> bool:
        '''
        Determine whether a given position is out of bounds.

        Parameters:
            row (int): Row position of piece.
            col (int): Column position of piece.
        
        Returns:
            bool: Whether this piece is out of bounds or not given its position.
        '''
        
        return not (0 <= row <= 7 and 0 <= col <= 7)
    
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Piece):
            return False
        return type(self) == type(other) and self.player == other.player# and self.has_moved == other.has_moved
    
    def __hash__(self) -> int:
        return hash((type(self), self.player, self.has_moved))
    
    def __str__(self) -> str:
        symbols: dict[Type[Piece], str] = {
            Pawn: 'p',
            Knight: 'n',
            Bishop: 'b',
            Rook: 'r',
            Queen: 'q',
            King: 'k'
        }
        
        letter: str = symbols.get(type(self), '?')
        if self.player == 1:
            return letter.upper()
        return letter

class Knight(Piece):
    def __init__(self, player: int) -> None:
        super().__init__(player)

    def get_potential_boards(self, board: list[list[Piece | None]], position: tuple[int, int]) -> list[list[list[Piece | None]]]:
        return self.get_directional_moves(board, position, set([(2, 1), (2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]), 1)

class Rook(Piece):
    def __init__(self, player: int) -> None:
        super().__init__(player)
    
    def get_potential_boards(self, board: list[list[Piece | None]], position: tuple[int, int]) -> list[list[list[Piece | None]]]:
        return self.get_directional_moves(board, position, set([(0, 1), (0, -1), (-1, 0), (1, 0)]), 8)

class Bishop(Piece):
    def __init__(self, player: int) -> None:
        super().__init__(player)
    
    def get_potential_boards(self, board: list[list[Piece | None]], position: tuple[int, int]) -> list[list[list[Piece | None]]]:
        return self.get_directional_moves(board, position, set([(1, 1), (1, -1), (-1, 1), (-1, -1)]), 8)

class Queen(Piece):
    def __init__(self, player: int) -> None:
        super().__init__(player)
    
    def get_potential_boards(self, board: list[list[Piece | None]], position: tuple[int, int]) -> list[list[list[Piece | None]]]:
        return self.get_directional_moves(board, position, set([(0, 1), (0, -1), (-1, 0), (1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]), 8)

class King(Piece):
    def __init__(self, player: int) -> None:
        super().__init__(player)
    
    def get_potential_boards(self, board: list[list[Piece | None]], position: tuple[int, int]) -> list[list[list[Piece | None]]]:
        moves: list[list[list[Piece | None]]] = self.get_directional_moves(board, position, set([(0, 1), (0, -1), (-1, 0), (1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]), 1)
        king: Piece | None = board[position[0]][position[1]]

        if king is not None and not self.has_moved:
            first_row: int
            if self.player == 1:
                first_row = 7
            else:
                first_row = 0
            
            left_pos: tuple[int, int] = (first_row, 0)
            right_pos: tuple[int, int] = (first_row, 7)

            left_piece: Piece | None = board[left_pos[0]][left_pos[1]]
            right_piece: Piece | None = board[right_pos[0]][right_pos[1]]

            if left_piece is not None and not left_piece.has_moved:
                new_board: list[list[Piece | None]] = [row[:] for row in board]
                new_board[left_pos[0]][left_pos[1]] = None
                new_board[right_pos[0]][right_pos[1]] = None

                new_board[first_row][1] = king
                new_board[first_row][2] = left_piece
                king.has_moved = True
                left_piece.has_moved = True
                moves.append(new_board)
            
            if right_piece is not None and not right_piece.has_moved:
                new_board = [row[:] for row in board]
                new_board[left_pos[0]][left_pos[1]] = None
                new_board[right_pos[0]][right_pos[1]] = None

                new_board[first_row][6] = king
                new_board[first_row][5] = right_piece
                king.has_moved = True
                right_piece.has_moved = True
                moves.append(new_board)
        
        return moves

class Pawn(Piece):
    def __init__(self, player: int) -> None:
        super().__init__(player)
    def get_potential_boards(self, board: list[list[Piece | None]], position: tuple[int, int]) -> list[list[list[Piece | None]]]:
        moves: list[list[list[Piece | None]]] = []
        forward: int
        start_row: int
        promote_row: int

        if self.player == 1:
            forward = -1
            start_row = 6
            promote_row = 0
        else:
            forward = 1
            start_row = 1
            promote_row = 7
        
        new_pos: tuple[int, int] = (position[0] + forward, position[1])
        if not self.is_out_of_bounds(new_pos[0], new_pos[1]) and board[new_pos[0]][new_pos[1]] is None:
            moves.append(self.get_board_from_move(board, position, new_pos))
        
        if position[0] == start_row:
            new_pos = (position[0] + forward * 2, position[1])
            if not self.is_out_of_bounds(new_pos[0], new_pos[1]):
                if board[new_pos[0]][new_pos[1]] is None:
                    moves.append(self.get_board_from_move(board, position, new_pos))
        
        for col_change in [-1, 1]:
            new_pos = (position[0] + forward, position[1] + col_change)
            if not self.is_out_of_bounds(new_pos[0], new_pos[1]):
                piece: Piece | None = board[new_pos[0]][new_pos[1]]
                if piece is not None and piece.player != self.player:
                    moves.append(self.get_board_from_move(board, position, new_pos))
        
        return moves