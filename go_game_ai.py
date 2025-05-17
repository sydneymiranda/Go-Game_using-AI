import random
from go_game_mcts import MCTSNode, mcts
from go_game_rules import is_suicide


class GoAI:
    def __init__(self, board_size, simulations=100):
        self.board_size = board_size
        self.simulations = simulations

    def get_move(self, board, player_color):
        # Create the root node from the current board state
        root = MCTSNode(board, player_color)

        # Perform MCTS simulation to get the best move
        best_move = None
        for _ in range(self.simulations):
            # Perform MCTS for each simulation
            node = root
            while node.children and not node.untried_moves:
                node = node.best_child()

            # Expand the node if there are untried moves
            if node.untried_moves:
                node = node.expand()

            # Rollout to simulate a random game from this node
            result = node.rollout()

            # Backpropagate the result of the simulation
            node.backpropagate(result)

        # Check for suicide and avoid it
        legal_moves = [move for move in root.get_legal_moves() if not is_suicide(board, move[0], move[1], player_color)]

        if legal_moves:
            # If there are any legal moves, pick one of them
            best_move = random.choice(legal_moves)

        return best_move
