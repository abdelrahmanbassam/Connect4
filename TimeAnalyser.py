import time
import matplotlib.pyplot as plt
from MiniMax.algorithms_factory import AlgorithmsFactory
from Heuristic.heuristics_factory import HeuristicsFactory

class TimeAnalyser:
    def __init__(self):
        self.heuristic = HeuristicsFactory().get_heuristic("ConsecutiveCounts")
        self.algorithms = {
            "MiniMax": 1,
            "MiniMaxWithPruning": 2,
            "Expecti": 3
        }
        self.results = {
            "time": {name: [] for name in self.algorithms},
            "nodes": {name: [] for name in self.algorithms}
        }

    def compare_algorithms(self, board, max_depth=5):
        for depth in range(1, max_depth + 1):
            for name, alg_id in self.algorithms.items():
                algorithm = AlgorithmsFactory().get_algorithm(alg_id, self.heuristic, board, 1, depth)
                start_time = time.time()
                algorithm.minimax(board, depth)
                end_time = time.time()
                self.results["time"][name].append(end_time - start_time)
                self.results["nodes"][name].append(algorithm.nodes_expanded)

    def print_results_table(self):
        depths = list(range(1, len(next(iter(self.results["time"].values()))) + 1))
        for name in self.algorithms:
            print(f"\n{name}")
            for i, depth in enumerate(depths):
                nodes_expanded = self.results["nodes"][name][i]
                time_taken = self.results["time"][name][i]
                print(f"depth = {depth} nodes_expanded = {nodes_expanded} time taken = {time_taken}")


    def plot_results(self):
        # Determine the depth range from the length of results
        depths = list(range(1, len(next(iter(self.results["time"].values()))) + 1))

        # Plot nodes expanded
        plt.figure(figsize=(12, 6))
        for name in self.algorithms:
            plt.plot(depths, self.results["nodes"][name], label=name)
        plt.xlabel('Depth')
        plt.ylabel('Nodes Expanded')
        plt.title('Nodes Expanded vs Depth')
        plt.legend()
        plt.grid(True)
        plt.show()

        # Plot time taken
        plt.figure(figsize=(12, 6))
        for name in self.algorithms:
            plt.plot(depths, self.results["time"][name], label=name)
        plt.xlabel('Depth')
        plt.ylabel('Time (seconds)')
        plt.title('Time Taken vs Depth')
        plt.legend()
        plt.grid(True)
        plt.show()

# Example usage
if __name__ == "__main__":
    board = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]
    ]
    analyser = TimeAnalyser()
    analyser.compare_algorithms(board)
    analyser.print_results_table()
    analyser.plot_results()