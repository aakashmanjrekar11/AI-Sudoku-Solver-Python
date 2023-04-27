'''
- Install Flask using 'pip install -U Flask'
- Run this file to start Flask app in browser on http://127.0.0.1:5000/
- Also check out the console for debugging info
- For detailed debugging info, set 'app.run(debug=True)' in the last line of this file just like it is by default
'''

#! PART 6: Implementing web-based visualization using Flask

#? Import libraries
from flask import Flask, render_template, request
from sudoku import *

#? Initialize Flask app
app = Flask(__name__)

def parse_input_string(input_string):
    '''function to parse input string into 2D array'''
    input_list = input_string.replace(" ", "").replace("\t", "").replace("\n", "")
    input_grid = [[int(input_list[i*9 + j]) for j in range(9)] for i in range(9)]
    return input_grid

def grid_to_string(grid):
    '''function to convert 2D array to string'''
    output_list = [str(item) for sublist in grid for item in sublist]
    output_string = "".join(output_list)
    return output_string

#? Set up route
@app.route('/', methods=['GET', 'POST'])
def sudoku():
    '''sudoku() function to handle GET and POST requests'''
    
    #? handle POST request with input puzzle string
    if request.method == 'POST':

        #! Convert input string to grid
        input_string = request.form['puzzle']
        print("User input string: ", input_string, "\n")
        
        #! Display input puzzle as 2D grid
        input_grid = parse_input_string(input_string)
        print("Converted input grid:\n", input_grid, "\n")

        #* Run Sudoku solver by calling 'run_puzzle' function from sudoku.py
        assignments, order_of_assignment, domains = run_puzzle(input_grid)

        #? Display order of assignment and domains in console for testing
        # print(order_of_assignment)
        # print(domains)
        
        #? prepare solved puzzle as grid
        output_grid = [[assignments[f"C{i+1}{j+1}"][0] if isinstance(assignments[f"C{i+1}{j+1}"], list) else assignments[f"C{i+1}{j+1}"] for j in range(9)] for i in range(9)]

        #! Display Solved Puzzle as 2D grid in console
        print("Output grid:\n", output_grid, "\n")
        
        #! Display Solved Puzzle as string in console
        output_string = grid_to_string(output_grid)
        print("Output string: ", output_string, "\n")

        #! Convert input grid to string just as a backup
        input_string = grid_to_string(input_grid)

        #! Render index.html template with input and solved puzzles
        return render_template('index.html', input_grid=input_grid, input_string=input_string, output_grid=output_grid, output_string=output_string, order_of_assignment=order_of_assignment, domains=domains)

    #? handle GET request
    return render_template('index.html')

#! Run Flask app in browser in debug mode
if __name__ == '__main__':
    app.run(debug=True)


