from Heuristic.heuristic import Heuristic
from Heuristic.normal_score import NormalScore
from Heuristic.consecutive_counts import ConsecutiveCounts
from Heuristic.fast_heuristic import FastHeuristic
class HeuristicsFactory:
    def get_heuristic(self, heuristic_name):
        if heuristic_name == "NormalScore":
            return NormalScore()
        elif heuristic_name == "ConsecutiveCounts":
            return ConsecutiveCounts()
        elif heuristic_name == "FastHeuristic":
            return FastHeuristic()
        return ConsecutiveCounts()
            

