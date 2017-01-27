def cross(A, B):
    return [s+t for s in A for t in B]

rows = 'ABCDEFGHI'
cols = '123456789'
digits = '123456789'

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

unitlist = row_units + column_units + square_units 
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

# Contains a list of boxes in the Sudoku Diagona from left to right
diagonal_units = [r+c for r,c in list(zip(rows,cols))]

# Contains a list of boxes in the Sudoku Diagona from right to left
diagonal_units2 = [r+c for r,c in list(zip(rows[::-1],cols))]


assignments = []


def assign_value(values, box, value):
    """
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


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
    
    while boxes_to_search:
        box = boxes_to_search.pop()
        value = values[box]
        
        for p in peers[box]:
            if p in boxes_to_search and values[p] == value:
                all_twins.append( (box,p) )


    # Eliminate the naked twins as possibilities for their peers
    for box, twin in all_twins:
        value = values[box]

        for p in peers[box].intersection(peers[twin]):
            if not values[p] == value:
                for c in value:
                    values[p] = values[p].replace(c, '')

    return values

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
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def diagonal_peers(block):
    res = set()

    if block in diagonal_units:
        res.union(set(diagonal_units))

    if block in diagonal_units2:
        res.union(set(diagonal_units2))

    if res:
        res.remove(block)

    return res

def diagonal_units_search(block):
    res = list()

    if block in diagonal_units:
        res.append(list(diagonal_units))

    if block in diagonal_units2:
        res.append(list(diagonal_units2))

    return res  

def eliminate(values):
    # Modified for Diagonal Solution
    
    res = dict(values)

    for block in values.keys():
        block_value = values[block]

        if len(block_value) == 1:
            for p in peers[block].union(diagonal_peers(block)):
                assign_value(res, p, res[p].replace(block_value, ''))

    return res
    

def only_choice(values):
    """

    :type values: dict
    """
    new_values = values.copy()  # note: do not modify original values
    boxes = [box for box in values.keys() if len(values[box]) > 1]

    for box in boxes:
        # Picking square units
        box_units = units[box]
        box_units = box_units + diagonal_units_search(box)

        for b_square_units in box_units:
             
            b_square_values = set()
            for p in b_square_units:
                if not box == p:
                    b_square_values = b_square_values | set(values[p])

            choices = set(values[box]) - b_square_values

            if len(choices) == 1:
                assign_value(new_values,box,choices.pop())

    return new_values


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


def search(values):
    values = reduce_puzzle(values)

    not_solved = [b for b in boxes if values[b] == '']
    solved = len([b for b in boxes if len(values[b]) == 1]) == len(boxes)

    if not_solved:
        return None

    if solved:
        return values

    else:

        unfilled_squares = [(len(values[b]), b) for b in boxes if len(values[b]) > 1]
        unfilled_squares.sort()

        # Chose one of the unfilled square s with the fewest possibilities

        selected = unfilled_squares[0][1]

        # Update box using selected
        old_value = values[selected]

        s = None
        for v in old_value:
            values[selected] = v
            # Recursion
            s = s or search(dict(values))

            # Restore previous value
            values[selected] = old_value

        return s
    

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
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))
    

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)
        input('Press enter')
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
