class SearchNode:
    def __init__(self, state, parent=None, path_cost=0, heuristic=0):
        self.state = state
        self.parent = parent
        self.path_cost = path_cost
        self.heuristic = heuristic
        self.total_cost = path_cost + heuristic
    
    def __lt__(self, other):
        return self.total_cost < other.total_cost
    
    def get_path(self):
        """Returns the path from start to this node"""
        path = []
        current = self
        while current:
            path.append(current.state)
            current = current.parent
        return list(reversed(path))

class MultipleBranchingProblem:
    """
    A problem with multiple paths where some nodes have identical heuristic values.
    This demonstrates the benefit of flexible beam search.
    """
    
    def __init__(self):
        # Graph represented as adjacency list with costs
        self.graph = {
            'A': [('B', 1), ('C', 1), ('D', 1)],
            'B': [('E', 1), ('F', 1)],
            'C': [('G', 1)],
            'D': [('H', 1), ('I', 1)],
            'E': [('J', 3)],  
            'F': [('K', 1)],
            'G': [('L', 1)],
            'H': [('M', 1)],  
            'I': [('N', 1)],
            'J': [('Z', 10)], 
            'K': [('Z', 9)],   
            'L': [('Z', 8)],
            'M': [('Z', 3)],   
            'N': [('Z', 7)],
        }

        self.heuristic_values = {
            'A': 5,
            'B': 4, 'C': 4, 'D': 4,
            'E': 6, 'F': 4, 'G': 4, 'H': 3, 'I': 3,
            'J': 2, 'K': 2, 'L': 2, 'M': 1, 'N': 2,
            'Z': 0
        }
    
    def get_start_state(self):
        return 'A'
    
    def is_goal_state(self, state):
        return state == 'Z'
    
    def get_successors(self, state):
        return [(next_state, cost) for next_state, cost in self.graph.get(state, [])]
    
    def heuristic(self, state):
        return self.heuristic_values.get(state, float('inf'))

def standard_beam_search(problem, beam_width=2):
    """Standard beam search that strictly keeps only the best beam_width nodes."""
    start = problem.get_start_state()
    start_node = SearchNode(start, None, 0, problem.heuristic(start))
    
    if problem.is_goal_state(start):
        return start_node.get_path()
    
    beam = [start_node]
    iterations = 0
    
    print(f"\nStandard Beam Search (width={beam_width}):")
    print(f"Iteration 0: Beam = [{beam[0].state}]")
    
    while beam and iterations < 10:  
        iterations += 1
        
        # Generate all successors of the current beam
        all_successors = []
        for node in beam:
            for next_state, cost in problem.get_successors(node.state):
                h = problem.heuristic(next_state)
                new_node = SearchNode(next_state, node, node.path_cost + cost, h)
                
                # If goal, return path
                if problem.is_goal_state(next_state):
                    total_cost = new_node.path_cost
                    print(f"Goal found: {new_node.get_path()} (total cost: {total_cost})")
                    return new_node.get_path(), total_cost
                
                all_successors.append(new_node)
        
        # Sort by total cost and select the best beam_width nodes
        all_successors.sort()
        beam = all_successors[:beam_width]
        
        print(f"Iteration {iterations}:")
        print(f"  All successors: {[(n.state, n.total_cost) for n in all_successors]}")
        print(f"  New beam: {[(n.state, n.total_cost) for n in beam]}")
        
        if not beam:
            break
    
    # Show path of best node in the final beam
    if beam:
        best_path = beam[0].get_path()
        print(f"Best partial path: {best_path}")
        return best_path, None
    return None, None

def flexible_beam_search(problem, beam_width=2):
    """
    Flexible beam search that includes all nodes with the same cost 
    as the beam_width-th best node.
    """
    start = problem.get_start_state()
    start_node = SearchNode(start, None, 0, problem.heuristic(start))
    
    if problem.is_goal_state(start):
        return start_node.get_path()
    
    beam = [start_node]
    iterations = 0
    
    print(f"\nFlexible Beam Search (width={beam_width}):")
    print(f"Iteration 0: Beam = [{beam[0].state}]")
    
    while beam and iterations < 10:  # Limit iterations to avoid infinite loops
        iterations += 1
        
        # Generate all successors of the current beam
        all_successors = []
        for node in beam:
            for next_state, cost in problem.get_successors(node.state):
                h = problem.heuristic(next_state)
                new_node = SearchNode(next_state, node, node.path_cost + cost, h)
                
                # If goal, return path
                if problem.is_goal_state(next_state):
                    total_cost = new_node.path_cost
                    print(f"Goal found: {new_node.get_path()} (total cost: {total_cost})")
                    return new_node.get_path(), total_cost
                
                all_successors.append(new_node)
        
        # Sort all successors by total cost
        all_successors.sort()
        
        # Apply flexible beam width rule
        if len(all_successors) > beam_width:
            # Find the cost threshold for the beam_width'th node (the highest cost in the current beam)
            threshold_cost = all_successors[beam_width-1].total_cost
            
            # Find all nodes with cost <= threshold
            beam = [node for node in all_successors if node.total_cost <= threshold_cost]
        else:
            beam = all_successors
        
        print(f"Iteration {iterations}:")
        print(f"  All successors: {[(n.state, n.total_cost) for n in all_successors]}")
        if all_successors:
            print(f"  Threshold cost: {all_successors[min(beam_width-1, len(all_successors)-1)].total_cost}")
        print(f"  New beam: {[(n.state, n.total_cost) for n in beam]}")
        
        if not beam:
            break
    
    # Show path of best node in the final beam
    if beam:
        best_path = beam[0].get_path()
        print(f"Best partial path: {best_path}")
        return best_path, None
    return None, None

# create problem and run both search algorithms
def main():
    problem = MultipleBranchingProblem()
    beam_width = 2
    
    # run standard beam search
    standard_path, standard_cost = standard_beam_search(problem, beam_width)
    
    # run flexible beam search
    flexible_path, flexible_cost = flexible_beam_search(problem, beam_width)
    
    print(f"Standard beam search path: {standard_path} (cost: {standard_cost})")
    print(f"Flexible beam search path: {flexible_path} (cost: {flexible_cost})")
    
    if standard_cost and flexible_cost:
        if standard_cost > flexible_cost:
            print(f"Flexible beam search found a better path with cost savings of {standard_cost - flexible_cost}!")
        elif standard_cost < flexible_cost:
            print(f"Standard beam search found a better path with cost savings of {flexible_cost - standard_cost}!")
        else:
            print("Both searches found paths with equal costs.")

if __name__ == "__main__":
    main()