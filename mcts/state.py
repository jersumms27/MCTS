from abc import ABC, abstractmethod
import random
import numpy as np
from typing import Any

class State(ABC):
    '''
    A representation of a game state.

    Attributes:
        representation (Any): Some representation of the game state (e.g. str, list).
        player (int): Which player's turn it currently is at this state of the game.
        num_players (int): Total number of players in the game.
        is_terminal (bool): Whether this state is a terminal state or not.

    Methods:
        get_next_states: Get all states which are possible to reach within 1 action.
        take_random_action: Get the state from taking a random action.
        calculate_value: Calculate the value of the game state.
        is_terminal_state: Determine whether this state is a terminal state.
    '''

    def __init__(self, representation: Any, players: list[Any], player: Any) -> None:
        '''
        Create a new state.

        Parameters:
            representation (Any): Some representation of the game state (e.g. str, list).
            players (list[Any]): All players in turn order.
            player (Any): Which player's turn it currently is at this state of the game.
        '''

        self.representation: Any = representation
        self.players: list[Any] = players
        self.player: Any = player
        self.is_terminal: bool = self.is_terminal_state()

    @property
    def num_players(self) -> int:
        return len(self.players)

    @abstractmethod
    def get_next_states(self) -> set['State']:
        '''
        Get states from taking all possible available actions.

        Returns:
            set[State]: All possible states.
        '''

        pass

    @property
    def is_chance(self) -> bool:
        return False

    def get_chance_outcomes(self) -> dict['State', float]:
        raise NotImplementedError('This state is not a chance state.')

    def take_random_action(self) -> 'State':
        '''
        Get one state by taking a random available action.

        Returns:
            State: A random state.
        '''

        if self.is_chance:
            outcomes = self.get_chance_outcomes()
            states = list(outcomes.keys())
            probs = list(outcomes.values())
            normalized = [p / sum(probs) for p in probs]
            
            return states[np.random.choice(len(states), p=normalized)]

        next_states = list(self.get_next_states())
        if not next_states:
            raise ValueError('Cannot take action from a terminal state.')
        return random.choice(next_states)

    @abstractmethod
    def calculate_value(self, player: Any) -> float:
        '''
        Calculate the value of the game at this current state.

        Parameters:
            player (Any): Whose turn it is in the actual game.
        
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

        return hash((str(self.representation), self.player))