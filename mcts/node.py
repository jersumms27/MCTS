import numpy as np
from typing import Any
from state import State

class Node:
    '''
    A MCTS node to keep track of states.

    Attributes:
        parent (Node): This node's parent node.
        children (set[Node]): This node's child nodes.
        state (State): Which state this node represents.
        total_score (dict[Any, float]): Per-player accumulated simulation value
            (a max-n value vector keyed by player).
        num_sims (int): How many total simulations have been run from this node.

    Methods:
        UCB1: Calculates UCB1 score from a given player's perspective.
        add_children: Add new children to this node.
        update: Update node's simulation statistics.
        get_value: Calculates value of node for a given player based on simulations.
        is_leaf: Determines whether this node is a leaf node or not.
    '''

    def __init__(self, state: State, parent: 'Node | None' = None, probability: float = 1.0) -> None:
        '''
        Create a new node.

        Parameters:
            state (State): Which state this node represents.
            parent (Node | None): This node's parent node; default is None.
        '''

        self.parent: Node | None = parent
        self.children: set[Node] = set()
        self.state: State = state
        self.probability: float = probability

        self.total_score: dict[Any, float] = {} # w_i per player
        self.num_sims: int = 0 # n_i
    
    def sample_child(self, explore_constant: float = np.sqrt(2.0)) -> 'Node | None':
        if self.is_leaf():
            return None
        
        child: Node
        if self.state.is_chance:
            children: list[Node] = list(self.children)
            probs: list[float] = [c.probability for c in children]
            normalized: list[float] = [p / sum(probs) for p in probs]
            child = children[np.random.choice(len(children), p=normalized)]
        else:
            # Decision node: the player to move here picks the child that
            # maximizes their own value (max-n selection).
            child = max(self.children, key=lambda c: c.UCB1(self.state.player, explore_constant))

        return child

    def UCB1(self, player: Any, explore_constant: float = np.sqrt(2.0)) -> float:
        '''
        Calculate the UCB1 value of this state from a given player's perspective.

        Parameters:
            player (Any): The player whose value perspective to score by (the deciding player at the parent).
            explore_constant (float): The exploration constant according to the UCB1 formula; default is sqrt(2).

        Returns:
            float: The UCB1 value.
        '''

        if self.num_sims == 0:
            return float('inf')

        w_i: float = self.total_score.get(player, 0.0)
        n_i: float = float(self.num_sims)
        N_i: float
        if self.parent is None:
            N_i = 1
        else:
            N_i = float(self.parent.num_sims)
        c: float = explore_constant

        return (w_i / n_i) + c * np.sqrt(np.log(N_i) / n_i)

    def add_children(self, children: set['Node']) -> None:
        '''
        Add any number of children to this node.

        Parameters:
            children (set[Node]): New children to be added.
        '''

        self.children = self.children.union(children)
    
    def update(self, result: dict[Any, float]) -> None:
        '''
        Update the node's statistics after a simulation.

        Parameters:
            result (dict[Any, float]): Per-player value vector of the simulation.
        '''

        self.num_sims += 1
        for player, value in result.items():
            self.total_score[player] = self.total_score.get(player, 0.0) + value

    def get_value(self, player: Any) -> float:
        '''
        Calculate value of node for a given player.

        Parameters:
            player (Any): The player whose value to compute.

        Returns:
            float: Value of node given by that player's total score / number of simulations.
        '''
        return self.total_score.get(player, 0.0) / (float(self.num_sims) + 1e-6)
    
    def is_leaf(self) -> bool:
        '''
        Determines whether this is a leaf node or not.

        Returns:
            bool: Whether this is a leaf node or not.
        '''

        return len(self.children) == 0
    
    def __str__(self) -> str:
        avg: dict[Any, float] = {
            player: score / (float(self.num_sims) + 1e-6)
            for player, score in self.total_score.items()
        }

        output: str = ''
        output += str(self.state) + '\n\n'
        output += 'Value: ' + str(avg)

        return output
