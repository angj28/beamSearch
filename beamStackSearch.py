class BeamStackSearch: # beam search , depth-first search variation. Back tracking is at the deepest level first (LIFO stack). 
    def __init__(self, beam_width=2):
        self.beam_width = beam_width
        self.stack = []  # Stack of beams for backtracking
        self.best_score = float('-inf')
        self.best_solution = None
    
    def search(self, initial_state):
        # Initialize with the first beam containing only the initial state
        current_beam = [(initial_state, 0)]  # (state, score)
        self.stack.append([])  # Initialize stack with an empty beam for backtracking
        
        while current_beam:
            # Expand current beam
            expansions = []
            for state, score in current_beam:
                # Get all possible next states
                next_states = self.expand_state(state)
                
                for next_state in next_states:
                    next_score = self.evaluate(next_state)
                    expansions.append((next_state, next_score))
                    
                    # Update best solution if we found a better one
                    if next_score > self.best_score and self.is_goal(next_state):
                        self.best_score = next_score
                        self.best_solution = next_state
            
            # If no expansions are possible, backtrack
            if not expansions:
                if not self.stack:  # No more states to backtrack to
                    break
                print("Reached the end with score: " + str(self.best_score) + ", but backtracking.")
                current_beam = self.stack.pop()
                continue
            
            # Sort expansions by score (descending)
            expansions.sort(key=lambda x: x[1], reverse=True)
            
            # Keep the top beam_width states for the next beam
            next_beam = expansions[:self.beam_width]
            
            # Store the remaining states on the stack for backtracking
            if len(expansions) > self.beam_width:
                self.stack.append(expansions[self.beam_width:])
            
            current_beam = next_beam
        
        return self.best_solution, self.best_score
    
    def expand_state(self, state):
        """Generate all possible next states from the current state."""
        raise NotImplementedError
    
    def evaluate(self, state):
        """Evaluate the state and return a score."""
        raise NotImplementedError
    
    def is_goal(self, state):
        """Check if the state is a goal state."""
        raise NotImplementedError


# Finding the path to maximize sum in a grid
class GridPathFinder(BeamStackSearch):
    def __init__(self, grid, beam_width=2):
        super().__init__(beam_width)
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0
    
    def expand_state(self, state):
        row, col, path = state
        expansions = []
        
        possible_moves = [(row+1, col), (row, col+1)]
        
        for new_row, new_col in possible_moves:
            if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                new_path = path + [(new_row, new_col)]
                expansions.append((new_row, new_col, new_path))
        
        return expansions
    
    def evaluate(self, state):
        # Calculate the sum of values along the path
        row, col, path = state
        score = self.grid[0][0]  # Starting position
        for r, c in path:
            score += self.grid[r][c]
        return score
    
    def is_goal(self, state):
        # Check if we've reached the bottom-right corner
        row, col, _ = state
        return row == self.rows - 1 and col == self.cols - 1


# Example application: Find path in the grid with max sum
def main():
    grid = [
        [1, 3, 1, 5],
        [2, 8, 3, 8],
        [10, 2, 5, 10],
        [9, 4, 1, 2]
    ]
    
    # Initial state: (row, col, path_so_far)
    initial_state = (0, 0, [])
    
    finder = GridPathFinder(grid, beam_width=2)
    best_solution, best_score = finder.search(initial_state)
    
    # Print results
    row, col, path = best_solution
    print(f"Best path score: {best_score}")
    print(f"Path: (0,0) -> " + " -> ".join([f"({r},{c})" for r, c in path]))
    
    # Print the grid with the path marked
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if (r == 0 and c == 0) or (r, c) in path:
                print(f"[{grid[r][c]}]", end=" ")
            else:
                print(f" {grid[r][c]} ", end=" ")
        print()


if __name__ == "__main__":
    main()