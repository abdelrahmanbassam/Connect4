from Heuristic.heuristic import Heuristic
from Heuristic.normal_score import NormalScore
class HeuristicsFactory:
    def get_heuristic(self, heuristic_name):
        if heuristic_name == "NormalScore":
            return NormalScore()
        return NormalScore()
            

