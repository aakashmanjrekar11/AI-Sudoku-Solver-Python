
# Part 1: Representation of the given 4x4 Sudoku Puzzle as a Binary CSP :

# Puzzle_4x4 = [[1, None, None, None],
#    		   [None, 2, None, None],
#    		   [None, None, 3, None],
#    		   [None, None, None, 4]]

# variables = [
#       ['C11',1],['C12',1,2,3,4],['C13',1,2,3,4],['C14',1,2,3,4],
#       ['C21',1,2,3,4],['C22',2],['C23',1,2,3,4],['C24',1,2,3,4],
#       ['C31',1,2,3,4],['C32',1,2,3,4],['C33',3],['C34',1,2,3,4],
#       ['C41',1,2,3,4],['C42',1,2,3,4],['C43',1,2,3,4],['C44',4]
# ]

# constraints = [
# 	(('C11','C12','C13','C14'),(1,2,3,4),(2,3,4,1)), # row 1
# 	(('C21','C22','C23','C24'),(1,2,3,4),(2,3,4,1)), # row 2
# 	(('C31','C32','C33','C34'),(1,2,3,4),(2,3,4,1)), # row 3
# 	(('C41','C42','C43','C44'),(1,2,3,4),(2,3,4,1)), # row 4
# 	(('C11','C21','C31','C41'),(1,2,3,4),(2,3,4,1)), # col 1
# 	(('C12','C22','C32','C42'),(1,2,3,4),(2,3,4,1)), # col 2
# 	(('C13','C23','C33','C43'),(1,2,3,4),(2,3,4,1)), # col 3
# 	(('C14','C24','C34','C44'),(1,2,3,4),(2,3,4,1)), # col 4
# 	(('C11','C12','C21','C22'),(1,2,3,4),(2,3,4,1)), # box 1
# 	(('C13','C14','C23','C24'),(1,2,3,4),(2,3,4,1)), # box 2
# 	(('C31','C32','C41','C42'),(1,2,3,4),(2,3,4,1)), # box 3
# 	(('C33','C34','C43','C44'),(1,2,3,4),(2,3,4,1))  # box 4
# ]

'''
- Run the app.py file to see the Flask web app in action on http://127.0.0.1:5000/
- This file contains the code for the Sudoku Solver
'''

#? importing libraries and modules
from copy import deepcopy
from sudoku_constraints import constraints

#! Sample 9x9 Sudoku Puzzle as a 2D array for testing purpose
puzzle1 = [
    [7, 0, 0, 4, 0, 0, 0, 8, 6],
    [0, 5, 1, 0, 8, 0, 4, 0, 0],
    [0, 4, 0, 3, 0, 7, 0, 9, 0],
    [3, 0, 9, 0, 0, 6, 1, 0, 0],
    [0, 0, 0, 0, 2, 0, 0, 0, 0],
    [0, 0, 4, 9, 0, 0, 7, 0, 8],
    [0, 8, 0, 1, 0, 2, 0, 6, 0],
    [0, 0, 6, 0, 5, 0, 9, 1, 0],
    [2, 1, 0, 0, 0, 3, 0, 0, 5]
]


#! PART 2: Define 'revise' function
def revise(csp, var1, var2):
    removed = False
    constraints = csp['constraints'].get((var1, var2), None)
    if constraints is None:
        return removed

    domain1 = csp['variables'][var1]
    domain2 = csp['variables'][var2]

    for value1 in domain1:
        satisfy_constraint = False
        for value2 in domain2:
            if [value1, value2] in constraints:
                satisfy_constraint = True
                break
        if not satisfy_constraint:
            domain1.remove(value1)
            removed = True

    return removed


#! PART 3: Define 'AC_3' function
def AC_3(csp):
    queue = [(var1, var2) for var1 in csp['variables'] for var2 in csp['variables'] if var1 != var2]
    while queue:
        (var1, var2) = queue.pop(0)
        if revise(csp, var1, var2):
            if len(csp['variables'][var1]) == 0:
                return False
            for var3 in csp['variables']:
                if var3 != var1 and var3 != var2:
                    queue.append((var3, var1))
    return True


#! PART 4: Define 'minimum_remaining_values' function
def minimum_remaining_values(csp, assignments):
    unassigned_vars = [var for var in csp['variables'] if var not in assignments]
    min_var = unassigned_vars[0]
    for var in unassigned_vars:
        if len(csp['variables'][var]) < len(csp['variables'][min_var]):
            min_var = var
    return min_var


#! PART 5: Define backtracking search function 'backtrack'
def backtrack(csp):
    assignments = {}
    order_of_assignment = []
    domains = []
    failed_values = {} # added failed_values dictionary
    backtrack_counts = {} # added backtrack_counts dictionary

    def backtrack_helper():
        if len(assignments) == len(csp['variables']):
            return True

        var = minimum_remaining_values(csp, assignments)
        for value in csp['variables'][var]:
            assignments[var] = value
            order_of_assignment.append(var)
            domains.append(deepcopy(csp['variables']))

            csp['variables'][var] = [value]
            inferences = AC_3(csp)

            if inferences:
                result = backtrack_helper()
                if result:
                    return True

            # update failed values and backtrack counts
            if var not in failed_values:
                failed_values[var] = []
            if not inferences:
                failed_values[var].append(value)
                if var not in backtrack_counts:
                    backtrack_counts[var] = 0
                backtrack_counts[var] += 1

            del assignments[var]
            csp['variables'] = deepcopy(domains.pop())
            order_of_assignment.pop()

        return False

    if backtrack_helper():
        return assignments, order_of_assignment, domains, failed_values
    else:
        return None, None, None, None



#! Define 'run_puzzle' function
#? This function solves the puzzle and returns the assignments, order of assignment and domains. It sends these to the GUI over in app.py.
def run_puzzle(puzzle):

    # define variables
    variables = {}
    for i in range(9):
        for j in range(9):
            name = f'C{i+1}{j+1}'
            if puzzle[i][j] == 0:
                variables[name] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            else:
                variables[name] = [puzzle[i][j]]


    #? Define CSP
    CSP = {'variables': variables, 'constraints': constraints}
    # print(CSP['variables'])    
    
    #? Run backtracking search on CSP
    assignments, order_of_assignment, domains, failed_values = backtrack(CSP)
    return(assignments, order_of_assignment, domains, failed_values)

# ---------------- End of code ----------------

# ------------------ TESTING ------------------

#! Testing code without GUI
    # # print the result
    # if assignments is None:
    #     print("No solution found.")
    # else:
    #     print("\n======  Solved Puzzle:  ======")
    #     for i in range(9):
    #         # for j in range(9):
    #         #     name = f'C{i+1}{j+1}'
    #         #     print(assignments[name], end=' ')
    #         # print()
    #         for j in range(9):
    #             name = f'C{i+1}{j+1}'
    #             print(assignments[name], end='')

        # print("\n\n======  Order of assignment:  ======")
        # print(order_of_assignment)

        # print("\n\n======  Domains of remaining unassigned variables after each assignment:  ======")
        # for i, domain in enumerate(domains):
        #     print(f"Step {i+1}: {domain}")

# run_puzzle(puzzle1)