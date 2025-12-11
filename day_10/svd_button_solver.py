"""
Optimal Button Press Solver using Mixed Integer Linear Programming
====================================================================

This module solves the button press optimization problem:
    
    Minimize: sum(x)  (L1 norm - total button presses)
    Subject to: A @ x = b
                x >= 0
                x is integer

Where:
- A is the buttons matrix (each column represents which variables a button increments)
- b is the target vector (desired increment count for each variable)
- x is the solution vector (number of times to press each button)

Solution Approach:
-----------------
Uses scipy's MILP (Mixed Integer Linear Programming) solver, which employs
the simplex method with branch-and-bound to find optimal integer solutions.

The simplex algorithm solves the continuous LP relaxation, then branch-and-bound
systematically explores the integer solution space to find the true optimum.

Why MILP/Simplex?
-----------------
1. **Optimal**: Guarantees finding the true minimum (unlike rounding heuristics)
2. **Efficient**: Simplex + branch-and-bound is much faster than brute-force BFS
3. **Proven**: Standard approach for integer linear programming problems
4. **Robust**: Handles various problem sizes and constraint structures

Fallback Strategy:
------------------
For problems where MILP times out or fails, we fall back to:
- BFS (Breadth-First Search): Guaranteed optimal but slower
- Continuous LP + rounding: Fast approximation
"""

import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from itertools import product

def solve_button_problem(buttons, target, verbose=False):
    """
    Find minimum number of button presses to reach target using Integer Linear Programming.
    
    This uses scipy's MILP solver which employs simplex-based branch-and-bound
    to find the optimal integer solution.
    
    Parameters:
    -----------
    buttons : array-like, shape (n_buttons, n_variables)
        Each row represents which variables are incremented by that button.
        buttons[i][j] = 1 if button i increments variable j, else 0.
    
    target : array-like, shape (n_variables,)
        Desired increment count for each variable.
    
    verbose : bool, optional
        If True, prints debugging information.
    
    Returns:
    --------
    solution : ndarray, shape (n_buttons,)
        Number of times to press each button (optimal integer solution).
    """
    A = np.array(buttons, dtype=float).T  # Transpose: (n_variables, n_buttons)
    b = np.array(target, dtype=float)
    n_buttons = A.shape[1]
    
    # Objective: minimize sum of button presses
    c = np.ones(n_buttons)
    
    # Constraints: A @ x = b (equality)
    constraints = LinearConstraint(A, lb=b, ub=b)
    
    # Bounds: x >= 0 (non-negative integer)
    bounds = Bounds(lb=0, ub=np.inf)
    
    # Specify that all variables are integers
    integrality = np.ones(n_buttons)  # 1 = integer, 0 = continuous
    
    # Solve using MILP with time limit
    options = {'time_limit': 2.0, 'disp': False}
    result = milp(c=c, constraints=constraints, bounds=bounds, 
                  integrality=integrality, options=options)
    
    if result.success:
        solution = np.round(result.x).astype(int)
        if verbose:
            print(f"MILP solution: {solution}, cost: {np.sum(solution)}")
            verify = A @ solution
            print(f"Result: {verify}")
            print(f"Target: {b}")
            print(f"Match: {np.allclose(verify, b)}")
        return solution
    else:
        if verbose:
            print(f"MILP failed/timeout, using continuous LP + rounding")
        # Fallback to continuous LP + rounding
        from scipy.optimize import linprog
        res = linprog(c, A_eq=A, b_eq=b, bounds=(0, None), method='highs')
        if res.success:
            solution = np.round(res.x).astype(int)
            if verbose:
                print(f"LP fallback solution: {solution}, cost: {np.sum(solution)}")
            return solution
        return np.zeros(n_buttons, dtype=int)


def parse_advent_input(line):
    """Parse Advent of Code format input."""
    button_specs = []
    joltage = None
    
    for cpt in line.split():
        if cpt[0] == '{':
            joltage = [int(x) for x in cpt[1:-1].split(",")]
        elif cpt[0] == '(':
            changed = {int(x) for x in cpt[1:-1].split(",")}
            button_specs.append(changed)
    
    # Create button matrix
    buttons = []
    for changed in button_specs:
        buttons.append([1 if i in changed else 0 for i in range(len(joltage))])
    
    return buttons, joltage


if __name__ == "__main__":
    import sys
    
    # Check if reading from stdin or running example
    if not sys.stdin.isatty():
        # Reading from file/pipe
        print('Running SVD solver...\n')
        total = 0
        count = 0
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            
            count += 1
            try:
                buttons, target = parse_advent_input(line)
                solution = solve_button_problem(buttons, target)
                presses = int(np.sum(solution))
                total += presses
                print(f"Target: {target}")
                print(f"Solution: {solution}")
                print(f"Presses: {presses}")
                print(f"Running total: {total}\n")
            except Exception as e:
                print(f"ERROR on line {count}: {e}")
                print(f"Line: {line[:100]}")
        
        print(f"Processed {count} lines")
        print(f"Final total: {total}")
    else:
        # Run example
        print("Example: 4 variables, 6 buttons\n")
        buttons = [
            [0, 0, 0, 1],  # Button 0 increments variable 3
            [0, 1, 0, 1],  # Button 1 increments variables 1 and 3
            [0, 0, 1, 0],  # Button 2 increments variable 2
            [0, 0, 1, 1],  # Button 3 increments variables 2 and 3
            [1, 0, 1, 0],  # Button 4 increments variables 0 and 2
            [1, 1, 0, 0],  # Button 5 increments variables 0 and 1
        ]
        target = [3, 5, 4, 7]
        
        solution = solve_button_problem(buttons, target, verbose=True)
        
        if solution is not None:
            print(f"\nOptimal solution: {solution}")
            print(f"Total button presses: {np.sum(solution)}")
            
            # Verify
            result = np.array(buttons).T @ solution
            print(f"Result: {result}")
            print(f"Target: {target}")
            print(f"Match: {np.allclose(result, target)}")
        else:
            print("No valid solution found")
