from abc import ABC, abstractmethod
import random
from typing import TypeVar, Generic

T = TypeVar('T')

class State(ABC, Generic[T]):
    '''
    A representation of a game state.

    Attributes:
        representation (T): Some representation of the game state (e.g. str, list).
        player (int): Which player's turn it currently is at this state of the game.
        is_terminal (bool): Whether this state is a terminal state or not.
    
    Methods:
        get_next_states: Get all states which are possible to reach within 1 action.
        take_random_action: Get the state from taking a random action.
        calculate_value: Calculate the value of the game state.
        is_terminal: Determine whether this state is a terminal state.
    '''

    def __init__(self, representation: T, player: int) -> None:
        '''
        Create a new state.

        Parameters:
            representation (T): Some representation of the game state (e.g. str, list).
            player (int): Which player's turn it currently is at this state of the game.
        '''

        self.representation: T = representation
        self.player: int = player
        self.is_terminal: bool = self.is_terminal_state()

    @abstractmethod
    def get_next_states(self) -> set['State']:
        '''
        Get states from taking all possible available actions.

        Returns:
            set[State]: All possible states.
        '''

        pass

    def take_random_action(self) -> 'State':
        '''
        Get one state by taking a random available action.

        Returns:
            State: A random state.
        '''

        return random.choice(list(self.get_next_states()))

    @abstractmethod
    def calculate_value(self, player: int) -> float:
        '''
        Calculate the value of the game at this current state.

        Parameters:
            player (int): Whose turn it is in the actual game.
        
        Returns:
            float: The value of this game state (will always be between -1 and 1).
        '''

        pass

    @abstractmethod
    def is_terminal_state(self) -> bool:
        '''
        Determine whether the game state is a terminal state.

        Returns:
            bool: Whether the game state is a terminal state or not.
        '''

        pass

    def __eq__(self, other: object) -> bool:
        '''Override the __eq__ function. Two states are equal if their representations are equal.

        Parameters:
            other (object): The state being compared to this one.
        
        Returns:
            bool: Whether the two states are equal or not.
        '''

        if not isinstance(other, State):
            return False
        return type(self.representation) == type(other.representation) and self.representation == other.representation\
        and self.player == other.player
    
    def __hash__(self) -> int:
        '''
        Generate a hash for the state.

        Returns:
        int: A hash value for the state.
        '''

        return hash(str(self.representation))