from mcts.node import Node
from state import State
import numpy as np
import random

c: float = np.sqrt(2)
max_iter: int = int(10)
max_sims: int = int(5)

class MCTS:
    '''
    Monte Carlo Tree Search algorithm.

    Attributes:
        player (int): Which player the algorithm is calculating for.
        root (Node): The root node of the tree.
    
    Methods:
        get_best_action: Run the actual MCTS algorithm by getting the best possible action.
        selection: Selects a leaf node based on UCB1.
        expansion: Expands the leaf node into all possible next states.
        simulation: Simulates a game until a terminal state (or other cutoff) is reached.
        backpropagation: Backpropagates the simulation results up the tree to the root node.
        update_root: Update root of the tree based on the new game state.
    '''
    def __init__(self, player: int, initial_state: State) -> None:
        '''
        Create a MCTS object.

        Parameters:
            player (int): Which player the algorithm is calculating for.
            initial_state (State): Initial state of the game.
        '''

        self.player: int = player
        self.root: Node = Node(state=initial_state)
    
    def get_best_action(self) -> State:
        '''
        Run the Monte Carlo Tree Search algorithm.

        Parameters:
            player(int): Which player's turn it currently is.

        Returns:
            State: The best next possible state for the player.
        '''
        
        for _ in range(max_iter):
            leaf_node: Node = self.selection()
            node: Node | None = self.expansion(leaf_node)
            if node is not None:
                value = self.simulation(node)
                self.backpropagation(node, value)
        
        best_node: Node = max(self.root.children, key=lambda child: child.get_value())

        # self.udpate_root(best_node.state, 2)
        return best_node.state

    def selection(self) -> Node:
        '''
        Select the best leaf node given UCB1 metrics.
        
        Returns:
            Node: Leaf node to be expanded.
        '''
        
        node: Node = self.root
        while not node.is_leaf():
            node = max(node.children, key=lambda child: child.UCB1(c))
        
        return node

    def expansion(self, node: Node) -> Node | None:
        '''
        Expand the node into all possible game states reachable within one action.

        Parameters:
            node (Node): The leaf node to be expanded.
        
        Returns:
            Node: A random child of the expanded node.
        '''

        node.add_children(set([Node(state, node) for state in node.state.get_next_states()]))

        if len(node.children) == 0:
            return None
        return random.choice(list(node.children))

    def simulation(self, node: Node) -> float:
        '''
        Perform a random simulation of the game from the state of the node.

        Parameters:
            node (Node): The node to begin the simulation.
        
        Returns:
            float: The value of the terminal state of the simulation.
        '''

        state: State = node.state
        num_sims = 0

        while not state.is_terminal and num_sims < max_sims:
            state = state.take_random_action()
            num_sims += 1
        
        return state.calculate_value(self.player)

    def backpropagation(self, node: Node, value: float) -> None:
        '''
        Propagate the simulation value back through the tree to the root.

        Parameters:
            node (Node): Leaf node which the simulation ran from.
            value (float): Value of the simulation.
        '''
        
        node.update(value)

        while node.parent is not None:
            node = node.parent
            node.update(value)
    
    def udpate_root(self, state: State, num_players: int) -> None:
        '''
        Update the root based on new game state.

        Parameters:
            state (State): The new state of the game.
            num_players (int): Number of players playing the game.
        '''

        nodes: set[Node] = self.root.children
        for _ in range(num_players):
            prev_nodes: set[Node] = nodes.copy()
            nodes = set()

            for node in prev_nodes:
                if node.state == state:
                    self.root = node
                    return
                else:
                    nodes = nodes.union(node.children)
        
        self.root = Node(state)
