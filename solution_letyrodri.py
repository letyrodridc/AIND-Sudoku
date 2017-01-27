'''
    Udacity AIND
    Project 1: Solve a Sudoku with AI
    by Leticia Rodriguez 

    ADDITIONALS

    THIS CODE DOENS'T SOLVE DIAGONAL SUDOKUS VARIANT
'''
from utils import *

assignments = []

#UDACITY 
def assign_value(values, box, value):
    """
    Assigns a value to a given box. If it updates the board record it.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
        box (str): box to be udated
        value: new value for the box
    
    Returns:
        values updated with value in box
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

#MY_SOLUTION 
def naked_twins(values):
    """
    Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins

    all_twins = list()
    
    # Are twins! I need 2 values, if > or < I avoid iteration
    boxes_to_search = [box for box in boxes if len(values[box]) == 2]
    
    # Uses a stack just not to add same tuple twice
    while boxes_to_search:
        box = boxes_to_search.pop()
        value = values[box]
        
        for p in peers[box]:
            if p in boxes_to_search and values[p] == value:
                # They have same value, are twins!
                all_twins.append( (box,p) )

    # Eliminate the naked twins as possibilities for their peers
    for box, twin in all_twins:
        value = values[box]

        # It's interested just to update those boxes affected by both twins
        # uses an intersection of peers of both boxes
        for p in peers[box].intersection(peers[twin]):
            if not values[p] == value:
                for c in value:
                    values[p] = values[p].replace(c, '')

    return values

#MY_SOLUTION
def grid_values(grid):
    """
    
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    res = dict()

    for i, c in enumerate(grid):
        k = boxes[i]
        if c=='.':
            res[k] = digits
        else:    
            res[k] = c

    return res

#UDACITY 
def display(values):
    """
    Display the values as a 2-D grid.
    Input: values - The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

#MY_SOLUTION
def eliminate(values):
    """
    Returns a dictionary with elimination technique applied.
    Input: values - The sudoku in dictionary form
    Output: dict - copy of values with elimination technique applied
    """
    
    res = dict(values)

    for block in values.keys():
        block_value = values[block]

        if len(block_value) == 1:

            for p in peers[block]:
                assign_value(res, p, res[p].replace(block_value, ''))

    return res
    
#MY_SOLUTION
def only_choice(values):
    """
    Returns a dictionary with Only Choice technique applied.
    Input: values - The sudoku in dictionary form
    Output: dict - copy of values with Only Choice applied
    """
    new_values = values.copy()  # note: do not modify original values
    boxes = [box for box in values.keys() if len(values[box]) > 1]

    for box in boxes:
        box_units = units[box] 

        for b_square_units in box_units:
             
            b_square_values = set()
            for p in b_square_units:
                if not box == p:
                    b_square_values = b_square_values | set(values[p])

            choices = set(values[box]) - b_square_values

            if len(choices) == 1:
                assign_value(new_values,box,choices.pop())

    return new_values

#MY_SOLUTION
def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Eliminate Strategy
        values = eliminate(values)

        # Only Choice Strategy
        values = only_choice(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])

        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after

        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False

    return values

#MY_SOLUTION - DFS

def search(values):
    """
    Solves a Sudoku
    Input: values - The sudoku in dictionary form
    Output: values - Sudoku solved
    """
    # First, reduce the puzzle using the previous function

    values = reduce_puzzle(values)

    # Verify if could't solved it and there is no solution for that instance
    # See reduce_puzzle
    not_solved = values is False

    if not_solved:
        return None

    # Checks if all the boxes has one value --- so, solved true 
    solved = len([b for b in boxes if len(values[b]) == 1]) == len(boxes)

  
    if solved:
        return values

    else:

        # Chose one of the unfilled square s with the fewest possibilities

        _,selected = min([(len(values[b]), b) for b in boxes if len(values[b]) > 1])

        # Saves selected values
        old_value = values[selected]

        s = None

        # Try each value of the selected
        for v in old_value:
        
            # Update box using one of the values of selected box
            values[selected] = v
            
            # Recursion
            s = s or search(dict(values))

            # Restore previous value
            values[selected] = old_value

        return s

#MY_SOLUTION
def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

    # Converts from sudoku string to sudoku dictionary
    sudoku = grid_values(grid)

    # Search solution
    sudoku = search(sudoku)

    return sudoku


if __name__ == '__main__':
    sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)
    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
