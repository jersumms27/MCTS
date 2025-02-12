from state import State

class TicTacToe(State):
    def __init__(self, representation: list[list[int]]=[[0, 0, 0], [0, 0, 0], [0, 0, 0]], player: int=1):
        super().__init__(representation, player)
    
    def get_next_states(self) -> set[State]:
        moves: set[State] = set()

        for i in range(len(self.representation)):
            for j in range(len(self.representation[i])):
                if self.representation[i][j] == 0:
                    new_move: list[list[int]] = [row[:] for row in self.representation]
                    new_move[i][j] = self.player
                    moves.add(TicTacToe(new_move, 3 - self.player))

        return moves
    
    def take_random_action(self) -> State:
        return super().take_random_action()
    
    def calculate_value(self, player: int) -> float:
        winner: int = 0
        
        for i in range(3):
            if self.representation[i][0] == self.representation[i][1] == self.representation[i][2] != 0:
                winner = self.representation[i][0]
                break
            if self.representation[0][i] == self.representation[1][i] == self.representation[2][i] != 0:
                winner = self.representation[0][i]
                break
        if self.representation[0][0] == self.representation[1][1] == self.representation[2][2] != 0:
            winner = self.representation[0][0]
        elif self.representation[0][2] == self.representation[1][1] == self.representation[2][0] != 0:
            winner = self.representation[0][2]

        if winner == player:
            return 1.0
        return 0.0
    
    def is_terminal_state(self) -> bool:
        # Check rows, columns, and diagonals
        for i in range(3):
            if self.representation[i][0] == self.representation[i][1] == self.representation[i][2] != 0:
                return True
            if self.representation[0][i] == self.representation[1][i] == self.representation[2][i] != 0:
                return True
        if self.representation[0][0] == self.representation[1][1] == self.representation[2][2] != 0:
            return True
        if self.representation[0][2] == self.representation[1][1] == self.representation[2][0] != 0:
            return True
        
        # Check if the board is full
        return all(0 not in row for row in self.representation)

    def __str__(self) -> str:
        grid: list[list[str]] = []

        for row in self.representation:
            new_row: list[str] = []
            for val in row:
                if val == 0:
                    new_row.append(' ')
                elif val == 1:
                    new_row.append('X')
                elif val == 2:
                    new_row.append('O')
            
            grid.append(new_row)
        
        output: str = ''
        for i, row in enumerate(grid):
            output += ' ' + ' | '.join([symbol for symbol in row]) + ' \n'
            if i < len(grid) - 1:
                output += '-----------\n'
        
        return output
