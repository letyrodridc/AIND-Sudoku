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

# Contains a list of boxes in the Sudoku Diagonal from left to right
diagonal_units = [r+c for r,c in list(zip(rows,cols))]

# Contains a list of boxes in the Sudoku Diagonal from right to left
diagonal_units2 = [r+c for r,c in list(zip(rows[::-1],cols))]
