import math
import random
from go_game_constants import EMPTY, BOARD_SIZE
from go_game_rules import is_suicide, remove_dead_stones

class MCTSNode:
    def __init__(self, board, player, parent=None, move=None):
        self.board = board
        self.player = player
        self.parent = parent
        self.move = move
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = self.get_legal_moves()

    def get_legal_moves(self):
        """Get all legal moves for the current player"""
        legal_moves = []
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                if self.board[y][x] == EMPTY:
                    temp_board = [row[:] for row in self.board]
                    if not is_suicide(temp_board, x, y, self.player):
                        legal_moves.append((x, y))
        return legal_moves

    def expand(self):
        """Expand the node by choosing an untried move and creating a new child node"""
        if self.untried_moves:
            move = self.untried_moves.pop()
            x, y = move
            new_board = [row[:] for row in self.board]  # Create a new board to avoid modifying the original
            new_board[y][x] = self.player
            remove_dead_stones(new_board, self.player)
            child = MCTSNode(new_board, 3 - self.player, self, move)
            self.children.append(child)
            return child
        return None

    def is_terminal_node(self):
        """Check if this node is a terminal node (no untried moves)"""
        return not self.untried_moves

    def best_child(self, c_param=1.41):
        """Select the best child node based on the UCB1 formula"""
        # Limiting the number of children considered for faster selection
        if len(self.children) > 10:  # Limit to top 10 most visited children
            self.children = sorted(self.children, key=lambda c: c.visits, reverse=True)[:10]

        choices_weights = [
            (child.wins / child.visits) + c_param * math.sqrt((2 * math.log(self.visits) / child.visits))
            for child in self.children
        ]
        return self.children[choices_weights.index(max(choices_weights))]

    def rollout(self):
        """Simulate a random game from this node to estimate its score"""
        board = [row[:] for row in self.board]
        current_player = self.player
        depth = 0
        while depth < 30:  # Limit simulation depth to 30 moves
            legal_moves = [
                (x, y) for y in range(BOARD_SIZE)
                for x in range(BOARD_SIZE)
                if board[y][x] == EMPTY and not is_suicide(board, x, y, current_player)
            ]
            if not legal_moves:
                break
            x, y = random.choice(legal_moves)
            board[y][x] = current_player
            remove_dead_stones(board, current_player)
            current_player = 3 - current_player
            depth += 1
        return self.simulate_score(board)

    def simulate_score(self, board):
        """A simple simulation to estimate the winner based on the number of stones"""
        black_stones = sum(row.count('B') for row in board)
        white_stones = sum(row.count('W') for row in board)
        return 1 if (self.player == 'B' and black_stones > white_stones) or (self.player == 'W' and white_stones > black_stones) else 0

    def backpropagate(self, result):
        """Backpropagate the result of the simulation to update the node statistics"""
        self.visits += 1
        self.wins += result
        if self.parent:
            self.parent.backpropagate(1 - result)

def mcts(root, iter_limit=100):
    """Perform Monte Carlo Tree Search to find the best move"""
    for _ in range(iter_limit):
        node = root

        # Selection: Traverse the tree to select the most promising node
        while node.children and not node.untried_moves:
            if node.is_terminal_node():  # Check if it's a terminal node
                break  # Avoid going deeper in the tree if it's a terminal node
            node = node.best_child()

        # Expansion: Expand the node if there are untried moves
        if node.untried_moves:
            node = node.expand()

        # Simulation: Simulate a random game from the expanded node
        result = node.rollout()

        # Backpropagation: Update the node statistics based on the simulation result
        node.backpropagate(result)

    # Return the best move based on the most visited child node
    return sorted(root.children, key=lambda c: c.visits)[-1].move if root.children else None
