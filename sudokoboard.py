import copy
import time
import os

class SudokuCSP:
    def __init__(self, filename):
        self.filename = filename
        self.grid = self.read_board(filename)
        self.variables = [(r, c) for r in range(9) for c in range(9)]
        
        self.domains = {}
        for var in self.variables:
            if self.grid[var[0]][var[1]] == 0:
                self.domains[var] = set(range(1, 10))
            else:
                self.domains[var] = {self.grid[var[0]][var[1]]}
                
        self.neighbors = {var: self.get_neighbors(var) for var in self.variables}
        self.calls = 0
        self.failures = 0

    def read_board(self, filename):
        grid = []
        with open(filename, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                row = [int(c) for c in line if c.isdigit()]
                if len(row) != 9:
                    raise ValueError(f"\nFORMAT ERROR in '{filename}' at line {line_num}: Expected 9 digits, found {len(row)}.")
                grid.append(row)
        if len(grid) != 9:
            raise ValueError(f"\nFORMAT ERROR in '{filename}': Expected 9 rows, found {len(grid)}.")
        return grid

    def get_neighbors(self, var):
        r, c = var
        neighbors = set()
        
        for i in range(9):
            if i != c: neighbors.add((r, i))
            if i != r: neighbors.add((i, c))
            
        br, bc = (r // 3) * 3, (c // 3) * 3
        for i in range(3):
            for j in range(3):
                if (br + i, bc + j) != (r, c):
                    neighbors.add((br + i, bc + j))
                    
        return neighbors

    def revise(self, domains, xi, xj):
        revised = False
        to_remove = set()
        
        for x in domains[xi]:
            if len(domains[xj]) == 1 and x in domains[xj]:
                to_remove.add(x)
                
        for x in to_remove:
            domains[xi].remove(x)
            revised = True
            
        return revised

    def ac3(self, domains, queue=None):
        if queue is None:
            queue = [(xi, xj) for xi in self.variables for xj in self.neighbors[xi]]

        while queue:
            xi, xj = queue.pop(0)
            if self.revise(domains, xi, xj):
                if len(domains[xi]) == 0:
                    return False
                for xk in self.neighbors[xi]:
                    if xk != xj:
                        queue.append((xk, xi))
        return True

    def select_unassigned_variable(self, assignment, domains):
        unassigned = [v for v in self.variables if v not in assignment]
        best_var = None
        min_len = 10 
        
        for var in unassigned:
            if len(domains[var]) < min_len:
                min_len = len(domains[var])
                best_var = var
                
        return best_var

    def forward_check(self, var, value, domains):
        for neighbor in self.neighbors[var]:
            if neighbor in domains and value in domains[neighbor]:
                domains[neighbor].remove(value)
                if len(domains[neighbor]) == 0:
                    return False
        return True

    def is_consistent(self, var, value, assignment):
        for neighbor in self.neighbors[var]:
            if neighbor in assignment and assignment[neighbor] == value:
                return False
        return True

    def backtrack(self, assignment, domains):
        self.calls += 1

        if len(assignment) == len(self.variables):
            return assignment

        var = self.select_unassigned_variable(assignment, domains)

        for value in domains[var]:
            if self.is_consistent(var, value, assignment):
                assignment[var] = value
                
                new_domains = copy.deepcopy(domains)
                new_domains[var] = {value}

                if self.forward_check(var, value, new_domains):
                    queue = [(neighbor, var) for neighbor in self.neighbors[var]]
                    if self.ac3(new_domains, queue):
                        result = self.backtrack(assignment, new_domains)
                        if result:
                            return result

                del assignment[var]

        self.failures += 1
        return False

    def solve(self):
        if not self.ac3(self.domains):
            return None

        assignment = {}
        for var in self.variables:
            if self.grid[var[0]][var[1]] != 0:
                assignment[var] = self.grid[var[0]][var[1]]

        return self.backtrack(assignment, self.domains)

    def print_solution(self, assignment):
        if not assignment:
            print("No solution found.")
            return
            
        print(f"--- Solution for {self.filename} ---")
        for r in range(9):
            row_str = ""
            for c in range(9):
                row_str += str(assignment[(r, c)]) + " "
            print(row_str)
        print("-" * 30)

if __name__ == '__main__':
    files = ["easy.txt", "medium.txt", "hard.txt", "veryhard.txt"]
    
    for file in files:
        if os.path.exists(file):
            print(f"Attempting to solve {file}...")
            try:
                solver = SudokuCSP(file)
                start_time = time.time()
                solution = solver.solve()
                elapsed = time.time() - start_time
                
                solver.print_solution(solution)
                
                print(f"Metrics for {file}:")
                print(f" - BACKTRACK Calls: {solver.calls}")
                print(f" - BACKTRACK Failures: {solver.failures}")
                print(f" - Time taken: {elapsed:.4f} seconds\n")
            except ValueError as e:
                print(e)
        else:
            print(f"File {file} not found. Please ensure it is in the same directory.")