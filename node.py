import numpy as np
from state import State

class Node:
    '''
    A MCTS node to keep track of states.

    Attributes:
        parent (Node): This node's parent node.
        children (set[Node]): This node's child notes.
        state (State): Which state this node represents.
        total_score (float): How many simulation wins this node has achieved.
        num_sims (int): How many total simulations have been run from this node.

    Methods:
        UCB1: Calculates UCB1 score.
        add_children: Add new children to this node.
        update: Update node's simulation statistics.
        get_score: Calculates value of node based on simulations.
        is_leaf: Determines whether this node is a leaf node or not.
    '''

    def __init__(self, state: State, parent: 'Node | None'=None) -> None:
        '''
        Create a new node.

        Parameters:
            state (State): Which state this node represents.
            parent (Node | None): This node's parent node; default is None.
        '''

        self.parent: Node | None = parent
        self.children: set[Node] = set()
        self.state: State = state

        self.total_score: float = 0.0 # w_i
        self.num_sims: int = 0 # n_i
    
    def UCB1(self, explore_constant: float=np.sqrt(2.0)) -> float:
        '''
        Calculate the UCB1 value of this state.

        Parameters:
            explore_constant (float): The exploration constant according to the UCB1 formula; default is sqrt(2).
        
        Returns:
            float: The UCB1 value.a
        '''

        w_i: float = self.total_score
        n_i: float = float(self.num_sims) + 1e-6
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
            children: set[Node]: New children to be added.
        '''

        self.children = self.children.union(children)
    
    def update(self, result: float) -> None:
        '''
        Update the node's statistics after a simulation.

        Parameters:
            result (float): Result of the simulation.
        '''

        self.num_sims += 1
        self.total_score += result
    
    def get_value(self) -> float:
        '''
        Calculate value of node.

        Returns:
            float: Value of node given by total score / numer of simulations.
        '''
        return self.total_score / (float(self.num_sims) + 1e-6)
    
    def is_leaf(self) -> bool:
        '''
        Determines whether this is a leaf node or not.

        Returns:
            bool: Whether this is a leaf node or not.
        '''

        return len(self.children) == 0
    
    def __str__(self) -> str:
        output: str = ''
        output += str(self.state) + '\n\n'
        output += 'Value: ' + str(self.get_value())

        return output
