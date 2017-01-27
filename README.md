# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: To solve a Sudoku, we need to narrow the possible values in each box. Using the Naked Twins technique, we can change the values of a row, a column or/and square, where the twins belongs, eliminating the "naked twin" values in those other boxes.
Because the twins has two values and are two boxes, we can assume that to satisfy Sudoku rules, one of each has to have one of the two possible values. So, it is not possible that other box in the same column, row or/and square has that value. So, that's why it's eliminated from the rest of boxes in column, row or/and square.
We apply a constraint to reduce the search space in future iterations.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: The Diagonal Sudoku doesn't allows two identical values in the diagonals.
Similar as we did with column, row and square, we can apply elimination on the diagonals. If exists a box with an only value in the diagonal, we already know that in the rest of the diagonal boxes that value is not a valid option.
Eliminating those values from diagonal boxes will narrow down the search space in future interactions.
Also, we can do similar approach in Only Choice technique.
We know that the nine values should be on each diagonal, if there is a value that only appears as an option in a unique box in the diagonal, we can conclude that's the box value.
  

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.