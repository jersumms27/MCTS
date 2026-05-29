from node import Node
from state import State
import numpy as np
import random
from typing import Any

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
    def __init__(self, player: Any, initial_state: State) -> None:
        '''
        Create a MCTS object.

        Parameters:
            player (Any): Which player the algorithm is calculating for.
            initial_state (State): Initial state of the game.
        '''

        self.player: Any = player
        self.root: Node = Node(state=initial_state)
    
    def get_best_action(self, max_iter: int=10000) -> State:
        '''
        Run the Monte Carlo Tree Search algorithm.

        Parameters:
            max_iter (int): Maximum number of MCTS iterations to run; default is 10000.

        Returns:
            State: The best next possible state for the player.
        '''
        
        for _ in range(max_iter):
            leaf_node: Node = self.selection()

            node: Node | None = self.expansion(leaf_node)

            if node is not None:
                value = self.simulation(node)
                self.backpropagation(node, value)
            else: # leaf node is terminal state
                value = self._value_vector(leaf_node.state)
                self.backpropagation(leaf_node, value)

        best_node: Node = max(self.root.children, key=lambda child: child.get_value(self.player))

        self.update_root(best_node.state)
        return best_node.state

    def selection(self, explore_const: float=float(np.sqrt(2))) -> Node:
        '''
        Select the best leaf node given UCB1 metrics.
        
        Returns:
            Node: Leaf node to be expanded.
        '''
        
        node: Node = self.root
        while not node.is_leaf():
            child: Node | None = node.sample_child(explore_const)
            if child is None:
                break
            node = child

        return node


    def expansion(self, node: Node) -> Node | None:
        '''
        Expand given node into all possible game states reachable within one action.

        Parameters:
            node (Node): The leaf node to be expanded.
        
        Returns:
            Node: A random child of the expanded node.
        '''

        if node.state.is_chance:
            outcomes: dict[State, float] = node.state.get_chance_outcomes()
            node.add_children(set([Node(state, node, prob) for state, prob in outcomes.items()]))
        else:
            node.add_children(set([Node(state, node) for state in node.state.get_next_states()]))

        if len(node.children) == 0:
            return None
        return random.choice(list(node.children))

    def simulation(self, node: Node, max_turns: int=1000) -> dict[Any, float]:
        '''
        Perform a random simulation of the game from the state of the node.

        Parameters:
            node (Node): The node to begin the simulation.

        Returns:
            dict[Any, float]: The per-player value vector of the terminal state of the simulation.
        '''

        state: State = node.state
        num_turns = 0

        while not state.is_terminal and num_turns < max_turns:
            state = state.take_random_action()
            num_turns += 1

        return self._value_vector(state)

    def _value_vector(self, state: State) -> dict[Any, float]:
        '''
        Compute the per-player value vector of a state (for max-n backpropagation).

        Parameters:
            state (State): The state to evaluate.

        Returns:
            dict[Any, float]: A mapping from each player to their value of the state.
        '''

        return {player: state.calculate_value(player) for player in state.players}

    def backpropagation(self, node: Node, value: dict[Any, float]) -> None:
        '''
        Propagate the simulation value vector back through the tree to the root.

        Parameters:
            node (Node): Leaf node which the simulation ran from.
            value (dict[Any, float]): Per-player value vector of the simulation.
        '''

        node.update(value)

        while node.parent is not None:
            node = node.parent
            node.update(value)
    
    def update_root(self, state: State) -> None:
        '''
        Update the root based on new game state.

        Parameters:
            state (State): The new state of the game.
        '''

        nodes: set[Node] = self.root.children
        for _ in range(state.num_players):
            prev_nodes: set[Node] = nodes.copy()
            nodes = set()

            for node in prev_nodes:
                if node.state == state:
                    self.root = node
                    self.root.parent = None
                    return
                else:
                    nodes = nodes.union(node.children)

        self.root = Node(state)
