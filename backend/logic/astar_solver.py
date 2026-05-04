from search_algorithm import SearchAlgorithm
from queue import PriorityQueue
from search_algorithm import Node

class AstarNode(Node):
    def __init__(self, state, parent = None, action = None, g = 0, h = 0) -> None:
        self.h = h
        super().__init__(state, parent, action, g)
        
    def __lt__(self, other):
        return self.g + self.h < other.g + other.h 
    
class AStar(SearchAlgorithm):

    def __init__(self, heuristic = lambda x,y : 0, view = False, w = 1) -> None:
        self.heuristic = heuristic
        self.w = w
        super().__init__(view)

    def solve(self, problem) -> list[str] | None:
        frontier = PriorityQueue()
        
        h_init = self.heuristic(problem.init, problem.goal) * self.w
        
        start_node = AstarNode(state=problem.init, parent=None, action=None, g=0, h=h_init)
        
        frontier.put(start_node)
        explored = set()
        
        while not frontier.empty():
            
            current_node = frontier.get()
            current_state = current_node.state
            
            if problem.isGoal(current_state):
                path = []
                while current_node.parent is not None:
                    path.append(current_node.action)
                    current_node = current_node.parent
                
                path.reverse()
                return path
            
            if current_state not in explored:
                explored.add(current_state)
                
                successors = problem.getSuccessors(current_state)
                
                for action, next_state, step_cost in successors:
                    if next_state not in explored:
                        new_g = current_node.g + step_cost
                        new_h = self.heuristic(next_state, problem.goal) * self.w
                        
                        new_node = AstarNode(state=next_state, parent=current_node, action=action, g=new_g, h=new_h)
                        frontier.put(new_node)
                        
        return None